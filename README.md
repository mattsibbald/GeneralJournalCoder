# MDProgress — Medical Literature Specialty Tagger

A Streamlit app that pulls recent articles from PubMed, scores them across 48 physician specialties using a hybrid embedding + ontology model, and surfaces a ranked feed per specialty.

## Features

- **PubMed ingest** — searches 20+ high-impact journals (NEJM, JAMA, BMJ, Lancet, etc.) via NCBI E-utilities
- **Hybrid scoring** — combines semantic embeddings (sentence-transformers or OpenAI) with MeSH/keyword ontology matching, clinical signal, and publication-type weighting
- **48 specialty profiles** — Royal College specialties from Cardiology to Pediatrics, with rich cross-specialty linking (e.g. Kawasaki disease tags both Rheumatology and Pediatrics)
- **LLM adjudication** — optional GPT-4o-mini or Claude call for borderline articles
- **Four tabs**: Run Pipeline · Browse Feed · Test Scorer · Overview

## Quick Start

```bash
git clone https://github.com/mattsibbald/mdprogress.git
cd mdprogress
chmod +x run.sh
./run.sh
```

`run.sh` creates a virtual environment, installs dependencies, and launches Streamlit at http://localhost:8501.

On first run, sentence-transformers downloads its model (~90 MB). Subsequent runs use the disk cache.

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Notes |
|---|---|---|
| `NCBI_EMAIL` | Yes | Any email — required by NCBI TOS |
| `NCBI_API_KEY` | No | Raises rate limit from 3 → 10 req/s. Free at ncbi.nlm.nih.gov/account |
| `OPENAI_API_KEY` | No | Needed for OpenAI embeddings or LLM adjudication |
| `ANTHROPIC_API_KEY` | No | Needed for Anthropic LLM adjudication |

## Deployment on Streamlit Community Cloud

1. Fork or push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set `app.py` as the entry point
4. Add secrets under **Settings → Secrets**:
   ```toml
   NCBI_EMAIL = "you@example.com"
   NCBI_API_KEY = ""        # optional
   OPENAI_API_KEY = ""      # optional
   ANTHROPIC_API_KEY = ""   # optional
   ```

## Architecture

```
fetcher.py          PubMed esearch + efetch → Article objects
embeddings.py       Sentence-transformer / OpenAI embedding engine
scorer.py           Hybrid scoring + LLM adjudication
specialty_profiles.py  48 specialty term lists + descriptions
config.py           PipelineConfig dataclass
pipeline.py         CLI entry point
app.py              Streamlit UI
```

## Requirements

- Python 3.10+
- See `requirements.txt`

## License

MIT
