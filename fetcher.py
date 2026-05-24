"""
fetcher.py — Pull recent articles from PubMed using NCBI E-utilities.

Strategy:
  1. esearch  → get PMIDs for selected journals in the date window
  2. efetch   → retrieve full XML (title, abstract, MeSH, pub type, DOI, etc.)
  3. Filter   → drop editorials, letters, corrections, etc.
  4. Cache    → store raw XML and parsed records to avoid repeated API calls
"""

from __future__ import annotations

import hashlib
import json
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

import requests
from tqdm import tqdm

from config import PipelineConfig


# ---------------------------------------------------------------------------
# PubMed E-utilities base URL
# ---------------------------------------------------------------------------
EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


# ---------------------------------------------------------------------------
# Data model for a single article
# ---------------------------------------------------------------------------
class Article:
    def __init__(self):
        self.pmid: str = ""
        self.doi: str = ""
        self.title: str = ""
        self.abstract: str = ""
        self.journal: str = ""
        self.pub_date: str = ""
        self.pub_types: List[str] = []
        self.mesh_terms: List[str] = []
        self.keywords: List[str] = []
        self.authors: List[str] = []
        self.journal_section: str = ""   # e.g. "Original Article", "Review"
        self.structured_abstract: Dict[str, str] = {}  # BACKGROUND, METHODS, etc.
        self.key_question: str = ""      # JAMA "Question"
        self.key_meaning: str = ""       # JAMA "Meaning"

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Article":
        a = cls()
        a.__dict__.update(d)
        return a

    def full_text_for_embedding(self) -> str:
        """Combine title + abstract for embedding."""
        parts = [self.title]
        if self.key_question:
            parts.append(f"Question: {self.key_question}")
        if self.key_meaning:
            parts.append(f"Meaning: {self.key_meaning}")
        if self.abstract:
            parts.append(self.abstract)
        return " ".join(parts)

    def is_excluded(self, config: PipelineConfig) -> bool:
        """Return True if article should be dropped based on pub type."""
        for pt in self.pub_types:
            for excl in config.excluded_pub_types:
                if excl.lower() in pt.lower():
                    return True
        return False


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def _cache_path(cache_dir: str, key: str) -> str:
    h = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(cache_dir, f"{h}.json")


def _load_cache(cache_dir: str, key: str) -> Optional[dict]:
    p = _cache_path(cache_dir, key)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def _save_cache(cache_dir: str, key: str, data: dict) -> None:
    os.makedirs(cache_dir, exist_ok=True)
    p = _cache_path(cache_dir, key)
    with open(p, "w") as f:
        json.dump(data, f)


# ---------------------------------------------------------------------------
# PubMed API helpers
# ---------------------------------------------------------------------------
def _build_params(config: PipelineConfig, extra: dict = None) -> dict:
    params = {"tool": "mdprogress", "email": config.email}
    if config.ncbi_api_key:
        params["api_key"] = config.ncbi_api_key
    if extra:
        params.update(extra)
    return params


def _get(url: str, params: dict, retries: int = 3) -> requests.Response:
    """GET with retry/backoff."""
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"  [retry in {wait}s] {e}")
            time.sleep(wait)


