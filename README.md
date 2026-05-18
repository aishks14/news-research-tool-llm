# 📰 News Research Tool — Complete Project Index

## **🎯 What This Project Does**

An end-to-end LLM application that:
1. Accepts a user query about a company, event, or market topic
2. Fetches real-time news articles via **NewsAPI**
3. Sends articles to **Groq's free LLM** (LLaMA 3) via **LangChain**
4. Generates a professional research summary in seconds
5. Delivers results through a beautiful **Streamlit** web interface

**Replaces OpenAI:** Uses Groq's free API instead of OpenAI's paid models. Identical interface, no cost, extremely fast.

---

## ** File Structure & Descriptions**

### **Root Files**

```
news_research_tool/
```

#### **1. `app.py`** (16 KB | 450+ lines)
**The Front-End / User Interface**

- **What it does:** Builds and runs the Streamlit web application
- **Key responsibilities:**
  - Renders the web UI with title, input box, settings sidebar
  - Accepts user queries and settings
  - Calls `langchain_config.py` to fetch news + run the LLM
  - Displays results with HTML/CSS styling
  - Provides download button for summaries
  - Shows individual source articles
  
- **Streamlit Components Used:**
  - `st.text_input()` — query input box
  - `st.slider()` — max articles setting
  - `st.selectbox()` — model selection
  - `st.button()` — search trigger
  - `st.spinner()` — loading indicator
  - `st.markdown(..., unsafe_allow_html=True)` — custom CSS
  - `st.session_state` — stores query history
  - `st.download_button()` — .txt export
  - `st.columns()` — multi-column layouts
  
- **Custom Features:**
  - Dark theme with teal/blue accent colors
  - Metric cards showing stats (articles fetched, sources, model)
  - Expandable article cards showing sources and links
  - Example query chips for quick demos
  - Session-based search history
  - Model selection between llama3-8b, llama3-70b, mixtral

---

#### **2. `langchain_config.py`** (10 KB | 300+ lines)
**The Core Intelligence Layer**

- **What it does:** Orchestrates the LLM pipeline and news fetching
- **Key responsibilities:**
  - Initializes **Groq LLM** (ChatGroq with LLaMA 3 8B)
  - Defines the **PromptTemplate** that instructs the AI
  - Creates the **LLMChain** pipeline
  - Connects to **NewsAPI** and fetches articles
  - Extracts and processes article text
  
- **Main Functions:**
  - `get_news_articles(query, max_articles)` → fetches from NewsAPI
  - `extract_article_texts(articles)` → pulls title + description
  - `build_summaries_text(article_texts)` → joins into one text block
  - `get_summary(query, max_articles)` → master orchestrator
  
- **LLM Configuration:**
  - Model: `llama3-8b-8192` (fast, free)
  - Temperature: 0.3 (factual, not creative)
  - Max tokens: 1024 (enough for comprehensive summaries)
  
- **Prompt Template:**
  - Gives the LLM a "role" (equity research analyst)
  - Provides the news articles as context
  - Instructs the format: 4-6 paragraphs + bullet point takeaways
  - Emphasizes: only use info from articles, professional tone

---

#### **3. `utils.py`** (9 KB | 240+ lines)
**Utility Functions Library**

- **What it does:** Provides standalone helper functions used throughout the project
- **Key functions:**
  - `format_published_date(iso_date)` — converts "2024-03-15T10:30:00Z" → "15 Mar 2024"
  - `truncate_text(text, max_chars)` — safely shortens long strings at word boundaries
  - `validate_query(query)` — checks user input before API calls
  - `get_source_domain(url)` — extracts "reuters.com" from full URL
  - `count_words(text)` — counts words in summary
  - `build_download_content(query, model, summary, articles)` — formats .txt export
  
- **Why separated:** Keeps the codebase clean, testable, and reusable

---

#### **4. `requirements.txt`** (144 bytes)
**Python Dependencies**

Lists all packages needed with version constraints:
```
langchain>=0.2.0
langchain-groq>=0.1.0
langchain-community>=0.2.0
newsapi-python>=0.2.7
streamlit>=1.35.0
python-dotenv>=1.0.0
requests>=2.31.0
```

Install all with: `pip install -r requirements.txt`

---

#### **5. `.env`** (Template)
**API Keys Storage**

