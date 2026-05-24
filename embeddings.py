"""
embeddings.py — Compute and cache embedding vectors.

Supports:
  - sentence-transformers (local, free, default)
  - OpenAI text-embedding-3-small (API key required, higher quality)

Specialty profile descriptions are embedded once and cached to disk.
Article vectors are computed in batches and also cached.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Dict, List, Optional

import numpy as np

from config import PipelineConfig


# ---------------------------------------------------------------------------
# Cosine similarity
# ---------------------------------------------------------------------------
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    a = a / (np.linalg.norm(a) + 1e-10)
    b = b / (np.linalg.norm(b) + 1e-10)
    return float(np.dot(a, b))


def cosine_similarity_matrix(queries: np.ndarray, keys: np.ndarray) -> np.ndarray:
    """
    queries: (n, d)
    keys:    (m, d)
    Returns: (n, m) similarity matrix
    """
    q = queries / (np.linalg.norm(queries, axis=1, keepdims=True) + 1e-10)
    k = keys / (np.linalg.norm(keys, axis=1, keepdims=True) + 1e-10)
    return q @ k.T


# ---------------------------------------------------------------------------
# Embedding backend: sentence-transformers
# ---------------------------------------------------------------------------
class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        print(f"[Embeddings] Loading sentence-transformer: {model_name}")
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str], batch_size: int = 64) -> np.ndarray:
        return self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=False,
        )


# ---------------------------------------------------------------------------
# Embedding backend: OpenAI
# ---------------------------------------------------------------------------
class OpenAIEmbedder:
    def __init__(self, model: str = "text-embedding-3-small", api_key: str = None):
        import openai
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        print(f"[Embeddings] Using OpenAI model: {model}")

    def encode(self, texts: List[str], batch_size: int = 256) -> np.ndarray:
        from tqdm import tqdm
        all_vecs = []
        for i in tqdm(range(0, len(texts), batch_size), desc="OpenAI embeddings"):
            batch = texts[i: i + batch_size]
            resp = self.client.embeddings.create(model=self.model, input=batch)
            vecs = [item.embedding for item in resp.data]
            all_vecs.extend(vecs)
        return np.array(all_vecs, dtype=np.float32)


# ---------------------------------------------------------------------------
# EmbeddingEngine — unified interface with disk caching
# ---------------------------------------------------------------------------
class EmbeddingEngine:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.cache_dir = os.path.join(config.cache_dir, "embeddings")
        os.makedirs(self.cache_dir, exist_ok=True)

        if config.embedding_provider == "openai":
            self.backend = OpenAIEmbedder(
                model=config.openai_embedding_model,
                api_key=config.openai_api_key,
            )
        else:
            self.backend = SentenceTransformerEmbedder(model_name=config.st_model)

    # ------------------------------------------------------------------ #
    # Cache helpers
    # ------------------------------------------------------------------ #
    def _cache_key(self, texts: List[str]) -> str:
        h = hashlib.md5("|".join(texts).encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{h}.npy")

    def _try_load(self, texts: List[str]) -> Optional[np.ndarray]:
        path = self._cache_key(texts)
        if os.path.exists(path):
            return np.load(path)
        return None

    def _save(self, texts: List[str], vecs: np.ndarray) -> None:
        np.save(self._cache_key(texts), vecs)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def embed(self, texts: List[str]) -> np.ndarray:
        """Embed a list of texts, using disk cache when available."""
        cached = self._try_load(texts)
        if cached is not None:
            return cached
        vecs = self.backend.encode(texts, batch_size=self.config.batch_size)
        vecs = vecs.astype(np.float32)
        self._save(texts, vecs)
        return vecs

    def embed_specialties(self, descriptions: Dict[str, str]) -> Dict[str, np.ndarray]:
        """
        Embed specialty profile descriptions and return {key: vector}.
        Cached to avoid re-embedding on every run.
        """
        keys = list(descriptions.keys())
        texts = [descriptions[k] for k in keys]
        vecs = self.embed(texts)
        return {k: vecs[i] for i, k in enumerate(keys)}

    def embed_articles(self, article_texts: List[str]) -> np.ndarray:
        """
        Embed article texts in batches. Returns (n_articles, dim) matrix.
        Articles are cached per unique text hash.
        """
        # Cache per individual article to allow incremental runs
        results = []
        to_compute: List[tuple[int, str]] = []

        for idx, text in enumerate(article_texts):
            h = hashlib.md5(text.encode()).hexdigest()
            path = os.path.join(self.cache_dir, f"art_{h}.npy")
            if os.path.exists(path):
                results.append((idx, np.load(path)))
            else:
                to_compute.append((idx, text, path))

        if to_compute:
            batch_texts = [t for _, t, _ in to_compute]
            vecs = self.backend.encode(batch_texts, batch_size=self.config.batch_size)
            for (idx, text, path), vec in zip(to_compute, vecs):
                np.save(path, vec.astype(np.float32))
                results.append((idx, vec))

        results.sort(key=lambda x: x[0])
        return np.stack([v for _, v in results])

    def similarity_scores(
        self,
        article_vecs: np.ndarray,
        specialty_vecs: Dict[str, np.ndarray],
    ) -> Dict[str, np.ndarray]:
        """
        Compute cosine similarity between each article and each specialty profile.

        Returns:
            {specialty_key: np.ndarray of shape (n_articles,)}
        """
        specialty_keys = list(specialty_vecs.keys())
        specialty_matrix = np.stack([specialty_vecs[k] for k in specialty_keys])
        # (n_articles, n_specialties)
        sim_matrix = cosine_similarity_matrix(article_vecs, specialty_matrix)
        return {k: sim_matrix[:, i] for i, k in enumerate(specialty_keys)}
