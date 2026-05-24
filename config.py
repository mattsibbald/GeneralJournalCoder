"""
config.py — MDProgress literature pipeline configuration.

Copy .env.example → .env and fill in your keys before running.
"""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class PipelineConfig:
    # ------------------------------------------------------------------ #
    # PubMed / NCBI
    # ------------------------------------------------------------------ #
    ncbi_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("NCBI_API_KEY")
    )
    email: str = field(
        default_factory=lambda: os.getenv("NCBI_EMAIL", "admin@mdprogress.com")
    )

    # ------------------------------------------------------------------ #
    # Date range
    # ------------------------------------------------------------------ #
    months_back: int = 2          # Pull last N months of publications

    # ------------------------------------------------------------------ #
    # Journals — PubMed full journal titles (use [Journal] field tag)
    # Checkbox list for the UI; default = all enabled
    # ------------------------------------------------------------------ #
    journals: List[str] = field(default_factory=lambda: [
        "N Engl J Med",
        "JAMA",
        "BMJ",
        "CMAJ",
        "Lancet",
        "Ann Intern Med",
        "JAMA Intern Med",
        "JAMA Cardiol",
        "JAMA Netw Open",
        "JAMA Oncol",
        "Nat Med",
        "PLoS Med",
        "Ann Surg",
        "Circulation",
        "J Am Coll Cardiol",
        "Eur Heart J",
        "Gastroenterology",
        "Gut",
        "Am J Respir Crit Care Med",
        "Diabetes Care",
    ])

    # ------------------------------------------------------------------ #
    # Publication-type filters
    # ------------------------------------------------------------------ #
    excluded_pub_types: List[str] = field(default_factory=lambda: [
        "Editorial",
        "Letter",
        "Comment",
        "News",
        "Obituary",
        "Correction",
        "Retraction",
        "Published Erratum",
        "Biography",
        "Newspaper Article",
        "Personal Narrative",
    ])

    boosted_pub_types: List[str] = field(default_factory=lambda: [
        "Randomized Controlled Trial",
        "Meta-Analysis",
        "Systematic Review",
        "Practice Guideline",
        "Multicenter Study",
    ])

    standard_pub_types: List[str] = field(default_factory=lambda: [
        "Clinical Trial",
        "Observational Study",
        "Cohort Study",
        "Case-Control Study",
        "Review",
        "Original Article",
        "Original Investigation",
        "Research",
    ])

    # ------------------------------------------------------------------ #
    # Scoring weights (must sum to 1.0)
    # ------------------------------------------------------------------ #
    weight_embedding:     float = 0.45
    weight_ontology:      float = 0.25
    weight_clinical:      float = 0.15
    weight_pub_type:      float = 0.10
    weight_journal_sec:   float = 0.05

    # ------------------------------------------------------------------ #
    # Tagging thresholds
    # ------------------------------------------------------------------ #
    threshold_primary:    float = 0.75   # → primary_specialties[]
    threshold_secondary:  float = 0.60   # → secondary_specialties[]
    threshold_llm_review: float = 0.65   # Call LLM when score in [0.60, 0.70]

    # ------------------------------------------------------------------ #
    # Embedding model
    # ------------------------------------------------------------------ #
    # Options: "sentence_transformers" | "openai"
    embedding_provider: str = "sentence_transformers"
    # sentence-transformers model (runs locally, no API key needed)
    st_model: str = "all-MiniLM-L6-v2"
    # OpenAI alternative (requires OPENAI_API_KEY)
    openai_embedding_model: str = "text-embedding-3-small"
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )

    # ------------------------------------------------------------------ #
    # LLM adjudication (for borderline articles)
    # ------------------------------------------------------------------ #
    # Options: "openai" | "anthropic" | "none"
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"      # cheap + fast; or claude-haiku-4-5-20251001
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY")
    )

    # ------------------------------------------------------------------ #
    # Performance / output
    # ------------------------------------------------------------------ #
    max_articles: int = 1000      # Safety cap per run
    batch_size: int = 64          # Embedding batch size
    cache_dir: str = ".cache"     # Disk cache for embeddings + raw XML
    output_file: str = "articles_scored.json"
    top_n_specialties: int = 5    # Save top N specialty scores per article
