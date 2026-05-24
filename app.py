"""
app.py — MDProgress Streamlit UI

Run with:
    streamlit run app.py

Four tabs:
  1. Run Pipeline  — select journals, date range, run ingest + scoring
  2. Browse Feed   — pick a specialty, browse tagged articles with score details
  3. Test Scorer   — paste any title/abstract and score it against any specialty
  4. Overview      — bar chart of article counts per specialty
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timedelta

import streamlit as st

# ── path so we can import our own modules ──────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from specialty_profiles import SPECIALTY_PROFILES

# ── page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MDProgress — Literature Tester",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── colour palette ──────────────────────────────────────────────────────────
PRIMARY_COLOR   = "#0066CC"
SUCCESS_COLOR   = "#16A34A"
WARNING_COLOR   = "#D97706"
DANGER_COLOR    = "#DC2626"
NEUTRAL_COLOR   = "#6B7280"

# ── available journals ──────────────────────────────────────────────────────
JOURNALS = {
    "N Engl J Med":     "NEJM",
    "JAMA":             "JAMA",
    "BMJ":              "BMJ",
    "CMAJ":             "CMAJ",
    "Lancet":           "Lancet",
    "Ann Intern Med":   "Annals",
    "JAMA Intern Med":  "JAMA Internal Med",
    "JAMA Cardiol":     "JAMA Cardiology",
    "JAMA Netw Open":   "JAMA Network Open",
    "JAMA Oncol":       "JAMA Oncology",
    "Nat Med":          "Nature Medicine",
    "PLoS Med":         "PLOS Medicine",
    "Circulation":      "Circulation",
    "J Am Coll Cardiol":"JACC",
    "Eur Heart J":      "European Heart Journal",
    "Gastroenterology": "Gastroenterology",
    "Am J Respir Crit Care Med": "AJRCCM",
    "Diabetes Care":    "Diabetes Care",
    "Ann Surg":         "Annals of Surgery",
    "Gut":              "Gut",
}

DEFAULT_JOURNALS = [
    "N Engl J Med", "JAMA", "BMJ", "CMAJ", "Lancet",
    "Ann Intern Med", "JAMA Intern Med", "Nat Med",
]

# ── specialty display names ─────────────────────────────────────────────────
SPECIALTY_OPTIONS = {
    k: v["name"] for k, v in SPECIALTY_PROFILES.items()
}

# ── session state defaults ──────────────────────────────────────────────────
if "scored_articles" not in st.session_state:
    st.session_state.scored_articles = []
if "run_complete" not in st.session_state:
    st.session_state.run_complete = False
if "last_output_file" not in st.session_state:
    st.session_state.last_output_file = "articles_scored.json"


# ════════════════════════════════════════════════════════════════════════════
# Sidebar
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image("https://img.icons8.com/color/96/stethoscope.png", width=56)
    st.title("MDProgress")
    st.caption("Medical Literature Specialty Tagger")
    st.divider()

    # -- Journal selector ---------------------------------------------------
    st.subheader("📰 Journals")
    all_journals = st.checkbox("Select all", value=False, key="all_journals")

    journal_selections = {}
    for full_name, label in JOURNALS.items():
        default = full_name in DEFAULT_JOURNALS
        journal_selections[full_name] = st.checkbox(
            label,
            value=True if all_journals else default,
            key=f"j_{full_name}",
        )
    selected_journals = [j for j, checked in journal_selections.items() if checked]

    st.divider()

    # -- Date range --------------------------------------------------------
    st.subheader("📅 Date range")
    months_back = st.slider(
        "Months back", min_value=1, max_value=6, value=2,
        help="Pull publications from the last N months"
    )

    st.divider()

    # -- Model settings ----------------------------------------------------
    st.subheader("⚙️ Settings")
    embedding_provider = st.selectbox(
        "Embedding model",
        options=["sentence_transformers", "openai"],
        index=0,
        help="sentence_transformers runs locally (free). OpenAI requires an API key."
    )
    llm_provider = st.selectbox(
        "LLM adjudication",
        options=["none", "openai", "anthropic"],
        index=0,
        help="Calls the LLM only for borderline articles. 'none' skips it entirely."
    )

    st.divider()
    st.caption(f"v0.1 | {datetime.today().strftime('%Y-%m-%d')}")


# ════════════════════════════════════════════════════════════════════════════
# Tabs
# ════════════════════════════════════════════════════════════════════════════
tab_run, tab_browse, tab_test, tab_overview = st.tabs([
    "▶️  Run Pipeline",
    "🔍  Browse Feed",
    "🧪  Test Scorer",
    "📊  Overview",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Run Pipeline
# ════════════════════════════════════════════════════════════════════════════
with tab_run:
    st.header("Run Pipeline")

    col_conf, col_info = st.columns([2, 1])

    with col_conf:
        st.write("**Selected journals:**")
        if selected_journals:
            st.success(", ".join(JOURNALS[j] for j in selected_journals))
        else:
            st.error("Select at least one journal in the sidebar.")

        ncbi_key   = st.text_input("NCBI API key (optional, raises rate limit)",
                                   type="password",
                                   help="Get free key at ncbi.nlm.nih.gov/account")
        ncbi_email = st.text_input("NCBI email (required by NCBI TOS)",
                                   value=os.getenv("NCBI_EMAIL", ""),
                                   placeholder="you@example.com")
        openai_key = st.text_input("OpenAI API key (needed for openai embedding/LLM)",
                                   type="password",
                                   value=os.getenv("OPENAI_API_KEY", ""))
        output_path = st.text_input("Output file", value="articles_scored.json")

        st.divider()
        col_run, col_load = st.columns(2)

        with col_run:
            run_btn = st.button(
                "🚀 Run full pipeline",
                disabled=not selected_journals or not ncbi_email,
                use_container_width=True,
                type="primary",
            )

        with col_load:
            load_btn = st.button(
                "📂 Load existing results",
                use_container_width=True,
            )
            load_file = st.text_input(
                "File to load", value="articles_scored.json",
                label_visibility="collapsed"
            )

    with col_info:
        st.info(
            "**Pipeline steps**\n\n"
            "1. **Ingest** — PubMed esearch + efetch for selected journals\n"
            "2. **Embed** — Title + abstract vectorised\n"
            "3. **Score** — Hybrid score across all 48 specialties\n"
            "4. **Tag** — Primary (≥ 0.75) / Secondary (0.60–0.74)\n\n"
            "Results cached to disk — re-runs are fast."
        )
        st.warning(
            "**First run:** sentence-transformers will download "
            "~90 MB model on first use. Subsequent runs use cache."
        )

    # -- Load existing results ---------------------------------------------
    if load_btn:
        if os.path.exists(load_file):
            with open(load_file) as f:
                data = json.load(f)
            st.session_state.scored_articles = data.get("articles", [])
            st.session_state.run_complete = True
            st.session_state.last_output_file = load_file
            st.success(f"✓ Loaded {len(st.session_state.scored_articles)} articles from {load_file}")
        else:
            st.error(f"File not found: {load_file}")

    # -- Run pipeline ------------------------------------------------------
    if run_btn:
        if not ncbi_email:
            st.error("NCBI email is required.")
            st.stop()

        # Set env vars for sub-modules
        if ncbi_key:
            os.environ["NCBI_API_KEY"] = ncbi_key
        os.environ["NCBI_EMAIL"] = ncbi_email
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key

        from config import PipelineConfig
        from fetcher import ingest
        from embeddings import EmbeddingEngine
        from scorer import score_articles
        from specialty_profiles import get_specialty_descriptions

        cfg = PipelineConfig()
        cfg.journals = selected_journals
        cfg.months_back = months_back
        cfg.embedding_provider = embedding_provider
        cfg.llm_provider = llm_provider
        cfg.output_file = output_path
        if ncbi_key:
            cfg.ncbi_api_key = ncbi_key
        cfg.email = ncbi_email
        if openai_key:
            cfg.openai_api_key = openai_key

        progress_bar = st.progress(0, text="Starting…")
        status_box   = st.empty()

        try:
            # Step 1: Ingest
            status_box.info("Step 1/4 — Fetching articles from PubMed…")
            progress_bar.progress(5, text="Searching PubMed…")
            articles = ingest(cfg)
            progress_bar.progress(30, text=f"Fetched {len(articles)} articles")

            if not articles:
                st.error("No articles returned. Check journal names and date range.")
                st.stop()

            # Step 2: Embed specialties
            status_box.info("Step 2/4 — Embedding specialty profiles…")
            progress_bar.progress(35, text="Embedding specialty profiles…")
            engine = EmbeddingEngine(cfg)
            specialty_vecs = engine.embed_specialties(get_specialty_descriptions())
            progress_bar.progress(50, text="Specialty profiles embedded")

            # Step 3: Embed articles
            status_box.info(f"Step 3/4 — Embedding {len(articles)} articles…")
            progress_bar.progress(55, text="Embedding articles…")
            article_texts = [a.full_text_for_embedding() for a in articles]
            article_vecs  = engine.embed_articles(article_texts)
            emb_sims      = engine.similarity_scores(article_vecs, specialty_vecs)
            progress_bar.progress(75, text="Embeddings complete")

            # Step 4: Score
            status_box.info(f"Step 4/4 — Scoring {len(articles)} articles × 48 specialties…")
            progress_bar.progress(80, text="Scoring…")
            scored = score_articles(articles, emb_sims, cfg)
            progress_bar.progress(95, text="Writing output…")

            # Save
            output = {
                "run_date": datetime.utcnow().isoformat(),
                "config": {
                    "months_back": cfg.months_back,
                    "journals": cfg.journals,
                    "embedding_provider": cfg.embedding_provider,
                },
                "n_articles": len(scored),
                "articles": scored,
            }
            with open(cfg.output_file, "w") as f:
                json.dump(output, f, indent=2)

            st.session_state.scored_articles = scored
            st.session_state.run_complete = True
            st.session_state.last_output_file = cfg.output_file

            progress_bar.progress(100, text="Done!")
            status_box.success(
                f"✓ Pipeline complete — {len(scored)} articles scored across 48 specialties."
            )

        except Exception as e:
            status_box.error(f"Pipeline error: {e}")
            st.exception(e)

    # -- Show summary if results exist -------------------------------------
    if st.session_state.run_complete and st.session_state.scored_articles:
        scored = st.session_state.scored_articles
        n_primary = sum(1 for a in scored if a["primary_specialties"])
        n_untagged = sum(1 for a in scored if not a["primary_specialties"])

        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total articles", len(scored))
        m2.metric("Tagged (primary)", n_primary)
        m3.metric("Untagged", n_untagged)
        m4.metric("Specialties covered",
                  len({s for a in scored for s in a["primary_specialties"]}))


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Browse Feed
# ════════════════════════════════════════════════════════════════════════════
with tab_browse:
    st.header("Browse by Specialty")

    if not st.session_state.run_complete or not st.session_state.scored_articles:
        st.info("Run the pipeline first (or load existing results) in the **Run Pipeline** tab.")
    else:
        scored = st.session_state.scored_articles

        col_sel, col_opts = st.columns([2, 1])
        with col_sel:
            chosen_specialty = st.selectbox(
                "Select specialty",
                options=list(SPECIALTY_OPTIONS.keys()),
                format_func=lambda k: SPECIALTY_OPTIONS[k],
                index=0,
            )
        with col_opts:
            include_secondary = st.checkbox("Include secondary-tagged articles", value=True)
            min_score = st.slider("Minimum score", 0.0, 1.0, 0.0, 0.05,
                                  help="Filter by raw hybrid score")

        from scorer import get_feed
        feed = get_feed(scored, chosen_specialty, include_secondary, min_score)

        st.caption(
            f"**{SPECIALTY_OPTIONS[chosen_specialty]}** — "
            f"{len(feed)} articles "
            f"({sum(1 for a in feed if chosen_specialty in a['primary_specialties'])} primary, "
            f"{sum(1 for a in feed if chosen_specialty in a['secondary_specialties'])} secondary)"
        )

        if not feed:
            st.warning("No articles found for this specialty with current filters.")
        else:
            for art in feed[:50]:  # cap at 50 for performance
                score   = art.get("feed_score", 0.0)
                is_prim = chosen_specialty in art["primary_specialties"]
                tag_col = SUCCESS_COLOR if is_prim else WARNING_COLOR
                tag_lbl = "PRIMARY" if is_prim else "secondary"

                # Score bar colour
                if score >= 0.75:
                    bar_emoji = "🟢"
                elif score >= 0.60:
                    bar_emoji = "🟡"
                else:
                    bar_emoji = "🔴"

                with st.expander(
                    f"{bar_emoji} **{art['title'][:110]}{'…' if len(art['title'])>110 else ''}**"
                    f"  —  score {score:.3f}  [{tag_lbl}]"
                ):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.write(f"**{art['journal']}** | {art['pub_date']} | "
                                 f"{', '.join(art['pub_types'][:2])}")
                        if art.get("doi"):
                            st.write(f"🔗 [https://doi.org/{art['doi']}](https://doi.org/{art['doi']})")
                        if art.get("key_question"):
                            st.write(f"**Question:** {art['key_question']}")
                        if art.get("key_meaning"):
                            st.write(f"**Meaning:** {art['key_meaning']}")
                        if art.get("abstract_preview"):
                            st.write(art["abstract_preview"])

                    with c2:
                        st.write("**Specialty tags:**")
                        for sp in art["primary_specialties"][:6]:
                            st.success(SPECIALTY_OPTIONS.get(sp, sp))
                        for sp in art["secondary_specialties"][:4]:
                            st.warning(SPECIALTY_OPTIONS.get(sp, sp))

                        st.write("**Top scores:**")
                        for sp, sc in sorted(
                            art.get("scores", {}).items(),
                            key=lambda x: x[1], reverse=True
                        )[:5]:
                            pct = int(sc * 100)
                            st.progress(pct, text=f"{SPECIALTY_OPTIONS.get(sp, sp)[:20]}: {pct}%")

                        st.write("**MeSH terms:**")
                        st.caption(" · ".join(art.get("mesh_terms", [])[:8]))


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Test Scorer
# ════════════════════════════════════════════════════════════════════════════
with tab_test:
    st.header("Test Scorer")
    st.write(
        "Paste any title and abstract to see how it scores across specialties — "
        "without running the full pipeline."
    )

    # -- Sample articles ---------------------------------------------------
    SAMPLES = {
        "Empagliflozin in HFpEF (Cardiology ✅)": {
            "title": "Empagliflozin in Heart Failure with Preserved Ejection Fraction",
            "abstract": (
                "In this randomized, double-blind trial, 5988 patients with heart failure "
                "and a left ventricular ejection fraction of more than 40% were assigned "
                "to receive empagliflozin 10 mg once daily or placebo. The primary outcome "
                "was a composite of worsening heart failure or cardiovascular death. "
                "Empagliflozin led to a significantly lower rate of the composite of "
                "worsening heart failure or cardiovascular death than placebo (19.4% vs "
                "24.5%; hazard ratio, 0.79; 95% CI, 0.69 to 0.90; P<0.001). "
                "SGLT2 inhibitor therapy resulted in substantial reduction in MACE and "
                "hospitalisation for heart failure across HFpEF and HFrEF subgroups."
            ),
            "journal": "N Engl J Med",
            "pub_types": "Randomized Controlled Trial",
            "mesh": "Heart Failure, Diastolic; SGLT2 Inhibitors; Empagliflozin; Cardiovascular Diseases",
        },
        "Dupilumab in Atopic Dermatitis (Dermatology ✅)": {
            "title": "Dupilumab in Adults with Moderate-to-Severe Atopic Dermatitis",
            "abstract": (
                "Dupilumab, a monoclonal antibody targeting the IL-4 receptor alpha, was "
                "evaluated in this phase 3 randomized trial in adults with moderate-to-severe "
                "atopic dermatitis. At week 16, significantly more patients receiving "
                "dupilumab 300 mg every 2 weeks achieved an IGA score of 0 or 1 (36.1% vs "
                "8.5% with placebo) and a 75% improvement in EASI score (51.3% vs 14.7%). "
                "Adverse effects included injection-site reactions and conjunctivitis. "
                "Biologic therapy with dupilumab represents an effective treatment for "
                "refractory atopic dermatitis with clinically meaningful skin clearing."
            ),
            "journal": "NEJM",
            "pub_types": "Randomized Controlled Trial",
            "mesh": "Dermatitis, Atopic; Biological Agents; Dupilumab; Interleukin-4 Receptor alpha Subunit",
        },
        "Fetal Heart Rate Monitoring (Cardiology ❌)": {
            "title": "Electronic Fetal Heart Rate Monitoring During Labour",
            "abstract": (
                "Continuous electronic fetal heart rate monitoring was compared with "
                "intermittent auscultation in this pragmatic randomised trial of 46,000 "
                "women in labour. The primary outcome was perinatal mortality and "
                "hypoxic-ischaemic encephalopathy. Continuous monitoring did not significantly "
                "reduce the primary outcome (0.41% vs 0.40%) but was associated with higher "
                "rates of caesarean delivery (15.2% vs 11.5%)."
            ),
            "journal": "Lancet",
            "pub_types": "Randomized Controlled Trial",
            "mesh": "Fetal Heart Rate; Cardiotocography; Labor, Obstetric; Fetal Monitoring",
        },
        "Semaglutide for Obesity (Endocrinology + Cardiology)": {
            "title": "Semaglutide and Cardiovascular Outcomes in Obesity without Diabetes",
            "abstract": (
                "SELECT trial: 17,604 adults with overweight or obesity and established "
                "cardiovascular disease but without diabetes were randomized to semaglutide "
                "2.4 mg once weekly or placebo. The primary endpoint, MACE (cardiovascular "
                "death, nonfatal MI, or nonfatal stroke), occurred in 6.5% of semaglutide "
                "patients versus 8.0% of placebo patients (HR 0.80, 95% CI 0.72–0.90, P<0.001). "
                "Mean weight loss was 9.4% vs 0.9% with placebo. GLP-1 receptor agonist "
                "therapy reduced major adverse cardiovascular events independent of weight loss."
            ),
            "journal": "N Engl J Med",
            "pub_types": "Randomized Controlled Trial",
            "mesh": "Semaglutide; Obesity; Cardiovascular Diseases; Weight Loss; GLP-1 Receptor",
        },
    }

    sample_choice = st.selectbox(
        "Load a sample article", ["— custom input —"] + list(SAMPLES.keys())
    )

    if sample_choice != "— custom input —":
        s = SAMPLES[sample_choice]
        default_title    = s["title"]
        default_abstract = s["abstract"]
        default_journal  = s["journal"]
        default_pub      = s["pub_types"]
        default_mesh     = s["mesh"]
    else:
        default_title = default_abstract = default_journal = default_pub = default_mesh = ""

    col_in, col_out = st.columns([1, 1])

    with col_in:
        st.subheader("Article input")
        title    = st.text_input("Title", value=default_title)
        abstract = st.text_area("Abstract", value=default_abstract, height=220)
        journal  = st.text_input("Journal", value=default_journal)
        pub_types_str = st.text_input("Publication type(s) (comma-separated)",
                                       value=default_pub)
        mesh_str = st.text_input("MeSH terms (comma-separated)", value=default_mesh)

        score_btn = st.button("Score this article →", type="primary",
                              use_container_width=True, disabled=not title)

    with col_out:
        st.subheader("Specialty scores")

        if score_btn and title:
            from fetcher import Article as FetchArticle
            from scorer import (
                _ontology_score, _pub_type_signal, _clinical_signal,
                compute_hybrid_score,
            )
            from config import PipelineConfig
            import numpy as np

            art = FetchArticle()
            art.title       = title
            art.abstract    = abstract
            art.journal     = journal
            art.pub_types   = [p.strip() for p in pub_types_str.split(",") if p.strip()]
            art.mesh_terms  = [m.strip() for m in mesh_str.split(",") if m.strip()]
            art.journal_section = "Original Research" if art.pub_types else "Other"

            cfg = PipelineConfig()

            # Pure ontology + clinical + pub_type scores (no embeddings needed)
            component_scores = {}
            for sk, profile in SPECIALTY_PROFILES.items():
                ont  = _ontology_score(art, profile)
                pt   = _pub_type_signal(art)
                clin = _clinical_signal(art)

                # Without embeddings, estimate via ontology proxy
                # (user can run full pipeline for real embedding scores)
                emb_proxy = min(ont * 1.8, 1.0)  # rough proxy for demo

                hybrid = (
                    cfg.weight_embedding   * emb_proxy
                    + cfg.weight_ontology  * ont
                    + cfg.weight_clinical  * clin
                    + cfg.weight_pub_type  * pt
                    + cfg.weight_journal_sec * (1.0 if "Research" in art.journal_section else 0.6)
                )
                component_scores[sk] = {
                    "hybrid": round(min(hybrid, 1.0), 3),
                    "ontology": round(ont, 3),
                    "pub_type": round(pt, 3),
                    "clinical": round(clin, 3),
                }

            sorted_scores = sorted(
                component_scores.items(), key=lambda x: x[1]["hybrid"], reverse=True
            )

            # Top results
            st.write("**Top 10 specialty matches** *(embedding proxy — run full pipeline for exact scores)*")
            for sk, sc in sorted_scores[:10]:
                h = sc["hybrid"]
                name = SPECIALTY_OPTIONS[sk]
                if h >= 0.75:
                    label = "🟢 PRIMARY"
                elif h >= 0.60:
                    label = "🟡 secondary"
                else:
                    label = "⚪ low"

                st.write(f"{label}  **{name}**  —  `{h:.3f}`")
                cols = st.columns(3)
                cols[0].caption(f"ontology {sc['ontology']:.3f}")
                cols[1].caption(f"pub_type {sc['pub_type']:.3f}")
                cols[2].caption(f"clinical {sc['clinical']:.3f}")

            # Score breakdown chart
            try:
                import plotly.graph_objects as go

                top15 = sorted_scores[:15]
                names  = [SPECIALTY_OPTIONS[sk][:28] for sk, _ in top15]
                values = [sc["hybrid"] for _, sc in top15]
                colors = [
                    "#16A34A" if v >= 0.75 else
                    "#D97706" if v >= 0.60 else
                    "#D1D5DB"
                    for v in values
                ]

                fig = go.Figure(go.Bar(
                    x=values[::-1], y=names[::-1],
                    orientation="h",
                    marker_color=colors[::-1],
                ))
                fig.update_layout(
                    height=420,
                    margin=dict(l=0, r=10, t=10, b=10),
                    xaxis=dict(range=[0, 1], title="Hybrid score"),
                    yaxis=dict(tickfont=dict(size=11)),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                fig.add_vline(x=0.75, line_dash="dash", line_color="#16A34A",
                              annotation_text="primary threshold")
                fig.add_vline(x=0.60, line_dash="dot",  line_color="#D97706",
                              annotation_text="secondary threshold")
                st.plotly_chart(fig, use_container_width=True)

            except ImportError:
                st.info("Install plotly for score chart: pip install plotly")

            # Matched terms breakdown
            with st.expander("Show matched terms for top specialty"):
                top_sk = sorted_scores[0][0]
                top_profile = SPECIALTY_PROFILES[top_sk]
                all_text = (title + " " + abstract + " " + mesh_str).lower()

                matched_core = [t for t in top_profile.get("core_terms", [])
                                if t.lower() in all_text]
                matched_adj  = [t for t in top_profile.get("adjacent_terms", [])
                                if t.lower() in all_text]
                hit_excl     = [t for t in top_profile.get("exclusion_terms", [])
                                if t.lower() in all_text]

                st.write(f"**{SPECIALTY_OPTIONS[top_sk]}** — term analysis")
                if matched_core:
                    st.success(f"Core hits: {', '.join(matched_core)}")
                else:
                    st.warning("No core term hits")
                if matched_adj:
                    st.info(f"Adjacent hits: {', '.join(matched_adj)}")
                if hit_excl:
                    st.error(f"Exclusion hits: {', '.join(hit_excl)}")

            # LLM prompt preview
            with st.expander("Show LLM adjudication prompt (for top specialty)"):
                from scorer import RELEVANCE_PROMPT
                top_sk   = sorted_scores[0][0]
                top_prof = SPECIALTY_PROFILES[top_sk]
                preview  = RELEVANCE_PROMPT.format(
                    specialty_names=top_prof["name"],
                    specialty_descriptions=f"  • {top_prof['name']}: {top_prof['description'][:300]}...",
                    title=title,
                    journal=journal or "N/A",
                    pub_types=pub_types_str or "N/A",
                    abstract=abstract[:800],
                    mesh_terms=mesh_str or "N/A",
                )
                st.code(preview, language="text")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Overview
# ════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.header("Overview")

    if not st.session_state.run_complete or not st.session_state.scored_articles:
        st.info("Run the pipeline first (or load existing results) in the **Run Pipeline** tab.")
    else:
        scored = st.session_state.scored_articles
        n_total = len(scored)

        # -- Summary metrics -----------------------------------------------
        m1, m2, m3 = st.columns(3)
        m1.metric("Total articles scored", n_total)
        m2.metric("Tagged (primary specialty)", sum(1 for a in scored if a["primary_specialties"]))
        m3.metric(
            "Multi-specialty articles",
            sum(1 for a in scored if len(a["primary_specialties"]) > 1)
        )

        st.divider()

        # -- Articles per primary specialty (bar chart) --------------------
        counts: dict = {}
        for art in scored:
            for sp in art["primary_specialties"]:
                counts[sp] = counts.get(sp, 0) + 1

        if counts:
            sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            sp_names   = [SPECIALTY_OPTIONS.get(k, k) for k, _ in sorted_counts]
            sp_values  = [v for _, v in sorted_counts]

            try:
                import plotly.graph_objects as go

                fig = go.Figure(go.Bar(
                    x=sp_values[::-1], y=sp_names[::-1],
                    orientation="h",
                    marker_color=PRIMARY_COLOR,
                    text=sp_values[::-1],
                    textposition="outside",
                ))
                fig.update_layout(
                    title="Primary-tagged articles per specialty",
                    height=max(400, len(sp_names) * 22),
                    margin=dict(l=0, r=60, t=40, b=10),
                    xaxis_title="Articles",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

            except ImportError:
                for name, count in zip(sp_names, sp_values):
                    st.write(f"**{name}**: {count}")

        st.divider()

        # -- Journal breakdown ---------------------------------------------
        st.subheader("Articles by journal")
        journal_counts: dict = {}
        for art in scored:
            j = art.get("journal", "Unknown")
            journal_counts[j] = journal_counts.get(j, 0) + 1

        try:
            import plotly.express as px
            import pandas as pd

            jdf = pd.DataFrame(
                sorted(journal_counts.items(), key=lambda x: x[1], reverse=True),
                columns=["Journal", "Count"]
            )
            fig2 = px.bar(jdf, x="Journal", y="Count",
                          color_discrete_sequence=[PRIMARY_COLOR])
            fig2.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig2, use_container_width=True)

        except ImportError:
            for j, c in sorted(journal_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"**{j}**: {c}")

        st.divider()

        # -- Publication type breakdown ------------------------------------
        st.subheader("Publication type breakdown")
        pt_counts: dict = {}
        for art in scored:
            for pt in art.get("pub_types", []):
                pt_counts[pt] = pt_counts.get(pt, 0) + 1

        try:
            import plotly.express as px
            import pandas as pd

            ptdf = pd.DataFrame(
                sorted(pt_counts.items(), key=lambda x: x[1], reverse=True)[:15],
                columns=["Type", "Count"]
            )
            fig3 = px.bar(ptdf, x="Count", y="Type", orientation="h",
                          color_discrete_sequence=["#7C3AED"])
            fig3.update_layout(
                height=380,
                margin=dict(l=0, r=0, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig3, use_container_width=True)

        except ImportError:
            for pt, c in sorted(pt_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                st.write(f"**{pt}**: {c}")

        # -- Raw data table ------------------------------------------------
        st.divider()
        st.subheader("Raw results table")
        try:
            import pandas as pd
            df = pd.DataFrame([
                {
                    "Title": a["title"][:80],
                    "Journal": a["journal"],
                    "Date": a["pub_date"],
                    "Top score": round(a.get("top_score", 0), 3),
                    "Primary specialties": ", ".join(
                        SPECIALTY_OPTIONS.get(s, s) for s in a["primary_specialties"]
                    ),
                    "Secondary specialties": ", ".join(
                        SPECIALTY_OPTIONS.get(s, s) for s in a["secondary_specialties"][:3]
                    ),
                }
                for a in scored
            ])
            df = df.sort_values("Top score", ascending=False)
            st.dataframe(df, use_container_width=True, height=400)
        except ImportError:
            st.info("Install pandas for the data table: pip install pandas")