# ---------------------------------------------------------------------------
# Step 1: esearch — get PMIDs
# ---------------------------------------------------------------------------
def search_pmids(config: PipelineConfig) -> List[str]:
    """
    Build a PubMed query for all configured journals within the date window
    and return a list of PMIDs.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=config.months_back * 30)

    # Journal filter
    journal_clauses = " OR ".join(
        f'"{j}"[Journal]' for j in config.journals
    )
    journal_filter = f"({journal_clauses})"

    # Date filter (PDAT = publication date)
    date_filter = (
        f'("{start_date.strftime("%Y/%m/%d")}"[PDAT] : '
        f'"{end_date.strftime("%Y/%m/%d")}"[PDAT])'
    )

    # Require abstract
    has_abstract = "hasabstract[text]"

    query = f"{journal_filter} AND {date_filter} AND {has_abstract}"
    print(f"\n[PubMed] Query: {query}\n")

    cache_key = f"search:{query}"
    cached = _load_cache(config.cache_dir, cache_key)
    if cached:
        print(f"  → Loaded {len(cached['pmids'])} PMIDs from cache")
        return cached["pmids"]

    params = _build_params(config, {
        "db": "pubmed",
        "term": query,
        "retmax": config.max_articles,
        "retmode": "json",
        "sort": "pub date",
    })

    r = _get(f"{EUTILS_BASE}/esearch.fcgi", params)
    data = r.json()
    pmids = data.get("esearchresult", {}).get("idlist", [])
    print(f"  → Found {len(pmids)} PMIDs")

    _save_cache(config.cache_dir, cache_key, {"pmids": pmids})
    return pmids


# ---------------------------------------------------------------------------
# Step 2: efetch — retrieve XML records in batches
# ---------------------------------------------------------------------------
def fetch_articles(pmids: List[str], config: PipelineConfig) -> List[Article]:
    """
    Fetch full PubMed records for the given PMIDs (batched) and parse them.
    Results are cached per batch.
    """
    articles: List[Article] = []
    batch_size = 100  # PubMed recommends ≤ 200; keep smaller for reliability

    for i in tqdm(range(0, len(pmids), batch_size), desc="Fetching PubMed XML"):
        batch = pmids[i: i + batch_size]
        batch_key = f"fetch:{'_'.join(batch)}"
        cached = _load_cache(config.cache_dir, batch_key)

        if cached:
            articles.extend([Article.from_dict(d) for d in cached["articles"]])
            continue

        params = _build_params(config, {
            "db": "pubmed",
            "id": ",".join(batch),
            "rettype": "xml",
            "retmode": "xml",
        })

        r = _get(f"{EUTILS_BASE}/efetch.fcgi", params)
        batch_articles = _parse_xml(r.text)

        _save_cache(config.cache_dir, batch_key, {
            "articles": [a.to_dict() for a in batch_articles]
        })
        articles.extend(batch_articles)

        # Respect NCBI rate limits (10 req/s with key, 3 req/s without)
        time.sleep(0.15 if config.ncbi_api_key else 0.4)

    return articles


# ---------------------------------------------------------------------------
# XML parser
# ---------------------------------------------------------------------------
def _parse_xml(xml_text: str) -> List[Article]:
    """Parse PubMed efetch XML into Article objects."""
    articles = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"  [XML parse error] {e}")
        return articles

    for record in root.findall(".//PubmedArticle"):
        try:
            articles.append(_parse_record(record))
        except Exception as e:
            print(f"  [record parse error] {e}")

    return articles


def _parse_record(record: ET.Element) -> Article:
    a = Article()
    mc = record.find("MedlineCitation")
    if mc is None:
        return a

    # PMID
    pmid_el = mc.find("PMID")
    if pmid_el is not None:
        a.pmid = pmid_el.text or ""

    article_el = mc.find("Article")
    if article_el is None:
        return a

    # Title
    title_el = article_el.find("ArticleTitle")
    if title_el is not None:
        a.title = "".join(title_el.itertext()).strip()

    # Abstract
    abstract_el = article_el.find("Abstract")
    if abstract_el is not None:
        sections: Dict[str, str] = {}
        plain_parts = []
        for at in abstract_el.findall("AbstractText"):
            label = at.get("Label", "")
            text = "".join(at.itertext()).strip()
            if label:
                sections[label] = text
                plain_parts.append(f"{label}: {text}")
                # Capture JAMA-style structured sections
                if label.upper() == "QUESTION":
                    a.key_question = text
                elif label.upper() == "MEANING":
                    a.key_meaning = text
            else:
                plain_parts.append(text)
        a.abstract = " ".join(plain_parts)
        a.structured_abstract = sections

    # Journal
    journal_el = article_el.find("Journal")
    if journal_el is not None:
        jt = journal_el.find("Title")
        ja = journal_el.find("ISOAbbreviation")
        a.journal = (jt.text if jt is not None else (ja.text if ja is not None else ""))

    # Publication date
    pub_date = article_el.find(".//PubDate")
    if pub_date is not None:
        year = (pub_date.findtext("Year") or
                pub_date.findtext("MedlineDate", "")[:4])
        month = pub_date.findtext("Month", "01")
        day = pub_date.findtext("Day", "01")
        a.pub_date = f"{year}-{month}-{day}"

    # Publication types
    for pt in article_el.findall(".//PublicationType"):
        if pt.text:
            a.pub_types.append(pt.text.strip())

    # DOI
    for eloc in article_el.findall(".//ELocationID"):
        if eloc.get("EIdType") == "doi":
            a.doi = eloc.text or ""
            break

    # Authors
    for auth in article_el.findall(".//Author"):
        last = auth.findtext("LastName", "")
        initials = auth.findtext("Initials", "")
        if last:
            a.authors.append(f"{last} {initials}".strip())

    # MeSH headings
    mh_list = mc.find("MeshHeadingList")
    if mh_list is not None:
        for mh in mh_list.findall("MeshHeading"):
            desc = mh.find("DescriptorName")
            if desc is not None and desc.text:
                a.mesh_terms.append(desc.text.strip())
            for qual in mh.findall("QualifierName"):
                if qual.text:
                    a.mesh_terms.append(f"{desc.text}/{qual.text}")

    # Author keywords
    for kw in mc.findall(".//Keyword"):
        if kw.text:
            a.keywords.append(kw.text.strip())

    # Journal section (from ArticleId or DataBankList — best effort)
    # Some journals expose this in title prefix; approximate from pub type
    if "Review" in a.pub_types:
        a.journal_section = "Review"
    elif "Randomized Controlled Trial" in a.pub_types:
        a.journal_section = "Original Research"
    elif "Practice Guideline" in a.pub_types:
        a.journal_section = "Guideline"
    else:
        a.journal_section = "Other"

    return a


# ---------------------------------------------------------------------------
# Step 3: filter
# ---------------------------------------------------------------------------
def filter_articles(articles: List[Article], config: PipelineConfig) -> List[Article]:
    """Remove editorials, letters, corrections, and articles with no abstract."""
    before = len(articles)
    filtered = [
        a for a in articles
        if a.abstract.strip()          # must have abstract
        and a.title.strip()            # must have title
        and not a.is_excluded(config)  # not in excluded pub types
    ]
    print(f"  Filtered: {before} → {len(filtered)} articles "
          f"({before - len(filtered)} dropped)")
    return filtered


# ---------------------------------------------------------------------------
# Main ingest function
# ---------------------------------------------------------------------------
def ingest(config: PipelineConfig) -> List[Article]:
    """Full ingest pipeline: search → fetch → filter → return articles."""
    print("=" * 60)
    print("MDProgress — PubMed Ingest")
    print("=" * 60)

    pmids = search_pmids(config)
    if not pmids:
        print("No PMIDs found. Check journal names and date range.")
        return []

    articles = fetch_articles(pmids, config)
    articles = filter_articles(articles, config)

    print(f"\n✓ Ingest complete: {len(articles)} articles ready for scoring\n")
    return articles


# ---------------------------------------------------------------------------
# CLI for standalone use
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cfg = PipelineConfig()
    arts = ingest(cfg)
    print(f"\nSample article: {arts[0].title if arts else 'none'}")
