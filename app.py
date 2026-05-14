# =============================================================
# File: app.py
# =============================================================
# Purpose:
#   This is the FRONT-END / USER INTERFACE of the News Research Tool.
#   It is built entirely with Streamlit — a Python library that
#   converts Python scripts into fully interactive web applications
#   without writing any HTML, CSS, or JavaScript.
#
# What this file does:
#   1. Renders the web page with title, sidebar, and inputs
#   2. Accepts the user's query and settings
#   3. Calls langchain_config.py to fetch news + run the LLM
#   4. Displays the AI-generated summary in a structured layout
#   5. Shows the individual source articles for transparency
#
# How to run:
#   streamlit run app.py
#   → Opens automatically at http://localhost:8501
#
# Author: News Research Tool Project
# =============================================================

# ── Standard Library ──────────────────────────────────────────
import time
import logging

# ── Third-Party ───────────────────────────────────────────────
import streamlit as st

# ── Local Modules ─────────────────────────────────────────────
# We import only what app.py needs from langchain_config.py:
#   llm_chain  → the LangChain pipeline (prompt + Groq LLM)
#   get_summary → fetches news + extracts text in one call
from langchain_config import llm_chain, get_summary

# =============================================================
# SECTION 1 — Page Configuration
# =============================================================
# st.set_page_config() MUST be the very first Streamlit call.
# It controls the browser tab title, icon, and layout mode.
# =============================================================

st.set_page_config(
    page_title="Equity News Research Tool",
    page_icon="📰",
    layout="wide",          # Use full browser width
    initial_sidebar_state="expanded",
)

# =============================================================
# SECTION 2 — Custom CSS Styling
# =============================================================
# Streamlit allows injecting raw CSS via st.markdown with
# unsafe_allow_html=True. We use this to polish the UI beyond
# the default Streamlit theme.
# =============================================================

st.markdown("""
<style>
    /* Main background and font */
    .main { background-color: #0f172a; }

    /* Summary card styling */
    .summary-box {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        border-radius: 10px;
        padding: 1.5rem 2rem;
        margin: 1rem 0;
        color: #e2e8f0;
        font-size: 0.97rem;
        line-height: 1.75;
    }

    /* Individual article card */
    .article-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s;
    }
    .article-card:hover { border-color: #38bdf8; }
    .article-card h4 { color: #38bdf8; margin: 0 0 0.3rem 0; font-size: 0.95rem; }
    .article-card p  { color: #94a3b8; font-size: 0.85rem; margin: 0; }
    .article-card a  { color: #38bdf8; text-decoration: none; font-size: 0.82rem; }

    /* Metric card */
    .metric-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        text-align: center;
    }
    .metric-val   { font-size: 1.6rem; font-weight: 700; color: #38bdf8; }
    .metric-label { font-size: 0.8rem;  color: #64748b; margin-top: 2px; }

    /* Section heading */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f1f5f9;
        border-bottom: 2px solid #334155;
        padding-bottom: 0.4rem;
        margin: 1.5rem 0 0.8rem;
    }

    /* Badge tag */
    .badge {
        display: inline-block;
        background: #0c4a6e;
        color: #38bdf8;
        border: 1px solid #38bdf8;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.75rem;
        margin: 2px;
    }

    /* Info box */
    .info-box {
        background: #0c1a2e;
        border: 1px solid #1d4ed8;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #93c5fd;
        font-size: 0.88rem;
    }

    /* Hide default Streamlit header */
    #MainMenu { visibility: hidden; }
    header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# SECTION 3 — Sidebar
# =============================================================
# The sidebar contains settings and project information.
# Users can adjust behaviour without cluttering the main page.
# =============================================================

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    # Number of articles to fetch
    max_articles = st.slider(
        "📄 Max Articles to Fetch",
        min_value=3,
        max_value=20,
        value=10,
        step=1,
        help="More articles give richer context but take longer to process."
    )

    # Model selector (all free on Groq)
    model_choice = st.selectbox(
        "🤖 Groq Model",
        options=[
            "llama3-8b-8192",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
        ],
        index=0,
        help=(
            "llama3-8b → Fast & efficient\n"
            "llama3-70b → More powerful\n"
            "mixtral → Large context window"
        )
    )

    # Show raw articles toggle
    show_articles = st.toggle(
        "📰 Show Source Articles",
        value=True,
        help="Display the individual news articles used to generate the summary."
    )

    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    This tool uses:
    - 🗞️ **NewsAPI** — real-time news
    - 🦙 **Groq + LLaMA 3** — AI summarisation
    - 🔗 **LangChain** — LLM orchestration
    - 🌐 **Streamlit** — web interface
    """)

    st.markdown("---")
    st.markdown("### 🔑 API Keys Needed")
    st.markdown("""
    Add to your `.env` file:
    ```
    GROQ_API_KEY=...
    NEWS_API_KEY=...
    ```
    - [Get Groq key →](https://console.groq.com)
    - [Get NewsAPI key →](https://newsapi.org)
    """)

