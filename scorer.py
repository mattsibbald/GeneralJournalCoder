"""
scorer.py — Hybrid specialty scoring engine.

For each article × specialty pair, computes:

  specialty_score =
      w1 × embedding_similarity      (semantic)
    + w2 × ontology_score            (MeSH + keyword term matching)
    + w3 × clinical_signal           (patient pop, outcomes, procedure)
    + w4 × publication_type_signal   (RCT/meta-analysis boosted)
    + w5 × journal_section_signal    (Research > Opinion)

  Default weights: 0.45 / 0.25 / 0.15 / 0.10 / 0.05

Then runs LLM adjudication only for articles where:
  - Top specialty scores cluster in the ambiguous 0.60–0.70 range, OR
  - No specialty scores confidently (all < threshold_primary), OR
  - Article covers multiple subspecialties

The LLM adjudication prompt is based on the MDProgress relevance prompt
designed to be discipline-sensitive and conservative against noise.
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, List, Optional, Tuple

import numpy as np
from tqdm import tqdm

from config import PipelineConfig
from fetcher import Article
from specialty_profiles import SPECIALTY_PROFILES


# ---------------------------------------------------------------------------
# LLM adjudication prompt
# ---------------------------------------------------------------------------
RELEVANCE_PROMPT = """You are an expert physician and medical literature curator.

Your task is to determine whether a medical publication is relevant to the following physician discipline(s):
{specialty_names}

{specialty_descriptions}

Assess relevance based on whether the article would reasonably be of professional interest or potential clinical, diagnostic, therapeutic, procedural, systems, or educational value to a practicing physician in this discipline.

Inputs:
Title: {title}
Journal: {journal}
Publication type: {pub_types}
Abstract: {abstract}
MeSH terms: {mesh_terms}

Instructions:
1. Determine whether this article is:
   - HIGHLY RELEVANT
   - POSSIBLY RELEVANT
   - NOT RELEVANT

2. Consider:
   - Diseases, conditions, procedures, diagnostics, therapeutics, technologies, imaging, physiology, or complications commonly encountered in the specialty.
   - Interdisciplinary overlap that materially affects practice (e.g., nephrology and heart failure for cardiology; oncology and cardiotoxicity).
   - Practice relevance beyond direct procedural work (guidelines, risk prediction, pharmacology, quality improvement, health systems, AI, education, professionalism, patient safety, policy, workforce).

3. Do NOT classify as relevant based solely on:
   - Incidental mention of a specialty-related term
   - Generic biomarkers or medications without meaningful specialty implications
   - Broad epidemiology with no specialty-specific implications
   - Purely basic science with no plausible translational relevance

4. Weight the following more heavily:
   - Title and conclusion
   - Primary clinical question
   - Patient population
   - Outcomes measured
   - Practical implications for physicians in the specialty

5. When uncertain, prefer POSSIBLY RELEVANT over NOT RELEVANT.

Output only valid JSON (no markdown, no explanation outside JSON):
{{
  "relevance": "HIGHLY RELEVANT | POSSIBLY RELEVANT | NOT RELEVANT",
  "confidence": 0-100,
  "reason": "one sentence explanation",
  "matched_topics": ["topic1", "topic2"],
  "would_surface_in_trending_feed": true or false
}}

