# =============================================================
# File: utils.py
# =============================================================
# Purpose:
#   This module contains standalone UTILITY FUNCTIONS used
#   across the project. Keeping these separate from langchain_config.py
#   and app.py follows the "separation of concerns" principle:
#   each file has one clear job.
#
# Functions in this file:
#   - format_published_date()  → Clean date string formatting
#   - truncate_text()          → Safely truncate long strings
#   - build_download_content() → Format summary for .txt export
#   - validate_query()         → Check user input before API call
#   - get_source_domain()      → Extract domain from article URL
#   - count_words()            → Word count helper
#
# Author: News Research Tool Project
# =============================================================

# ── Standard Library ──────────────────────────────────────────
import re
from datetime import datetime
from urllib.parse import urlparse


# =============================================================
# FUNCTION 1 — Date Formatter
# =============================================================

def format_published_date(iso_date: str) -> str:
    """
    Convert an ISO 8601 datetime string into a readable date.

    NewsAPI returns dates like: "2024-03-15T10:30:00Z"
    This function converts them to: "15 Mar 2024"

    Parameters
    ----------
    iso_date : str
        ISO 8601 formatted date string from NewsAPI

    Returns
    -------
    str
        Human-readable date string, e.g. "15 Mar 2024"
        Returns the original string if parsing fails.

    Examples
    --------
    >>> format_published_date("2024-03-15T10:30:00Z")
    '15 Mar 2024'
    >>> format_published_date("")
    'Unknown date'
    """
    if not iso_date:
        return "Unknown date"
    try:
        dt = datetime.strptime(iso_date[:19], "%Y-%m-%dT%H:%M:%S")
        return dt.strftime("%d %b %Y")
    except ValueError:
        return iso_date[:10]  # Fallback to raw YYYY-MM-DD


# =============================================================
# FUNCTION 2 — Text Truncator
# =============================================================

def truncate_text(text: str, max_chars: int = 200, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum character length.

    Used to prevent excessively long article descriptions
    from overflowing the UI card layout.

    Parameters
    ----------
    text : str
        The input string to truncate.
    max_chars : int
        Maximum number of characters to keep (default: 200).
    suffix : str
        String appended when truncation occurs (default: "...").

    Returns
    -------
    str
        Truncated string with suffix if shortened, or the original
        string unchanged if it is within the limit.

    Examples
    --------
    >>> truncate_text("Hello world", max_chars=5)
    'Hello...'
    >>> truncate_text("Short", max_chars=100)
    'Short'
    """
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    # Truncate at the last space before the limit (avoid mid-word cuts)
    truncated = text[:max_chars].rsplit(" ", 1)[0]
    return truncated + suffix


# =============================================================
# FUNCTION 3 — Download Content Builder
# =============================================================

def build_download_content(query: str, model: str, summary: str,
                            articles: list) -> str:
    """
    Build a formatted plain-text string for the download button.

    Creates a clean, structured .txt file that the user can save
    for their records, including the query, model used, AI summary,
    and a list of all source articles.

    Parameters
    ----------
    query : str
        The original user query.
    model : str
        The Groq model name used (e.g. "llama3-8b-8192").
    summary : str
        The AI-generated summary text.
    articles : list
        List of raw article dicts from NewsAPI.

    Returns
    -------
    str
        A formatted multi-section plain-text string.
    """
    divider  = "=" * 70
    divider2 = "-" * 70
    now      = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        divider,
        "EQUITY NEWS RESEARCH TOOL — EXPORTED SUMMARY",
        divider,
        f"Query    : {query}",
        f"Model    : {model}",
        f"Exported : {now}",
        divider,
        "",
        "AI-GENERATED SUMMARY",
        divider2,
        summary,
        "",
        divider,
        "SOURCE ARTICLES",
        divider2,
    ]

    for i, art in enumerate(articles, start=1):
        title   = art.get("title", "No title")
        source  = art.get("source", {}).get("name", "Unknown")
        date    = format_published_date(art.get("publishedAt", ""))
        url     = art.get("url", "")
        desc    = art.get("description", "No description")

        if desc and desc.lower() != "[removed]":
            lines += [
                f"\n[{i}] {title}",
                f"    Source : {source}",
                f"    Date   : {date}",
                f"    Link   : {url}",
                f"    Desc   : {truncate_text(desc, 300)}",
            ]

    lines += ["", divider, "End of report", divider]
    return "\n".join(lines)


# =============================================================
# FUNCTION 4 — Query Validator
# =============================================================

def validate_query(query: str) -> tuple:
    """
    Validate the user's search query before making any API calls.

    Checks:
    - Query is not empty
    - Query is at least 3 characters long
    - Query is not more than 200 characters
    - Query contains at least one alphabetic character

    Parameters
    ----------
    query : str
        The raw query string from the Streamlit text input.

    Returns
    -------
    tuple : (is_valid: bool, error_message: str)
        is_valid      → True if the query passes all checks
        error_message → Empty string if valid, reason if invalid

    Examples
    --------
    >>> validate_query("Apple earnings")
    (True, '')
    >>> validate_query("")
    (False, 'Query cannot be empty.')
    >>> validate_query("ab")
    (False, 'Query must be at least 3 characters.')
    """
    query = query.strip()

    if not query:
        return False, "Query cannot be empty. Please enter a topic to research."

    if len(query) < 3:
        return False, "Query must be at least 3 characters long."

    if len(query) > 200:
        return False, "Query is too long. Please keep it under 200 characters."

    if not re.search(r"[a-zA-Z]", query):
        return False, "Query must contain at least one letter."

    return True, ""


# =============================================================
# FUNCTION 5 — Domain Extractor
# =============================================================

def get_source_domain(url: str) -> str:
    """
    Extract the root domain name from a full URL.

    Used to show a clean source label (e.g. "reuters.com")
    instead of the full URL in the UI.

    Parameters
    ----------
    url : str
        Full URL string, e.g. "https://www.reuters.com/article/..."

    Returns
    -------
    str
        Root domain, e.g. "reuters.com"
        Returns "unknown" if parsing fails.

    Examples
    --------
    >>> get_source_domain("https://www.reuters.com/article/123")
    'reuters.com'
    >>> get_source_domain("https://techcrunch.com/2024/01/story")
    'techcrunch.com'
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        # Remove "www." prefix if present
        if domain.startswith("www."):
            domain = domain[4:]
        return domain if domain else "unknown"
    except Exception:
        return "unknown"


# =============================================================
# FUNCTION 6 — Word Counter
# =============================================================

def count_words(text: str) -> int:
    """
    Count the number of words in a string.

    Used to display a word count for the AI-generated summary
    so users know how comprehensive it is.

    Parameters
    ----------
    text : str
        Any string to count words in.

    Returns
    -------
    int
        Number of words (split on whitespace).
        Returns 0 for empty or None input.

    Examples
    --------
    >>> count_words("Hello world this is a test")
    6
    >>> count_words("")
    0
    """
    if not text:
        return 0
    return len(text.split())