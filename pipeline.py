"""
pipeline.py — MDProgress literature pipeline: ingest → embed → score → output.

Usage:
  python pipeline.py                          # run with defaults
  python pipeline.py --months 2              # last 2 months
  python pipeline.py --journals nejm jama bmj  # specific journals
  python pipeline.py --specialty cardiology  # print feed for one specialty
  python pipeline.py --no-llm               # skip LLM adjudication

Environment variables (or .env file):
  NCBI_API_KEY     — PubMed API key (10 req/s vs 3 req/s without)
  NCBI_EMAIL       — required by NCBI TOS
  OPENAI_API_KEY   — for OpenAI embeddings or LLM adjudication
  ANTHROPIC_API_KEY — for Anthropic LLM adjudication

Pipeline steps:
  1. PubMed ingest (fetcher.py)
     - esearch for configured journals + date window
     - efetch full XML records (title, abstract, MeSH, pub type, DOI)
     - Filter: drop editorials, letters, corrections, no-abstract records

  2. Embedding (embeddings.py)
     - Embed specialty profile descriptions (once, cached)
     - Embed article title+abstract (batched, cached per article)
     - Compute cosine similarity matrix: n_articles × n_specialties

  3. Scoring (scorer.py)
     - Compute hybrid score per article × specialty:
         0.45 × embedding_similarity
       + 0.25 × ontology_score (MeSH/keyword term matching)
       + 0.15 × clinical_signal (patient pop, outcomes, procedures)
       + 0.10 × publication_type_signal (RCT/meta-analysis boosted)
       + 0.05 × journal_section_signal
     - Tag as primary (≥ 0.75) or secondary (0.60–0.74)
     - LLM adjudication for borderline cases

  4. Output
     - articles_scored.json  (full output)
     - Prints top articles per specialty to console (if --specialty given)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime

from config import PipelineConfig
from fetcher import ingest
from embeddings import EmbeddingEngine
from scorer import score_articles, get_feed
from specialty_profiles import SPECIALTY_PROFILES, get_specialty_descriptions

# ---------------------------------------------------------------------------
# Journal short → full name map (for CLI convenience)
# ---------------------------------------------------------------------------
JOURNAL_ALIASES = {
    "nejm": "N Engl J Med",
    "jama": "JAMA",
    "bmj": "BMJ",
    "cmaj": "CMAJ",
    "lancet": "Lancet",
    "annals": "Ann Intern Med",
    "jamaint": "JAMA Intern Med",
    "jamacardiol": "JAMA Cardiol",
    "natmed": "Nat Med",
    "plosmed": "PLoS Med",
}


def resolve_journals(aliases: list) -> list:
    return [JOURNAL_ALIASES.get(a.lower(), a) for a in aliases]


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def run(config: PipelineConfig) -> list:
    print("\n" + "=" * 60)
    print("  MDProgress — Literature Specialty Pipeline")
    print(f"  Date range: last {config.months_back} months")
    print(f"  Journals: {', '.join(config.journals)}")
    print(f"  Embeddings: {config.embedding_provider} ({config.st_model if config.embedding_provider == 'sentence_transformers' else config.openai_embedding_model})")
    print(f"  LLM adjudication: {config.llm_provider}")
    print("=" * 60 + "\n")

    # ------------------------------------------------------------------ #
    # Step 1: Ingest
    # ------------------------------------------------------------------ #
    articles = ingest(config)
    if not articles:
        print("No articles returned. Exiting.")
        sys.exit(1)

    # ------------------------------------------------------------------ #
    # Step 2: Embed
    # ------------------------------------------------------------------ #
    engine = EmbeddingEngine(config)

    print("\n[Embeddings] Embedding specialty profile descriptions...")
    specialty_descriptions = get_specialty_descriptions()
    specialty_vecs = engine.embed_specialties(specialty_descriptions)

    print(f"\n[Embeddings] Embedding {len(articles)} article texts...")
    article_texts = [a.full_text_for_embedding() for a in articles]
    article_vecs = engine.embed_articles(article_texts)

    print("\n[Embeddings] Computing similarity matrix...")
    embedding_similarities = engine.similarity_scores(article_vecs, specialty_vecs)

    # ------------------------------------------------------------------ #
    # Step 3: Score
    # ------------------------------------------------------------------ #
    print(f"\n[Scoring] Scoring {len(articles)} articles × {len(SPECIALTY_PROFILES)} specialties...")
    scored = score_articles(articles, embedding_similarities, config)

    # ------------------------------------------------------------------ #
    # Step 4: Output
    # ------------------------------------------------------------------ #
    output = {
        "run_date": datetime.utcnow().isoformat(),
        "config": {
            "months_back": config.months_back,
            "journals": config.journals,
            "embedding_provider": config.embedding_provider,
            "llm_provider": config.llm_provider,
            "threshold_primary": config.threshold_primary,
            "threshold_secondary": config.threshold_secondary,
        },
        "n_articles": len(scored),
        "specialties": list(SPECIALTY_PROFILES.keys()),
        "articles": scored,
    }

    os.makedirs(os.path.dirname(config.output_file) or ".", exist_ok=True)
    with open(config.output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Saved {len(scored)} scored articles → {config.output_file}")

    # Summary stats
    _print_summary(scored)

    return scored


def _print_summary(scored: list) -> None:
    """Print per-specialty article counts."""
    print("\n" + "-" * 50)
    print("Specialty tagging summary (primary articles):")
    print("-" * 50)

    counts = {}
    for art in scored:
        for sp in art["primary_specialties"]:
            counts[sp] = counts.get(sp, 0) + 1

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for sp, n in sorted_counts:
        name = SPECIALTY_PROFILES[sp]["name"]
        bar = "█" * min(n, 40)
        print(f"  {name:<45} {n:>4}  {bar}")

    untagged = sum(1 for a in scored if not a["primary_specialties"])
    print(f"\n  Untagged (no primary specialty): {untagged}")


def print_feed(scored: list, specialty_key: str, top_n: int = 10) -> None:
    """Print the top articles for a specialty to stdout."""
    if specialty_key not in SPECIALTY_PROFILES:
        print(f"Unknown specialty: {specialty_key}")
        print(f"Valid keys: {', '.join(SPECIALTY_PROFILES.keys())}")
        return

    feed = get_feed(scored, specialty_key, include_secondary=True)[:top_n]
    name = SPECIALTY_PROFILES[specialty_key]["name"]

    print(f"\n{'='*60}")
    print(f"  Top {len(feed)} articles for: {name}")
    print(f"{'='*60}")

    for i, art in enumerate(feed, 1):
        tag = "PRIMARY" if specialty_key in art["primary_specialties"] else "secondary"
        print(f"\n{i}. [{tag}] score={art['feed_score']:.3f}")
        print(f"   {art['title']}")
        print(f"   {art['journal']} | {art['pub_date']} | {', '.join(art['pub_types'][:2])}")
        if art.get("doi"):
            print(f"   https://doi.org/{art['doi']}")
        if art.get("key_meaning"):
            print(f"   Meaning: {art['key_meaning'][:200]}")
        print(f"   MeSH: {', '.join(art['mesh_terms'][:5])}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(
        description="MDProgress — PubMed ingest + specialty scoring pipeline"
    )
    p.add_argument("--months", type=int, default=2,
                   help="Months of publications to pull (default: 2)")
    p.add_argument("--journals", nargs="+",
                   help="Journal short codes or full names (default: all configured)")
    p.add_argument("--specialty",
                   help="Specialty key to print feed for (e.g. cardiology)")
    p.add_argument("--top-n", type=int, default=10,
                   help="Number of articles to show per specialty feed")
    p.add_argument("--output", default="articles_scored.json",
                   help="Output JSON file path")
    p.add_argument("--embedding-provider",
                   choices=["sentence_transformers", "openai"],
                   default="sentence_transformers")
    p.add_argument("--llm-provider",
                   choices=["openai", "anthropic", "none"],
                   default="openai")
    p.add_argument("--no-llm", action="store_true",
                   help="Disable LLM adjudication entirely")
    p.add_argument("--max-articles", type=int, default=1000)
    p.add_argument("--load", metavar="FILE",
                   help="Load existing scored JSON instead of re-running ingest+scoring")
    return p.parse_args()


def main():
    args = parse_args()

    config = PipelineConfig()
    config.months_back = args.months
    config.output_file = args.output
    config.max_articles = args.max_articles
    config.embedding_provider = args.embedding_provider

    if args.no_llm:
        config.llm_provider = "none"
    else:
        config.llm_provider = args.llm_provider

    if args.journals:
        config.journals = resolve_journals(args.journals)

    # Load existing output or run full pipeline
    if args.load:
        print(f"Loading scored articles from {args.load}...")
        with open(args.load) as f:
            data = json.load(f)
        scored = data["articles"]
        print(f"Loaded {len(scored)} articles")
    else:
        scored = run(config)

    # Print specialty feed if requested
    if args.specialty:
        print_feed(scored, args.specialty, top_n=args.top_n)


if __name__ == "__main__":
    main()
