# Career Agent Suite 💼
Multi-agent job search assistant powered by **Groq + Llama 4 Scout**, **Adzuna** (live jobs), and **Streamlit**.

API keys are configured server-side only (`.env` or Streamlit secrets) — never typed into the UI.

## Agents
| Agent | What it does |
|---|---|
| 🔎 Job Search | Pulls live job listings from Adzuna, AI-ranks them against your resume |
| 📝 Resume Analyst | Scores resume, ATS check, strengths/weaknesses, action items |
| ✉️ Cover Letter Writer | Personalized cover letter under 350 words |
| 📊 Skill Gap Agent | Skills you have vs. need, 90-day learning roadmap |
| 🎯 JD Matcher | Keyword match %, tailoring tips for specific JD |

## Project Structure
```
career_agent_suite/
├── app.py                       # Main Streamlit app (no keys in UI)
├── requirements.txt
├── .env.example                 # Template for local dev
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example     # Template for Streamlit Cloud deploy
├── utils.py                     # PDF reader, helpers
└── agents/
    ├── __init__.py
    ├── base.py                  # Groq client wrapper
    ├── resume_agent.py
    ├── cover_letter_agent.py
    ├── skill_gap_agent.py
    ├── jd_match_agent.py
    └── job_search_agent.py      # Adzuna API + AI ranking
```

## How to use
1. Upload resume PDF or paste resume text
2. Enter the role you're targeting (e.g. "ML Engineer") and optionally a location (e.g. "Bangalore" — leave blank to search all of India)
3. Optionally paste a job description for precise JD matching
4. Select which agents to run (Job Search is on by default)
5. Click 🚀 Run Agents

The **Job Search** tab pulls real, live job postings from Adzuna for your
role + location, then has Groq rank the top 5 matches against your resume
with a one-line reason for each.

## Tech Stack
- **Streamlit** — UI
- **Groq API** — LLM backend (free, ultra-fast) — `meta-llama/llama-4-scout-17b-16e-instruct` (500K tokens/day on free tier)
- **Adzuna API** — live job listings (free tier, India + global coverage)
- **PyPDF2** — PDF text extraction
- **python-dotenv** — local env variable management

## Security notes
- API keys live only in `.env` (local) or `st.secrets` (cloud) — never in
  client-facing widgets, query params, or session state.
- A 30-second cooldown between runs and a ~15,000 character resume length cap
  help protect the free-tier API quotas from accidental abuse.
- If you deploy this publicly, anyone using your app uses YOUR Groq/Adzuna
  quota. For a multi-user public app, you'd eventually want per-user auth +
  rate limiting beyond what's built in here.
