# =============================================================
# File: pages/about.py
# =============================================================
# Modern About Page for AI News Research Assistant
# =============================================================

import streamlit as st

st.set_page_config(
    page_title="About — AI News Research Assistant",
    page_icon="📰",
    layout="wide",
)

st.markdown("""
<style>

.main-title {
    font-size: 3rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 0.3rem;
}

.sub-text {
    color: #cbd5e1;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

.feature-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 1.3rem;
    margin-bottom: 1rem;
    transition: 0.3s ease-in-out;
}

.feature-card:hover {
    border-color: #38bdf8;
    transform: translateY(-3px);
}

.feature-title {
    color: #38bdf8;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

.feature-text {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.6;
}

.section-heading {
    color: #38bdf8;
    font-size: 2rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.highlight-box {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.highlight-box p {
    color: #e2e8f0;
    line-height: 1.7;
}

.footer-text {
    text-align: center;
    color: #94a3b8;
    margin-top: 3rem;
    font-size: 0.9rem;
}

#MainMenu {visibility:hidden;}
header {visibility:hidden;}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 AI News Research Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div class="sub-text">
An intelligent AI-powered platform that transforms real-time news into
clear, concise, and actionable insights using Large Language Models (LLMs).
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">🚀 What This Platform Does</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
<p>
The AI News Research Assistant helps users quickly understand large volumes
of news content by leveraging modern LLM technology and real-time news aggregation.
Instead of manually reading multiple articles, users can enter a topic and receive
AI-generated summaries, insights, trends, and key highlights within seconds.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">✨ Key Features</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🧠 AI-Powered Summarization</div>
        <div class="feature-text">
        Generates intelligent summaries from multiple news articles
        using advanced Large Language Models.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📈 Trend Identification</div>
        <div class="feature-text">
        Detects emerging trends, recurring themes, and important
        market developments from real-time news data.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">⚡ Real-Time News Insights</div>
        <div class="feature-text">
        Fetches the latest articles instantly and converts them
        into structured business intelligence.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🌍 Multi-Source News Coverage</div>
        <div class="feature-text">
        Aggregates articles from multiple trusted news platforms
        and provides a unified AI-driven summary.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 Market & Sentiment Analysis</div>
        <div class="feature-text">
        Helps users understand market sentiment, opportunities,
        risks, and business impact from ongoing news events.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">💡 Interactive User Experience</div>
        <div class="feature-text">
        Provides a clean and intuitive interface for exploring,
        analyzing, and understanding news topics efficiently.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-heading">🎯 Who Can Use This?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
<p>

✅ Financial & Equity Research Analysts<br><br>
✅ Data Analysts & Business Intelligence Teams<br><br>
✅ Students & Researchers<br><br>
✅ Market Research Professionals<br><br>
✅ Business Strategy Teams<br><br>
✅ Anyone who wants faster understanding of current events and news trends

</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">🛠️ Powered By</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
<p>

• Streamlit for interactive web application development<br><br>
• LangChain for LLM orchestration and AI workflow management<br><br>
• Groq LLM APIs for ultra-fast inference and intelligent summarization<br><br>
• NewsAPI for real-time global news aggregation

</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-heading">🔮 Future Enhancements</div>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
<p>

• Personalized news recommendations<br><br>
• Historical trend analysis dashboards<br><br>
• AI-generated reports & PDF exports<br><br>
• Voice-enabled AI news assistant<br><br>
• Multi-language summarization support<br><br>
• Advanced sentiment visualization & analytics

</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
Built with AI, LLMs, and modern data intelligence technologies 🚀
</div>
""", unsafe_allow_html=True)