# =============================================================
# SECTION 4 — Main Header
# =============================================================

st.markdown("""
<div style="text-align:center; padding: 1.5rem 0 0.5rem;">
    <h1 style="font-size:2.4rem; font-weight:800; color:#f1f5f9; margin:0;">
        📰 Equity News Research Tool
    </h1>
    <p style="color:#64748b; font-size:1rem; margin-top:0.4rem;">
        Powered by Groq · LLaMA 3 · LangChain · NewsAPI
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tech stack badges ──────────────────────────────────────────
cols_badges = st.columns([1, 6, 1])
with cols_badges[1]:
    st.markdown("""
    <div style="text-align:center; margin-bottom:1rem;">
        <span class="badge">🦙 LLaMA 3</span>
        <span class="badge">⚡ Groq</span>
        <span class="badge">🔗 LangChain</span>
        <span class="badge">🗞️ NewsAPI</span>
        <span class="badge">🌐 Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================
# SECTION 5 — Query Input
# =============================================================

st.markdown("### 🔍 Enter Your Research Query")
st.markdown(
    "Type any topic, company, sector, or event. "
    "The tool will fetch the latest news and generate an AI-powered summary."
)

# Example queries as clickable chips
st.markdown("**💡 Try these examples:**")
example_cols = st.columns(4)
examples = [
    "Apple iPhone sales 2024",
    "Federal Reserve interest rates",
    "NVIDIA AI chip demand",
    "Oil prices OPEC",
]
example_query = None
for i, ex in enumerate(examples):
    with example_cols[i]:
        if st.button(f"📌 {ex}", use_container_width=True):
            example_query = ex

# Main query input
query_input = st.text_input(
    label="Research Query",
    value=example_query if example_query else "",
    placeholder="e.g. Tesla earnings Q4 2024, Apple stock, Bitcoin rally...",
    label_visibility="collapsed",
)

# Search button
col_btn_l, col_btn, col_btn_r = st.columns([3, 2, 3])
with col_btn:
    search_clicked = st.button(
        "🔎 Get AI Summary",
        type="primary",
        use_container_width=True,
    )

# =============================================================
# SECTION 6 — Info Box (shown before any search)
# =============================================================

if not search_clicked and not example_query:
    st.markdown("""
    <div class="info-box" style="margin-top:1.5rem;">
        <strong>ℹ️ How it works:</strong><br><br>
        1️⃣  Enter a topic, company name, or market event above<br>
        2️⃣  Click <strong>Get AI Summary</strong><br>
        3️⃣  The tool fetches the latest news articles from NewsAPI<br>
        4️⃣  LangChain sends them to the Groq LLM (LLaMA 3)<br>
        5️⃣  You receive a structured, analyst-ready summary in seconds
    </div>
    """, unsafe_allow_html=True)

# =============================================================
# SECTION 7 — Core Logic: Fetch News + Generate Summary
# =============================================================

if search_clicked or example_query:
    query = query_input.strip() if query_input.strip() else (example_query or "")

    if not query:
        st.warning("⚠️  Please enter a query before clicking Search.")
    else:
        # ── Step 1: Fetch news articles ────────────────────────
        with st.spinner("📰 Fetching latest news articles..."):
            try:
                summaries_text, articles = get_summary(
                    query=query,
                    max_articles=max_articles
                )
                news_fetched = True
            except Exception as e:
                st.error(f"❌ Failed to fetch news: {str(e)}")
                news_fetched = False

        if news_fetched:
            # ── Step 2: Show quick stats ───────────────────────
            usable = [
                a for a in articles
                if a.get("description")
                and a["description"].lower() != "[removed]"
            ]
            sources = list({a["source"]["name"] for a in usable})

            st.markdown("---")
            st.markdown('<div class="section-header">📊 Research Overview</div>',
                        unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{len(articles)}</div>
                    <div class="metric-label">Articles Fetched</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{len(usable)}</div>
                    <div class="metric-label">Usable Articles</div>
                </div>""", unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{len(sources)}</div>
                    <div class="metric-label">News Sources</div>
                </div>""", unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-val">{model_choice.split("-")[0].upper()}</div>
                    <div class="metric-label">Model Used</div>
                </div>""", unsafe_allow_html=True)

            # ── Step 3: Run LLM summarisation ─────────────────
            st.markdown("---")
            st.markdown('<div class="section-header">🤖 AI-Generated Research Summary</div>',
                        unsafe_allow_html=True)

            with st.spinner("🦙 LLaMA 3 is analysing the articles..."):
                try:
                    t_start = time.time()

                    # Update the model in the chain if user changed it
                    llm_chain.llm.model_name = model_choice

                    # Run the LangChain pipeline
                    result = llm_chain.run({
                        "query":     query,
                        "summaries": summaries_text
                    })

                    t_elapsed = round(time.time() - t_start, 1)
                    llm_success = True

                except Exception as e:
                    st.error(f"❌ LLM error: {str(e)}")
                    llm_success = False

            if llm_success:
                # ── Display the summary ────────────────────────
                st.markdown(
                    f'<div class="summary-box">{result}</div>',
                    unsafe_allow_html=True
                )

                # Time and model info
                st.caption(
                    f"⏱️ Generated in {t_elapsed}s  ·  "
                    f"Model: {model_choice}  ·  "
                    f"Query: '{query}'"
                )

                # Download button
                st.download_button(
                    label="⬇️  Download Summary as .txt",
                    data=f"Query: {query}\n\nModel: {model_choice}\n\n"
                         f"{'='*60}\n\n{result}",
                    file_name=f"summary_{query[:30].replace(' ','_')}.txt",
                    mime="text/plain",
                )

            # ── Step 4: Show source articles ───────────────────
            if show_articles:
                st.markdown("---")
                st.markdown('<div class="section-header">📰 Source Articles</div>',
                            unsafe_allow_html=True)
                st.caption(
                    f"These are the {len(usable)} articles used to generate the summary above."
                )

                for i, article in enumerate(articles, start=1):
                    title       = article.get("title", "No title")
                    description = article.get("description", "")
                    url         = article.get("url", "#")
                    source_name = article.get("source", {}).get("name", "Unknown")
                    published   = article.get("publishedAt", "")[:10]

                    if not description or description.lower() == "[removed]":
                        continue

                    st.markdown(f"""
                    <div class="article-card">
                        <h4>#{i} — {title}</h4>
                        <p>{description}</p>
                        <p style="margin-top:0.4rem;">
                            📡 <strong>{source_name}</strong> &nbsp;|&nbsp;
                            📅 {published} &nbsp;|&nbsp;
                            <a href="{url}" target="_blank">Read full article →</a>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

# =============================================================
# SECTION 8 — Footer
# =============================================================

st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.8rem; padding:0.5rem 0 1rem;">
    📰 Equity News Research Tool &nbsp;·&nbsp;
    Built with LangChain + Groq + NewsAPI + Streamlit &nbsp;·&nbsp;
    OpenAI-free · Fully local-compatible
</div>
""", unsafe_allow_html=True)