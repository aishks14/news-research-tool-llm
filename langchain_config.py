# =============================================================
# File: langchain_config.py
# =============================================================
# Purpose:
#   This is the CORE INTELLIGENCE LAYER of the News Research Tool.
#   It handles three responsibilities:
#     1. Connects to the Groq LLM via LangChain
#     2. Fetches real-time news articles from NewsAPI
#     3. Builds the prompt pipeline that produces AI summaries
#
# Architecture:
#   NewsAPI → raw articles → text extraction → LangChain Prompt
#   → Groq LLM (LLaMA 3) → AI-generated summary
#
# Replacement Note:
#   OpenAI (as described in the project spec) has been replaced
#   with Groq's free API running LLaMA 3. The LangChain interface
#   is identical — only the model class changes.
#
# Author: News Research Tool Project
# =============================================================

# ── Standard Library ──────────────────────────────────────────
import os
import logging

# ── Third-Party ───────────────────────────────────────────────
from dotenv import load_dotenv
from newsapi import NewsApiClient
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

# =============================================================
# SECTION 1 — Environment & Logging Setup
# =============================================================

# Load API keys from .env file into environment variables
load_dotenv()

# Configure logger so all events are printed clearly to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Read keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY  = os.getenv("NEWS_API_KEY")

# Validate that both keys are present before anything else runs
if not GROQ_API_KEY:
    raise EnvironmentError(
        "❌  GROQ_API_KEY not found in .env file.\n"
        "    → Get a free key at https://console.groq.com\n"
        "    → Add it to your .env file as: GROQ_API_KEY=your_key_here"
    )

if not NEWS_API_KEY:
    raise EnvironmentError(
        "❌  NEWS_API_KEY not found in .env file.\n"
        "    → Get a free key at https://newsapi.org/register\n"
        "    → Add it to your .env file as: NEWS_API_KEY=your_key_here"
    )

logger.info("✅ Environment variables loaded successfully")

# =============================================================
# SECTION 2 — Groq LLM Initialisation (OpenAI Replacement)
# =============================================================
# We use Groq's free API instead of OpenAI.
# Groq runs the LLaMA 3 (8B) model on custom LPU hardware,
# making it significantly faster and completely free to use.
#
# Model options you can swap in:
#   - "llama3-8b-8192"     → Fast, great for summarisation
#   - "llama3-70b-8192"    → More powerful, slightly slower
#   - "mixtral-8x7b-32768" → Large context window (32K tokens)
# =============================================================

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0.3,       # Lower = more factual, less creative
    max_tokens=1024,       # Maximum tokens in the response
)

logger.info("✅ Groq LLM (LLaMA 3 8B) initialised")

# =============================================================
# SECTION 3 — Prompt Template
# =============================================================
# A PromptTemplate defines the exact instructions sent to the LLM.
# The {query} and {summaries} placeholders are filled in at
# runtime when llm_chain.run() is called.
#
# Good prompts give the model:
#   - A clear ROLE ("You are an equity research analyst...")
#   - Clear CONTEXT (the actual news summaries)
#   - A clear INSTRUCTION (what you want it to produce)
# =============================================================

