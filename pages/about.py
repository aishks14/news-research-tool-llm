# =============================================================
# File: pages/about.py
# =============================================================
# Purpose:
#   The ABOUT PAGE of the multi-page Streamlit application.
#   Explains the project architecture, tech stack, and
#   provides setup instructions for new users.
#
# Author: News Research Tool Project
# =============================================================

import streamlit as st

st.set_page_config(
    page_title="About — News Research Tool",
    page_icon="ℹ️",
    layout="wide",
)

st.markdown("""
<style>
    .info-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .info-card h3 { color: #38bdf8; margin-top: 0; }
    .info-card p, .info-card li { color: #cbd5e1; font-size: 0.92rem; }
    .phase-badge {
        display: inline-block;
        background: #0c4a6e;
        color: #38bdf8;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    #MainMenu { visibility: hidden; }
    header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# Header
# =============================================================

st.title("ℹ️ About This Project")
st.markdown(
    "An end-to-end AI news research assistant for equity analysts, "
    "built with LangChain, Groq (LLaMA 3), NewsAPI, and Streamlit."
)
st.markdown("---")

# =============================================================
# Architecture Diagram (text-based)
# =============================================================

st.markdown("### 🏗️ System Architecture")
st.code("""
User Query (Streamlit)
        │
        ▼
┌───────────────────┐
│   app.py          │  ← Front-end: Streamlit web interface
│   (UI layer)      │
└────────┬──────────┘
         │ calls
         ▼
┌───────────────────┐
│ langchain_config  │  ← Intelligence layer: LangChain pipeline
│   (logic layer)   │
└──┬─────────────┬──┘
   │             │
   ▼             ▼
┌──────────┐  ┌──────────────────┐
│ NewsAPI  │  │   Groq LLM       │
│ Articles │  │   (LLaMA 3)      │
└──────────┘  └──────────────────┘
   │                │
   └────────┬───────┘
            ▼
      AI Summary → Streamlit UI → User
""", language="")

st.markdown("---")

# =============================================================
# Tech Stack
# =============================================================

st.markdown("### 🛠️ Tech Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🔗 LangChain</h3>
        <p>
        The orchestration framework that connects the LLM to the
        prompt templates and data pipeline. Provides the
        <code>LLMChain</code>, <code>PromptTemplate</code>,
        and model abstractions used throughout the project.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>🗞️ NewsAPI</h3>
        <p>
        Real-time news aggregation API covering 80,000+ news sources
        worldwide. Returns article titles, descriptions, URLs, and
        publication dates filtered by query, language, and relevance.
        Free tier: 100 requests/day.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3>⚡ Groq + LLaMA 3</h3>
        <p>
        Groq provides a free API to run Meta's LLaMA 3 models on
        custom LPU (Language Processing Unit) hardware — delivering
        speeds 10-100× faster than standard GPU inference.
        <br><br>
        <strong>Replaces OpenAI</strong> in this project. Identical
        LangChain interface, zero cost, no rate-limit concerns for
        typical usage.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>🌐 Streamlit</h3>
        <p>
        Python-native web framework that converts Python scripts into
        interactive web apps. No HTML/CSS/JavaScript required.
        Handles session state, UI components, file downloads,
        and multi-page navigation automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =============================================================
# Setup Instructions
# =============================================================

st.markdown("### 🚀 Setup Instructions")

st.markdown("""
<div class="info-card">
    <span class="phase-badge">PHASE 1</span>
    <h3>Install Dependencies</h3>
    <pre style="background:#0f172a;padding:0.8rem;border-radius:6px;color:#38bdf8;">
pip install -r requirements.txt</pre>
</div>

<div class="info-card">
    <span class="phase-badge">PHASE 2</span>
    <h3>Get Your API Keys</h3>
    <ul>
        <li><strong>Groq API Key</strong> → 
            <a href="https://console.groq.com" target="_blank" style="color:#38bdf8;">
            console.groq.com</a> — Free, no credit card required</li>
        <li><strong>NewsAPI Key</strong> → 
            <a href="https://newsapi.org/register" target="_blank" style="color:#38bdf8;">
            newsapi.org/register</a> — Free tier: 100 req/day</li>
    </ul>
</div>

<div class="info-card">
    <span class="phase-badge">PHASE 3</span>
    <h3>Configure .env File</h3>
    <pre style="background:#0f172a;padding:0.8rem;border-radius:6px;color:#38bdf8;">
GROQ_API_KEY=your_groq_key_here
NEWS_API_KEY=your_newsapi_key_here</pre>
</div>

<div class="info-card">
    <span class="phase-badge">PHASE 4</span>
    <h3>Run the App</h3>
    <pre style="background:#0f172a;padding:0.8rem;border-radius:6px;color:#38bdf8;">
streamlit run app.py</pre>
    <p>Opens at <strong>http://localhost:8501</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# =============================================================
# Project Files Summary
# =============================================================

st.markdown("### 📁 Project File Summary")

files = [
    ("app.py",                "Main Streamlit UI — query input, summary display, article cards"),
    ("langchain_config.py",   "Core logic — LLM init, NewsAPI calls, LangChain pipeline"),
    ("utils.py",              "Utility functions — date formatting, validation, download builder"),
    ("pages/history.py",      "Streamlit page — past query history with download option"),
    ("pages/about.py",        "Streamlit page — project info, architecture, setup guide"),
    (".env",                  "API keys — NEVER commit this file to version control"),
    ("requirements.txt",      "Python package dependencies — install with pip"),
    ("README.md",             "Full project documentation and getting-started guide"),
<<<<<<< HEAD
]
=======
)
>>>>>>> 0169455050506155d34542ba676f2b1b42b8988f

for fname, desc in files:
    st.markdown(
        f"- **`{fname}`** — {desc}"
    )