### **Equity News Research Tool**

An AI-powered news summarisation assistant for equity research analysts
Built with LangChain · Groq (LLaMA 3) · NewsAPI · Streamlit
✅ Completely free — no OpenAI API key required


📋 One-Line Summary
Type any company name, market event, or financial topic → get a professionally structured AI summary of the latest news articles in seconds.

🏗️ Architecture
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

📁 Project Structure
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

🚀 Quick Start
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
🔑 Groq API Key (replaces OpenAI — completely free)

Go to https://console.groq.com
Sign up with your email (no credit card required)
Click "API Keys" in the left sidebar
Click "Create API Key"
Copy the key

🔑 NewsAPI Key (free tier: 100 requests/day)

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
✅ Opens automatically at http://localhost:8501

🎮 How to Use

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


Click "🔎 Get AI Summary"
Within a few seconds you get:

📊 Quick stats (articles fetched, sources, model)
🤖 Full AI-generated research summary
⬇️ Download button (.txt export)
📰 Individual source article cards




🤖 Available Models (all free on Groq)
ModelSpeedBest Forllama3-8b-8192⚡ FastestGeneral summarisationllama3-70b-8192🔥 PowerfulComplex analysismixtral-8x7b-32768📄 Large contextMany articles

📦 Dependencies
PackageVersionPurposelangchain≥0.2.0LLM orchestration frameworklangchain-groq≥0.1.0Groq LLM connectorlangchain-community≥0.2.0Community integrationsnewsapi-python≥0.2.7NewsAPI clientstreamlit≥1.35.0Web application frameworkpython-dotenv≥1.0.0Load .env API keysrequests≥2.31.0HTTP requests

🔄 What Replaced OpenAI
ComponentOriginal (OpenAI)This Project (Groq)LLM ModelGPT-3.5 / GPT-4LLaMA 3 (Meta)API ProviderOpenAIGroqLangChain Classlangchain.OpenAI()ChatGroq()Cost~$0.002/1K tokensFreeSpeedModerateVery fast (LPU)Context window4K–128K tokens8K–32K tokens

🛑 Common Issues & Fixes
EnvironmentError: GROQ_API_KEY not found
→ Make sure your .env file exists in the project root and contains the key.
NewsAPI error: rateLimited
→ Free tier allows 100 requests/day. Wait 24 hours or upgrade your plan.
ModuleNotFoundError
→ Run pip install -r requirements.txt again inside your virtual environment.
streamlit: command not found
→ Make sure your virtual environment is activated before running the command.

🔐 Security Notes

Never commit your .env file to Git — it contains secret API keys
The .gitignore file already excludes .env from version control
Rotate your API keys if you accidentally expose them


📈 Optional Enhancements
FeatureHowSave history to databaseAdd sqlite3 or tinydbExport as PDFAdd fpdf2 or reportlabAdd loginUse streamlit-authenticatorSchedule daily digestsUse APSchedulerDeploy onlinePush to Streamlit Community Cloud — free

📄 License
MIT License — free for personal and commercial use.