** CRITICAL:** This file contains secret API keys.
- **Never commit to Git** (it's in `.gitignore`)
- **Never share** with anyone
- **Create yourself** and fill in your own keys:
  ```
  GROQ_API_KEY=your_groq_key_here
  NEWS_API_KEY=your_newsapi_key_here
  ```

---

#### **6. `.gitignore`** (399 bytes)
**Version Control Exclusions**

Tells Git which files NOT to track:
- `.env` — API keys (security)
- `venv/` — virtual environment (too large)
- `__pycache__/` — Python cache (not needed)
- `.streamlit/` — Streamlit cache

---

#### **7. `README.md`** (6 KB)
**Full Project Documentation**

Comprehensive guide including:
- One-line summary
- Architecture diagram
- Project structure
- Quick start guide (6 steps)
- How to use the app
- Available models
- Dependencies table
- FAQ & troubleshooting
- Optional enhancements

**Read this first!**

---

#### **8. `QUICKSTART.md`** (3.5 KB)
**5-Minute Setup Guide**

Fast-track setup instructions:
- Scripts for Windows & macOS/Linux
- Manual setup steps (if scripts fail)
- API key registration links
- Troubleshooting table
- Getting help resources

**Start here if you want to run immediately.**

---

### **Pages Folder** — Multi-Page Navigation

Streamlit automatically creates navigation links for any .py file in `pages/`:

#### **9. `pages/history.py`** (5 KB | 140+ lines)
**Search History Page**

- **What it does:** Shows past queries and summaries from the current session
- **Features:**
  - Lists all queries with timestamps
  - Expandable cards showing full summaries
  - Download button for each past search
  - Clear all history button
  - Session-based (cleared on browser refresh)

---

#### **10. `pages/about.py`** (7.5 KB | 200+ lines)
**Project Information Page**

- **What it does:** Explains the project architecture and setup
- **Sections:**
  - System architecture diagram (ASCII art)
  - Tech stack description
  - Setup instructions (4 phases)
  - Project file summary
  - Getting help resources

---

### **Setup & Launch Scripts**

#### **11. `setup.sh`** (3.6 KB | Bash)
**Automated Setup for macOS/Linux**

**What it does:**
1. Creates a virtual environment
2. Activates it
3. Upgrades pip
4. Installs all dependencies
5. Prompts for API keys
6. Creates .env file with keys

**Usage:**
```bash
bash setup.sh
```

---

#### **12. `setup.bat`** (3.5 KB | Batch)
**Automated Setup for Windows**

Same as `setup.sh` but for Windows command prompt.

**Usage:**
```batch
setup.bat
```

---

#### **13. `run.sh`** (640 bytes | Bash)
**Quick Launch for macOS/Linux**

Activates virtual environment and launches Streamlit.

**Usage:**
```bash
bash run.sh
```

---

#### **14. `run.bat`** (645 bytes | Batch)
**Quick Launch for Windows**

Same as `run.sh` but for Windows.

**Usage:**
```batch
run.bat
```

---

### **Documentation & Learning**

#### **15. `Project_Walkthrough.ipynb`** (24 KB | Jupyter Notebook)
**Step-by-Step Code Walkthrough**

Complete Jupyter notebook with:
- **Phase 1:** Environment setup and package installation
- **Phase 2:** LangChain configuration explained
- **Phase 3:** NewsAPI integration walkthrough
- **Phase 4:** End-to-end pipeline test
- **Phase 5:** Utility functions demonstration
- **Phase 6:** Streamlit app overview
- **Phase 7:** Project summary

Each section has:
- Markdown explanations
- Executable code cells
- Output examples
- Function docstrings

**Best for:** Understanding the project line-by-line

---

## ** Data Flow Diagram**

```
┌─────────────────────────┐
│   User Query in         │
│   Streamlit Text Input  │
└────────────┬────────────┘
             │
             ▼
     ┌───────────────────────────┐
     │       app.py              │
     │   (Streamlit UI)          │
     └────────────┬──────────────┘
                  │ calls
                  ▼
     ┌────────────────────────────┐
     │   langchain_config.py      │
     │   (Intelligence Layer)     │
     └──┬───────────────────┬─────┘
        │                   │
        ▼                   ▼
   ┌──────────┐      ┌──────────────────┐
   │ NewsAPI  │      │   Groq LLM       │
   │ Fetch    │      │   (LLaMA 3)      │
   │ Articles │      │   via LangChain  │
   └────┬─────┘      └──────────┬───────┘
        │                       │
        └───────────┬───────────┘
                    ▼
        ┌──────────────────────────┐
        │  Article Texts + LLM     │
        │  Response Combined       │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │    app.py Displays       │
        │  Summary + Source Cards  │
        │  Download Button Ready   │
        └──────────────────────────┘
```

---

## ** Getting Started (5 Steps)**

### **Step 1 — Extract ZIP**
```bash
unzip news_research_tool.zip
cd news_research_tool
```

### **Step 2 — Run Setup Script**
**macOS/Linux:**
```bash
bash setup.sh
```
**Windows:**
```batch
setup.bat
```

### **Step 3 — Enter API Keys When Prompted**
Get them from:
- Groq: https://console.groq.com
- NewsAPI: https://newsapi.org

### **Step 4 — Run the App**
**macOS/Linux:**
```bash
bash run.sh
```
**Windows:**
```batch
run.bat
```

### **Step 5 — Open Browser**
App opens at: **http://localhost:8501**

---

## ** Project Statistics**

| Metric | Value |
|--------|-------|
| Total Files | 16 |
| Total Lines of Code | 1,385+ |
| Python Files | 5 |
| Documentation Files | 5 |
| Setup Scripts | 4 |
| Project Size (ZIP) | 33 KB |
| API Cost | Free |
| OpenAI Dependency | None |
| Free Alternatives | Groq + NewsAPI |

---

## **🛠️ Tech Stack Breakdown**

| Component | Technology | Cost | Role |
|-----------|-----------|------|------|
| Web UI | Streamlit | Free | Front-end |
| News Source | NewsAPI | Free (100 req/day) | Data source |
| LLM | Groq + LLaMA 3 | Free | Intelligence |
| Orchestration | LangChain | Free | Pipeline |
| Secrets | python-dotenv | Free | Config |
| **Total** | **Multiple Free** | **$0** | **Complete** |

---

## ** Key Features**

✅ **No OpenAI Cost** — Uses free Groq API  
✅ **Real-Time News** — Fetches current articles  
✅ **AI Summarization** — LLaMA 3 powered  
✅ **Professional Output** — Structured 4-6 paragraphs + bullets  
✅ **Easy Deployment** — Single `streamlit run app.py`  
✅ **Source Transparency** — Shows all articles used  
✅ **Download Export** — Save as .txt file  
✅ **Session History** — View past queries  
✅ **Multi-page App** — History + About pages  
✅ **Dark Theme UI** — Professional appearance  

---

## ** Learning Resources Inside**

1. **README.md** — Full documentation + architecture
2. **QUICKSTART.md** — Fast setup guide
3. **Project_Walkthrough.ipynb** — Code explanations with runnable cells
4. **Built-in app pages:**
   - `/about` — Architecture details
   - `/history` — Session tracking

---

## ** API Keys Required**

### **Groq (Free)**
1. Sign up at https://console.groq.com
2. No credit card needed
3. Click API Keys → Create API Key
4. Copy key to .env

### **NewsAPI (Free tier)**
1. Register at https://newsapi.org/register
2. Key shown immediately
3. 100 requests/day limit
4. Copy key to .env

---

## ** Frequently Asked Questions**

**Q: Do I need an OpenAI API key?**  
A: No! This project uses Groq's free API instead.

**Q: How much does this cost to run?**  
A: Completely free. Both Groq and NewsAPI offer free tiers.

**Q: Can I deploy this online?**  
A: Yes! Streamlit Community Cloud hosts it free.

**Q: How long does a summary take?**  
A: 5-10 seconds for news fetching + LLM processing.

**Q: Can I customize the prompt?**  
A: Yes, edit the `PROMPT_TEMPLATE` in `langchain_config.py`

**Q: Is my .env file safe?**  
A: Yes, it's in `.gitignore` and never committed to Git.

---

## ** Support**

1. Check **README.md** for full docs
2. Read **Project_Walkthrough.ipynb** for code details
3. Open app's **About** page for architecture
4. Review **QUICKSTART.md** for setup help

---

**Built with using LangChain + Groq + NewsAPI + Streamlit**  
**OpenAI-free · Fully local-compatible · Production-ready**

### **Equity News Research Tool**

An AI-powered news summarisation assistant for equity research analysts
Built with LangChain · Groq (LLaMA 3) · NewsAPI · Streamlit
Completely free — no OpenAI API key required


One-Line Summary
Type any company name, market event, or financial topic → get a professionally structured AI summary of the latest news articles in seconds.

Architecture
User Query (Streamlit Web UI)
          │
          ▼
    ┌─────────────┐
    │   app.py    │  ← Web interface (Streamlit)
    └──────┬──────┘
           │ calls
           ▼
    ┌──────────────────────┐
    │  langchain_config.py │  ← Core intelligence layer
    └──────┬───────────────┘
           │
     ┌─────┴──────┐
     │            │
     ▼            ▼
 NewsAPI       Groq LLM
 (news fetch)  (LLaMA 3 - free)
     │            │
     └─────┬──────┘
           ▼
    AI Summary → User

Project Structure
news_research_tool/
├── app.py                  ← Main Streamlit app (run this)
├── langchain_config.py     ← LLM + NewsAPI pipeline
├── utils.py                ← Helper functions
├── pages/
│   ├── history.py          ← Search history page
│   └── about.py            ← Project info page
├── .env                    ← API keys (never commit this!)
├── .gitignore
├── requirements.txt
└── README.md

Quick Start
Step 1 — Clone / Download the project
bash# If downloaded as zip:
unzip news_research_tool.zip
cd news_research_tool
Step 2 — Create a virtual environment (recommended)
bashpython -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
Step 3 — Install dependencies
bashpip install -r requirements.txt
Step 4 — Get your free API keys
Groq API Key (replaces OpenAI — completely free)

Go to https://console.groq.com
Sign up with your email (no credit card required)
Click "API Keys" in the left sidebar
Click "Create API Key"
Copy the key

NewsAPI Key (free tier: 100 requests/day)

Go to https://newsapi.org/register
Sign up with your email
Your API key is shown immediately on the dashboard
Copy the key

Step 5 — Configure your .env file
Open the .env file and replace the placeholder values:
envGROQ_API_KEY=gsk_your_actual_groq_key_here
NEWS_API_KEY=your_actual_newsapi_key_here
Step 6 — Run the app
bashstreamlit run app.py
Opens automatically at http://localhost:8501

How to Use

The web app opens in your browser
Type a query in the search box, e.g.:

"Tesla Q4 earnings results"
"Federal Reserve interest rate decision"
"NVIDIA AI chip shortage"
"Bitcoin price rally 2024"


Adjust settings in the left sidebar:

Max Articles — how many news articles to fetch (3–20)
Groq Model — choose between LLaMA 3 8B, 70B, or Mixtral
Show Source Articles — toggle article cards on/off


Click "Get AI Summary"
Within a few seconds you get:

Quick stats (articles fetched, sources, model)
Full AI-generated research summary
Download button (.txt export)
Individual source article cards




Available Models (all free on Groq)
ModelSpeedBest Forllama3-8b-8192⚡ FastestGeneral summarisationllama3-70b-8192🔥 PowerfulComplex analysismixtral-8x7b-32768📄 Large contextMany articles

Dependencies
PackageVersionPurposelangchain≥0.2.0LLM orchestration frameworklangchain-groq≥0.1.0Groq LLM connectorlangchain-community≥0.2.0Community integrationsnewsapi-python≥0.2.7NewsAPI clientstreamlit≥1.35.0Web application frameworkpython-dotenv≥1.0.0Load .env API keysrequests≥2.31.0HTTP requests

What Replaced OpenAI
ComponentOriginal (OpenAI)This Project (Groq)LLM ModelGPT-3.5 / GPT-4LLaMA 3 (Meta)API ProviderOpenAIGroqLangChain Classlangchain.OpenAI()ChatGroq()Cost~$0.002/1K tokensFreeSpeedModerateVery fast (LPU)Context window4K–128K tokens8K–32K tokens

Common Issues & Fixes
EnvironmentError: GROQ_API_KEY not found
→ Make sure your .env file exists in the project root and contains the key.
NewsAPI error: rateLimited
→ Free tier allows 100 requests/day. Wait 24 hours or upgrade your plan.
ModuleNotFoundError
→ Run pip install -r requirements.txt again inside your virtual environment.
streamlit: command not found
→ Make sure your virtual environment is activated before running the command.

Security Notes

Never commit your .env file to Git — it contains secret API keys
The .gitignore file already excludes .env from version control
Rotate your API keys if you accidentally expose them


Optional Enhancements
FeatureHowSave history to databaseAdd sqlite3 or tinydbExport as PDFAdd fpdf2 or reportlabAdd loginUse streamlit-authenticatorSchedule daily digestsUse APSchedulerDeploy onlinePush to Streamlit Community Cloud — free

License
MIT License — free for personal and commercial use.
