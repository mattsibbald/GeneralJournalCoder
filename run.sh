#!/usr/bin/env bash
# run.sh — MDProgress local launcher
# First run: creates a virtual environment and installs dependencies.
# Subsequent runs: activates the existing venv and starts Streamlit.
#
# Usage:
#   chmod +x run.sh      (first time only)
#   ./run.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$SCRIPT_DIR/.venv"
ENV_FILE="$SCRIPT_DIR/.env"
ENV_EXAMPLE="$SCRIPT_DIR/.env.example"

# ── Colour helpers ─────────────────────────────────────────────────────────
GREEN="\033[0;32m"; YELLOW="\033[1;33m"; RED="\033[0;31m"; NC="\033[0m"
ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC}  $1"; }
err()  { echo -e "${RED}✗${NC}  $1"; exit 1; }

echo ""
echo "  🩺  MDProgress — Literature Specialty Tagger"
echo "  ─────────────────────────────────────────────"
echo ""

# ── Check Python ───────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    err "python3 not found. Install Python 3.10+ from https://python.org"
fi
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
ok "Python $PY_VER found"

# ── .env setup ─────────────────────────────────────────────────────────────
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE" ]; then
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        warn ".env not found — created from .env.example"
        warn "Edit .env and add your NCBI_EMAIL before the pipeline will run."
        echo ""
    fi
fi

# Warn if NCBI_EMAIL not set
if grep -qE "^NCBI_EMAIL=$" "$ENV_FILE" 2>/dev/null || \
   ! grep -qE "^NCBI_EMAIL=.+" "$ENV_FILE" 2>/dev/null; then
    warn "NCBI_EMAIL is not set in .env — pipeline won't run until you add it."
    warn "Open .env and set: NCBI_EMAIL=you@example.com"
    echo ""
fi

# ── Virtual environment ────────────────────────────────────────────────────
if [ ! -d "$VENV_DIR" ]; then
    echo "  Creating virtual environment…"
    python3 -m venv "$VENV_DIR"
    ok "Virtual environment created at .venv/"
fi

source "$VENV_DIR/bin/activate"
ok "Virtual environment activated"

# ── Install / upgrade dependencies ────────────────────────────────────────
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"
FLAG="$VENV_DIR/.installed"

# Re-install if requirements.txt is newer than the install flag
if [ ! -f "$FLAG" ] || [ "$REQUIREMENTS" -nt "$FLAG" ]; then
    echo ""
    echo "  Installing dependencies (this takes ~2 min on first run)…"
    pip install --quiet --upgrade pip
    pip install --quiet -r "$REQUIREMENTS"
    touch "$FLAG"
    ok "Dependencies installed"
    echo ""
    echo "  Note: sentence-transformers will download its model (~90 MB)"
    echo "  automatically on first pipeline run."
    echo ""
fi

ok "Dependencies up to date"

# ── Cache directories ──────────────────────────────────────────────────────
mkdir -p "$SCRIPT_DIR/.cache/embeddings"

# ── Launch Streamlit ───────────────────────────────────────────────────────
echo ""
echo "  Starting MDProgress…"
echo "  → Open http://localhost:8501 in your browser"
echo "  → Press Ctrl+C to stop"
echo ""

exec streamlit run "$SCRIPT_DIR/app.py" \
    --server.port 8501 \
    --server.headless false \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#0066CC" \
    --theme.backgroundColor "#FFFFFF" \
    --theme.secondaryBackgroundColor "#F0F4F8" \
    --theme.textColor "#1A1A2E"
