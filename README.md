# Career Agent Suite 💼
Multi-agent job search assistant powered by **Groq + LLaMA 3.3 70B** and **Streamlit**.

## Agents
| Agent | What it does |
|---|---|
| 📝 Resume Analyst | Scores resume, ATS check, strengths/weaknesses, action items |
| ✉️ Cover Letter Writer | Personalized cover letter under 350 words |
| 📊 Skill Gap Agent | Skills you have vs. need, 90-day learning roadmap |
| 🎯 JD Matcher | Keyword match %, tailoring tips for specific JD |
| 🎤 Interview Coach | Behavioral + technical questions with STAR answers |

## Project Structure
```
career_agent_suite/
├── app.py                  # Main Streamlit app
├── requirements.txt
├── .env.example
├── utils.py                # PDF reader, helpers
└── agents/
    ├── __init__.py
    ├── base.py             # Groq client wrapper
    ├── resume_agent.py
    ├── cover_letter_agent.py
    ├── skill_gap_agent.py
    ├── jd_match_agent.py
    └── interview_agent.py
```

## Setup

### Step 1 — Get Groq API key (free)
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Create API key → copy it

### Step 2 — Clone & install
```bash
git clone <your-repo>
cd career_agent_suite
pip install -r requirements.txt
```

### Step 3 — Set API key
Option A: Create `.env` file:
```
GROQ_API_KEY=gsk_your_key_here
```
Option B: Just paste it in the sidebar when running the app.

### Step 4 — Run
```bash
streamlit run app.py
```
App opens at http://localhost:8501

## How to use
1. Upload resume PDF or paste resume text
2. Enter the role you're targeting (e.g. "ML Engineer")
3. Optionally paste the job description for precise JD matching
4. Select which agents to run
5. Click 🚀 Run Agents

## Tech Stack
- **Streamlit** — UI
- **Groq API** — LLM backend (free, ultra-fast)
- **LLaMA 3.3 70B** — the model powering all agents
- **PyPDF2** — PDF text extraction
- **python-dotenv** — env variable management