Rules:
- HIGHLY RELEVANT = directly important to routine or subspecialty practice.
- POSSIBLY RELEVANT = meaningful adjacent relevance or emerging topic.
- NOT RELEVANT = unlikely a physician in this discipline would reasonably want to read it.
- Set would_surface_in_trending_feed = true for HIGHLY RELEVANT and stronger POSSIBLY RELEVANT articles (confidence ≥ 70).
"""


# ---------------------------------------------------------------------------
# Ontology scoring
# ---------------------------------------------------------------------------
def _normalise(text: str) -> str:
    return text.lower()


def _ontology_score(article: Article, profile: dict) -> float:
    """
    Score based on term overlap between article text and specialty term lists.

    Weights:
      title  core_term     → +5
      abstract core_term   → +2
      title  adjacent_term → +2
      abstract adjacent_term → +1
      MeSH core_term       → +3
      MeSH adjacent_term   → +1.5
      exclusion_term hit   → -5
    """
    title = _normalise(article.title)
    abstract = _normalise(article.abstract)
    mesh_text = _normalise(" ".join(article.mesh_terms))

    score = 0.0
    max_possible = 0.0  # approximate ceiling for normalisation

    for term in profile.get("core_terms", []):
        t = _normalise(term)
        max_possible += 5  # one title hit is the max per term
        if t in title:
            score += 5
        elif t in mesh_text:
            score += 3
        elif t in abstract:
            score += 2

    for term in profile.get("adjacent_terms", []):
        t = _normalise(term)
        max_possible += 2
        if t in title:
            score += 2
        elif t in mesh_text:
            score += 1.5
        elif t in abstract:
            score += 1

    for term in profile.get("exclusion_terms", []):
        t = _normalise(term)
        if t in title or t in abstract:
            score -= 5

    if max_possible == 0:
        return 0.0

    # Normalise against a cap (5 core + 3 adjacent strong hits) rather than
    # the total of all terms — this way a handful of very relevant matches
    # scores high rather than being diluted by a large term list.
    cap = 5 * 5 + 3 * 2     # ≈ 31 points for a very relevant article
    return float(np.clip(score / cap, 0.0, 1.0))


# ---------------------------------------------------------------------------
# Publication type signal
# ---------------------------------------------------------------------------
_PUB_TYPE_SCORES = {
    "Randomized Controlled Trial": 1.0,
    "Meta-Analysis": 1.0,
    "Systematic Review": 0.95,
    "Practice Guideline": 0.95,
    "Multicenter Study": 0.85,
    "Clinical Trial": 0.80,
    "Observational Study": 0.75,
    "Cohort Study": 0.75,
    "Case-Control Study": 0.70,
    "Review": 0.65,
    "Original Article": 0.70,
    "Original Investigation": 0.70,
    "Research": 0.65,
}
_DEFAULT_PUB_TYPE_SCORE = 0.50


def _pub_type_signal(article: Article) -> float:
    best = _DEFAULT_PUB_TYPE_SCORE
    for pt in article.pub_types:
        for key, val in _PUB_TYPE_SCORES.items():
            if key.lower() in pt.lower():
                best = max(best, val)
    return best


# ---------------------------------------------------------------------------
# Journal section signal
# ---------------------------------------------------------------------------
_SECTION_SCORES = {
    "Original Research": 1.0,
    "Guideline": 0.95,
    "Review": 0.80,
    "Other": 0.60,
    "Education": 0.65,
}


def _section_signal(article: Article) -> float:
    return _SECTION_SCORES.get(article.journal_section, 0.60)


# ---------------------------------------------------------------------------
# Clinical signal (heuristic boost for patient-relevant articles)
# ---------------------------------------------------------------------------
_CLINICAL_KEYWORDS = [
    "patient", "clinical", "treatment", "diagnosis", "therapy",
    "mortality", "survival", "outcome", "trial", "randomized",
    "efficacy", "safety", "risk", "prevention", "cohort", "study",
]


def _clinical_signal(article: Article) -> float:
    text = _normalise(article.title + " " + article.abstract[:500])
    hits = sum(1 for kw in _CLINICAL_KEYWORDS if kw in text)
    return float(np.clip(hits / 6, 0.0, 1.0))


# ---------------------------------------------------------------------------
# Hybrid score
# ---------------------------------------------------------------------------
def compute_hybrid_score(
    article: Article,
    specialty_key: str,
    embedding_sim: float,
    config: PipelineConfig,
) -> float:
    profile = SPECIALTY_PROFILES[specialty_key]

    ont = _ontology_score(article, profile)
    clin = _clinical_signal(article)
    pt = _pub_type_signal(article)
    sec = _section_signal(article)

    score = (
        config.weight_embedding  * embedding_sim
        + config.weight_ontology   * ont
        + config.weight_clinical   * clin
        + config.weight_pub_type   * pt
        + config.weight_journal_sec * sec
    )
    return float(np.clip(score, 0.0, 1.0))


# ---------------------------------------------------------------------------
# LLM adjudication
# ---------------------------------------------------------------------------
class LLMAdjudicator:
    def __init__(self, config: PipelineConfig):
        self.config = config

    def _call_openai(self, prompt: str) -> Optional[dict]:
        import openai
        client = openai.OpenAI(api_key=self.config.openai_api_key)
        try:
            resp = client.chat.completions.create(
                model=self.config.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=300,
            )
            raw = resp.choices[0].message.content.strip()
            return json.loads(raw)
        except Exception as e:
            print(f"  [LLM openai error] {e}")
            return None

    def _call_anthropic(self, prompt: str) -> Optional[dict]:
        import anthropic
        client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
        try:
            resp = client.messages.create(
                model=self.config.llm_model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()
            return json.loads(raw)
        except Exception as e:
            print(f"  [LLM anthropic error] {e}")
            return None

    def adjudicate(
        self,
        article: Article,
        specialty_keys: List[str],
    ) -> Dict[str, dict]:
        """
        Run LLM relevance assessment for `article` against the given specialties.
        Returns {specialty_key: {relevance, confidence, reason, matched_topics,
                                  would_surface_in_trending_feed}}
        """
        if self.config.llm_provider == "none":
            return {}

        # Build specialty descriptions block
        specialty_names = ", ".join(
            SPECIALTY_PROFILES[k]["name"] for k in specialty_keys
        )
        specialty_descriptions = "\n".join(
            f"  • {SPECIALTY_PROFILES[k]['name']}: {SPECIALTY_PROFILES[k]['description'][:300]}..."
            for k in specialty_keys
        )

        prompt = RELEVANCE_PROMPT.format(
            specialty_names=specialty_names,
            specialty_descriptions=specialty_descriptions,
            title=article.title,
            journal=article.journal,
            pub_types=", ".join(article.pub_types[:3]),
            abstract=article.abstract[:1200],
            mesh_terms=", ".join(article.mesh_terms[:20]),
        )

        if self.config.llm_provider == "anthropic":
            result = self._call_anthropic(prompt)
        else:
            result = self._call_openai(prompt)

        if result is None:
            return {}

        # Map single result to each queried specialty (LLM assesses all at once)
        return {k: result for k in specialty_keys}


# ---------------------------------------------------------------------------
# Main scoring function
# ---------------------------------------------------------------------------
def score_articles(
    articles: List[Article],
    embedding_similarities: Dict[str, np.ndarray],
    config: PipelineConfig,
) -> List[dict]:
    """
    Score all articles across all specialties.

    embedding_similarities: {specialty_key: ndarray(n_articles,)}

    Returns a list of dicts, one per article, with structure:
    {
      "pmid": ...,
      "doi": ...,
      "title": ...,
      "journal": ...,
      "pub_date": ...,
      "pub_types": [...],
      "mesh_terms": [...],
      "abstract_preview": ...,
      "scores": {specialty_key: float, ...},
      "primary_specialties": [...],
      "secondary_specialties": [...],
      "top_score": float,
      "llm_adjudication": {...}   # only if run
    }
    """
    adjudicator = LLMAdjudicator(config) if config.llm_provider != "none" else None
    specialty_keys = list(SPECIALTY_PROFILES.keys())
    results = []

    # Normalize embedding similarities per article across all specialties.
    # Raw cosine similarities from sentence-transformers sit in the 0.2–0.45
    # range even for highly relevant pairs, which suppresses hybrid scores
    # below the tagging thresholds. Min-max normalisation per row preserves
    # the relative ranking while mapping the best-match to ~1.0.
    sim_matrix = np.stack(
        [embedding_similarities[sk] for sk in specialty_keys], axis=1
    )  # shape: (n_articles, n_specialties)
    row_min = sim_matrix.min(axis=1, keepdims=True)
    row_max = sim_matrix.max(axis=1, keepdims=True)
    sim_range = np.where(row_max - row_min == 0, 1.0, row_max - row_min)
    norm_sim_matrix = (sim_matrix - row_min) / sim_range
    normalized_similarities = {
        sk: norm_sim_matrix[:, idx] for idx, sk in enumerate(specialty_keys)
    }

    for i, article in enumerate(tqdm(articles, desc="Scoring articles")):
        # 1. Compute hybrid scores for all specialties
        scores: Dict[str, float] = {}
        for sk in specialty_keys:
            emb_sim = float(normalized_similarities[sk][i])
            scores[sk] = compute_hybrid_score(article, sk, emb_sim, config)

        # 2. Tag primary and secondary specialties
        primary = [k for k, v in scores.items() if v >= config.threshold_primary]
        secondary = [
            k for k, v in scores.items()
            if config.threshold_secondary <= v < config.threshold_primary
        ]

        # Keep only top_n
        top_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_n = dict(top_scores[: config.top_n_specialties])

        # 3. Decide if LLM adjudication is warranted
        llm_result = {}
        top_vals = [v for _, v in top_scores[:3]]
        needs_llm = (
            adjudicator is not None
            and (
                # Ambiguous: top scores cluster in the borderline zone
                (top_vals and config.threshold_secondary <= top_vals[0] <= config.threshold_llm_review)
                # Or no confident primary specialty found but something is in range
                or (not primary and any(v >= config.threshold_secondary for v in top_vals))
            )
        )

        if needs_llm:
            # Send ambiguous specialties (those near the boundary)
            ambiguous_keys = [
                k for k, v in top_scores[:5]
                if config.threshold_secondary - 0.05 <= v <= config.threshold_llm_review + 0.05
            ]
            if ambiguous_keys:
                llm_result = adjudicator.adjudicate(article, ambiguous_keys)
                # Upgrade/downgrade scores based on LLM result
                for sk, llm_data in llm_result.items():
                    rel = llm_data.get("relevance", "NOT RELEVANT")
                    conf = llm_data.get("confidence", 50) / 100.0
                    if rel == "HIGHLY RELEVANT" and sk not in primary:
                        primary.append(sk)
                    elif rel == "NOT RELEVANT" and sk in secondary:
                        secondary.remove(sk)

        result = {
            "pmid": article.pmid,
            "doi": article.doi,
            "title": article.title,
            "journal": article.journal,
            "pub_date": article.pub_date,
            "pub_types": article.pub_types[:5],
            "mesh_terms": article.mesh_terms[:15],
            "abstract_preview": article.abstract[:400],
            "key_question": article.key_question,
            "key_meaning": article.key_meaning,
            "scores": top_n,                   # top N specialties with scores
            "all_scores": scores,              # full scores dict (optional; large)
            "primary_specialties": sorted(set(primary)),
            "secondary_specialties": sorted(set(secondary)),
            "top_score": top_vals[0] if top_vals else 0.0,
            "llm_adjudication": llm_result,
        }
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Convenience: user-facing feed filter
# ---------------------------------------------------------------------------
def get_feed(
    scored_articles: List[dict],
    specialty_key: str,
    include_secondary: bool = True,
    min_score: float = 0.0,
) -> List[dict]:
    """
    Return articles relevant to a given specialty, sorted by score.

    Args:
        specialty_key: e.g. "cardiology"
        include_secondary: include articles tagged as secondary specialties
        min_score: minimum raw score (0–1) to include
    """
    feed = []
    for art in scored_articles:
        score = art["all_scores"].get(specialty_key, 0.0)
        is_primary = specialty_key in art["primary_specialties"]
        is_secondary = specialty_key in art["secondary_specialties"]

        if score < min_score:
            continue
        if is_primary or (include_secondary and is_secondary):
            feed.append({**art, "feed_score": score})

    feed.sort(key=lambda x: x["feed_score"], reverse=True)
    return feed
