# =============================================================
# File: pages/history.py
# =============================================================
# Purpose:
#   This is the QUERY HISTORY PAGE of the Streamlit multi-page app.
#   Streamlit automatically creates navigation links for any .py
#   file placed inside a "pages/" folder.
#
# What this file does:
#   1. Reads the session-state history of past queries and summaries
#   2. Displays them in a clean, expandable card layout
#   3. Allows the user to download any past summary as a .txt file
#   4. Provides a button to clear all history
#
# Note on session state:
#   Streamlit's st.session_state is an in-memory dictionary that
#   persists across page interactions within the same browser tab,
#   but is cleared when the tab is refreshed or closed.
#
# Author: News Research Tool Project
# =============================================================

import streamlit as st
from utils import build_download_content

# =============================================================
# Page Config
# =============================================================

st.set_page_config(
    page_title="Search History — News Research Tool",
    page_icon="🕐",
    layout="wide",
)

# =============================================================
# Custom CSS (matches main app styling)
# =============================================================

st.markdown("""
<style>
    .history-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-left: 4px solid #38bdf8;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .history-card h4 { color: #38bdf8; margin: 0 0 0.3rem; font-size: 1rem; }
    .history-card p  { color: #94a3b8; font-size: 0.85rem; margin: 0.2rem 0; }
    #MainMenu { visibility: hidden; }
    header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# Header
# =============================================================

st.title("🕐 Search History")
st.markdown(
    "All queries from your current session are stored here. "
    "History is cleared when you close or refresh the browser tab."
)
st.markdown("---")

# =============================================================
# History Display
# =============================================================

# Retrieve history from session state (set by app.py)
history = st.session_state.get("search_history", [])

if not history:
    st.info(
        "📭 No search history yet.\n\n"
        "Go back to the main page and run a query to see it appear here."
    )
else:
    st.markdown(f"**{len(history)} search(es) this session:**")

    # ── Clear all button ──────────────────────────────────────
    if st.button("🗑️  Clear All History", type="secondary"):
        st.session_state["search_history"] = []
        st.success("✅ History cleared.")
        st.rerun()

    st.markdown("---")

    # ── Render each history entry ─────────────────────────────
    for i, entry in enumerate(reversed(history), start=1):
        query   = entry.get("query", "Unknown query")
        model   = entry.get("model", "Unknown model")
        summary = entry.get("summary", "")
        articles = entry.get("articles", [])
        timestamp = entry.get("timestamp", "")
        n_articles = entry.get("n_articles", 0)

        with st.expander(f"#{i}  —  {query}  ({timestamp})", expanded=(i == 1)):
            col_l, col_r = st.columns([3, 1])
            with col_l:
                st.markdown(f"**Query:** `{query}`")
                st.markdown(f"**Model:** `{model}`  |  **Articles:** {n_articles}")
            with col_r:
                if summary and articles:
                    dl_content = build_download_content(
                        query=query, model=model,
                        summary=summary, articles=articles
                    )
                    st.download_button(
                        label="⬇️ Download",
                        data=dl_content,
                        file_name=f"summary_{query[:20].replace(' ','_')}.txt",
                        mime="text/plain",
                        key=f"dl_{i}"
                    )

            st.markdown("**Summary:**")
            st.markdown(
                f'<div style="background:#0f172a;border:1px solid #334155;'
                f'border-radius:8px;padding:1rem;color:#e2e8f0;font-size:0.9rem;'
                f'line-height:1.7;">{summary}</div>',
                unsafe_allow_html=True
            )