PROMPT_TEMPLATE = """
You are an expert equity research analyst AI assistant.

A user has asked about the following topic:
Query: {query}

Below are summaries extracted from the most recent and relevant 
news articles on this topic:

--- NEWS SUMMARIES START ---
{summaries}
--- NEWS SUMMARIES END ---

Your task:
1. Read all the news summaries carefully.
2. Identify the key themes, trends, and important facts.
3. Write a clear, concise, and well-structured overall summary 
   (4-6 paragraphs) that a financial analyst could use directly 
   in their research.
4. Highlight any significant risks, opportunities, or market 
   movements mentioned.
5. End with a short "Key Takeaways" bullet list (3-5 bullets).

Do NOT include any information not present in the provided summaries.
Write in a professional, analytical tone.
"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["query", "summaries"]
)

logger.info("✅ Prompt template configured")

# =============================================================
# SECTION 4 — LLMChain
# =============================================================
# LLMChain combines the prompt template and the LLM into a
# single callable pipeline:
#
#   llm_chain.run({"query": "...", "summaries": "..."})
#       → fills the prompt template
#       → sends it to Groq LLM
#       → returns the AI-generated text response
# =============================================================

llm_chain = LLMChain(prompt=prompt, llm=llm)

logger.info("✅ LLMChain pipeline created")

# =============================================================
# SECTION 5 — NewsAPI Functions
# =============================================================

# Initialise the NewsAPI client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)


def get_news_articles(query: str, max_articles: int = 10) -> list:
    """
    Fetch the most relevant recent news articles for a given query.

    Parameters
    ----------
    query : str
        The search term (e.g. "Tesla Q4 earnings", "Apple stock")
    max_articles : int
        Maximum number of articles to retrieve (default: 10)

    Returns
    -------
    list
        A list of article dicts from NewsAPI. Each dict contains:
        - title       : Headline of the article
        - description : Short summary/snippet of the article
        - url         : Link to the full article
        - source      : Dict with 'name' of the news source
        - publishedAt : ISO timestamp of when it was published

    Raises
    ------
    Exception
        If the NewsAPI call fails (network error, bad key, etc.)
    """
    logger.info(f"📰 Fetching news for query: '{query}'")

    try:
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",     # Sort by most relevant first
            page_size=max_articles,  # Limit results
        )
        articles = response.get("articles", [])
        logger.info(f"✅ Retrieved {len(articles)} articles")
        return articles

    except Exception as e:
        logger.error(f"❌ NewsAPI error: {e}")
        raise


def extract_article_texts(articles: list) -> list:
    """
    Extract clean text content from a list of raw article dicts.

    Each article dict from NewsAPI may have the fields:
      - title       : The article headline
      - description : A short snippet (usually 1-2 sentences)

    We combine title + description for each article to give the
    LLM more context than just the snippet alone.

    Parameters
    ----------
    articles : list
        Raw list of article dicts returned by get_news_articles()

    Returns
    -------
    list
        List of clean strings, one per article.
        Articles with no usable text are skipped.
    """
    texts = []
    for i, article in enumerate(articles, start=1):
        title       = article.get("title", "").strip()
        description = article.get("description", "").strip()
        source_name = article.get("source", {}).get("name", "Unknown")
        published   = article.get("publishedAt", "")[:10]  # Date only

        # Only include articles that have at least a description
        if description and description.lower() != "[removed]":
            text = (
                f"[Article {i} | Source: {source_name} | Date: {published}]\n"
                f"Headline: {title}\n"
                f"Summary: {description}"
            )
            texts.append(text)

    logger.info(f"✅ Extracted text from {len(texts)} usable articles")
    return texts


def build_summaries_text(article_texts: list) -> str:
    """
    Join individual article texts into one combined string.

    The LLM receives all article content as a single block of text.
    Articles are separated by a divider line for readability.

    Parameters
    ----------
    article_texts : list
        List of formatted article strings from extract_article_texts()

    Returns
    -------
    str
        A single combined string ready to be inserted into the prompt.
        Returns a fallback message if no texts are available.
    """
    if not article_texts:
        return "No relevant news articles were found for this query."

    return "\n\n" + ("\n" + "-" * 60 + "\n").join(article_texts)


def get_summary(query: str, max_articles: int = 10) -> tuple:
    """
    Master orchestrator function: fetch news → extract text → combine.

    This is the single function called by app.py. It handles the
    entire data pipeline from raw query to structured text ready
    for the LLM.

    Parameters
    ----------
    query : str
        The user's search query from the Streamlit input box.
    max_articles : int
        Maximum articles to fetch (default: 10).

    Returns
    -------
    tuple : (summaries_text: str, articles: list)
        summaries_text → Combined text block sent to the LLM
        articles       → Raw article list used to show source links
    """
    articles      = get_news_articles(query, max_articles)
    article_texts = extract_article_texts(articles)
    summaries     = build_summaries_text(article_texts)
    return summaries, articles