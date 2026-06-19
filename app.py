import streamlit as st
import os
import time
from dotenv import load_dotenv

from agents import (
    get_client,
    analyze_resume,
    write_cover_letter,
    analyze_skill_gap,
    match_jd,
    generate_interview_prep,
    search_jobs_adzuna,
    rank_and_summarize_jobs,
)
from utils import extract_text_from_pdf, extract_score

load_dotenv()


def get_secret(key: str) -> str:
    """Read from Streamlit secrets first (for cloud deploy), fall back to .env / OS env (for local dev)."""
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, "")


GROQ_API_KEY = get_secret("GROQ_API_KEY")
ADZUNA_APP_ID = get_secret("ADZUNA_APP_ID")
ADZUNA_APP_KEY = get_secret("ADZUNA_APP_KEY")

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Career Agent Suite",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #8B7FFF, #534AB7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        color: #9A9AB0;
        font-size: 0.95rem;
        margin-bottom: 1.8rem;
    }
    .agent-card {
        background: linear-gradient(145deg, #1E1B33, #16142A);
        border: 1px solid #3A3460;
        border-radius: 12px;
        padding: 16px 14px;
        margin-bottom: 10px;
        height: 100%;
        transition: border-color 0.2s ease;
    }
    .agent-card:hover {
        border-color: #8B7FFF;
    }
    .agent-card .agent-icon {
        font-size: 1.5rem;
        margin-bottom: 6px;
    }
    .agent-card .agent-name {
        font-weight: 700;
        font-size: 0.95rem;
        margin: 4px 0 2px 0;
        color: #F0EFFF;
    }
    .agent-card .agent-desc {
        font-size: 0.78rem;
        color: #9A9AB0;
    }
    .score-box {
        background: linear-gradient(145deg, #2A2350, #1E1A3D);
        border: 1px solid #4A3F8A;
        border-radius: 12px;
        padding: 18px 12px;
        text-align: center;
        margin-bottom: 14px;
    }
    .score-num {
        font-size: 2.4rem;
        font-weight: 800;
        color: #B0A8FF;
        line-height: 1.1;
    }
    .score-label {
        font-size: 0.78rem;
        color: #9A9AB0;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .job-card {
        background: linear-gradient(145deg, #1E1B33, #16142A);
        border: 1px solid #3A3460;
        border-radius: 12px;
        padding: 16px 18px;
        margin-bottom: 12px;
    }
    .job-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #F0EFFF;
    }
    .job-company {
        color: #B0A8FF;
        font-size: 0.9rem;
        margin-top: 2px;
    }
    .job-meta {
        color: #9A9AB0;
        font-size: 0.8rem;
        margin-top: 6px;
    }
    .job-desc {
        color: #C7C5DA;
        font-size: 0.85rem;
        margin-top: 10px;
        line-height: 1.5;
    }
    .match-badge {
        display: inline-block;
        background: linear-gradient(145deg, #2A2350, #1E1A3D);
        border: 1px solid #4A3F8A;
        color: #B0A8FF;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 3px 12px;
        border-radius: 20px;
        margin-bottom: 8px;
    }
    .highlight-tag {
        display: inline-block;
        background: rgba(176,168,255,0.12);
        color: #B0A8FF;
        font-size: 0.75rem;
        padding: 2px 9px;
        border-radius: 12px;
        margin-top: 6px;
    }
    .apply-btn {
        display: inline-block;
        background: linear-gradient(90deg, #8B7FFF, #534AB7);
        color: white !important;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 7px 16px;
        border-radius: 8px;
        text-decoration: none !important;
        margin-top: 10px;
    }
    .apply-btn:hover {
        opacity: 0.88;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.92rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #B0A8FF !important;
    }
    div[data-testid="stSidebarContent"] {
        background: #14121F;
    }
    hr {
        border-color: #2E2A4D !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Sidebar: Inputs (NO API KEYS HERE — those live in .env / st.secrets) ─────
with st.sidebar:
    st.markdown("## ⚙️ Setup")
    st.markdown("---")

    # Resume input
    st.markdown("### 📄 Your Resume")
    upload_tab, paste_tab = st.tabs(["Upload PDF", "Paste Text"])

    resume_text = ""
    with upload_tab:
        uploaded = st.file_uploader("Upload resume", type=["pdf", "txt"], label_visibility="collapsed")
        if uploaded:
            if uploaded.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded)
                if resume_text.startswith("Error"):
                    st.error(resume_text)
                else:
                    st.success(f"✅ PDF read — {len(resume_text.split())} words")
            else:
                resume_text = uploaded.read().decode("utf-8")
                st.success(f"✅ Text file loaded — {len(resume_text.split())} words")

    with paste_tab:
        pasted = st.text_area(
            "Paste your resume",
            height=200,
            placeholder="Paste full resume text here...",
            label_visibility="collapsed",
        )
        if pasted.strip():
            resume_text = pasted

    st.markdown("---")

    # Role & JD & location
    st.markdown("### 🎯 Target Role")
    target_role = st.text_input(
        "Role",
        placeholder="e.g. ML Engineer, Data Scientist",
        label_visibility="collapsed",
    )

    st.markdown("### 📍 Location (optional)")
    target_location = st.text_input(
        "Location",
        value="",
        placeholder="e.g. Bangalore — leave blank for all India",
        label_visibility="collapsed",
    )

    st.markdown("### 📋 Job Description (optional)")
    job_description = st.text_area(
        "JD",
        height=120,
        placeholder="Paste a job description for precise matching...",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Which agents to run
    st.markdown("### 🤖 Select Agents")
    run_jobsearch = st.checkbox("🔎 Job Search (live)", value=True)
    run_resume    = st.checkbox("Resume Feedback",  value=True)
    run_cover     = st.checkbox("Cover Letter",      value=True)
    run_skill     = st.checkbox("Skill Gap",         value=True)
    run_jd        = st.checkbox("JD Match",          value=True)
    run_interview = st.checkbox("Interview Prep",    value=True)

    st.markdown("---")
    run_btn = st.button("🚀 Run Agents", use_container_width=True, type="primary")

    # Quiet config status (no keys shown/typed — just confirms backend is configured)
    st.markdown("---")
    groq_ok = bool(GROQ_API_KEY)
    adzuna_ok = bool(ADZUNA_APP_ID and ADZUNA_APP_KEY)
    st.caption(f"{'🟢' if groq_ok else '🔴'} Groq backend {'connected' if groq_ok else 'not configured'}")
    st.caption(f"{'🟢' if adzuna_ok else '🔴'} Adzuna backend {'connected' if adzuna_ok else 'not configured'}")


# ─── Main area ────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">💼 Career Agent Suite</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-agent job search assistant · Groq + LLaMA 3.3 70B · Live jobs via Adzuna</div>', unsafe_allow_html=True)

# Agent overview cards (always visible)
cols = st.columns(6)
agents_meta = [
    ("🔎", "Job Search",        "Live listings"),
    ("📝", "Resume Analyst",    "Scores & feedback"),
    ("✉️", "Cover Letter",      "Personalized draft"),
    ("📊", "Skill Gap",         "What to learn next"),
    ("🎯", "JD Matcher",        "Keyword alignment"),
    ("🎤", "Interview Coach",   "Q&A prep"),
]
for col, (icon, name, desc) in zip(cols, agents_meta):
    with col:
        st.markdown(f"""
        <div class="agent-card">
            <div class="agent-icon">{icon}</div>
            <div class="agent-name">{name}</div>
            <div class="agent-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ─── Run logic ────────────────────────────────────────────────────────────────
COOLDOWN_SECONDS = 30  # prevent rapid repeated runs from burning free-tier quota

if run_btn:
    last_run = st.session_state.get("last_run_time", 0)
    elapsed = time.time() - last_run
    if elapsed < COOLDOWN_SECONDS:
        wait = int(COOLDOWN_SECONDS - elapsed)
        st.warning(f"⏳ Please wait {wait}s before running again — this keeps the free API quota available for everyone.")
        st.stop()

    # Validation — keys come from backend config, not the user
    if not GROQ_API_KEY:
        st.error("❌ Groq API key not configured on the server. Add GROQ_API_KEY to your .env file or Streamlit secrets.")
        st.stop()
    if run_jobsearch and not (ADZUNA_APP_ID and ADZUNA_APP_KEY):
        st.error("❌ Adzuna API keys not configured on the server. Add ADZUNA_APP_ID and ADZUNA_APP_KEY to your .env file, or untick Job Search.")
        st.stop()
    if not resume_text.strip():
        st.error("❌ Please upload or paste your resume.")
        st.stop()
    if len(resume_text) > 15000:
        st.error("❌ Resume text is too long (max ~15,000 characters). Please trim it to the essentials.")
        st.stop()
    if not target_role.strip():
        st.error("❌ Please enter the target role.")
        st.stop()

    st.session_state["last_run_time"] = time.time()
    client = get_client(GROQ_API_KEY)

    if "results" not in st.session_state:
        st.session_state.results = {}

    selected_agents = []
    if run_jobsearch: selected_agents.append("jobsearch")
    if run_resume:    selected_agents.append("resume")
    if run_cover:     selected_agents.append("cover")
    if run_skill:     selected_agents.append("skill")
    if run_jd:        selected_agents.append("jd")
    if run_interview: selected_agents.append("interview")

    progress = st.progress(0, text="Starting agents...")
    total = len(selected_agents)

    def run_jobsearch_agent():
        jobs = search_jobs_adzuna(
            app_id=ADZUNA_APP_ID,
            app_key=ADZUNA_APP_KEY,
            role=target_role,
            location=target_location,
        )
        ranking = rank_and_summarize_jobs(client, resume_text, target_role, jobs) if jobs else "No jobs found."
        return {"jobs": jobs, "ranking": ranking}

    agent_funcs = {
        "jobsearch": run_jobsearch_agent,
        "resume":    lambda: analyze_resume(client, resume_text, target_role),
        "cover":     lambda: write_cover_letter(client, resume_text, target_role, job_description),
        "skill":     lambda: analyze_skill_gap(client, resume_text, target_role, job_description),
        "jd":        lambda: match_jd(client, resume_text, target_role, job_description),
        "interview": lambda: generate_interview_prep(client, resume_text, target_role, job_description),
    }
    agent_names = {
        "jobsearch": "Job Search Agent",
        "resume": "Resume Analyst",
        "cover":  "Cover Letter Writer",
        "skill":  "Skill Gap Agent",
        "jd":     "JD Matcher",
        "interview": "Interview Coach",
    }

    for i, agent_id in enumerate(selected_agents):
        progress.progress((i) / total, text=f"🤖 Running {agent_names[agent_id]}...")
        try:
            st.session_state.results[agent_id] = agent_funcs[agent_id]()
        except Exception as e:
            st.session_state.results[agent_id] = f"**Error:** {str(e)}"
        progress.progress((i + 1) / total, text=f"✅ {agent_names[agent_id]} done")

    progress.progress(1.0, text="✅ All agents complete!")
    st.session_state["ran"] = True
    st.session_state["role"] = target_role


# ─── Results display ──────────────────────────────────────────────────────────
results = st.session_state.get("results", {})

if not results:
    st.info("👈 Fill in your resume and settings in the sidebar, then hit **Run Agents**.")
    st.markdown("""
    **How it works:**
    1. Upload your resume (PDF or paste text)
    2. Enter the job role and location you're targeting
    3. Optionally paste a job description for precise matching
    4. Select which agents to run and click 🚀

    *(Groq and Adzuna API keys are configured by the app owner in `.env` / secrets — not entered by users.)*
    """)
else:
    tab_labels = []
    tab_ids    = []

    if "jobsearch" in results: tab_labels.append("🔎 Job Search");      tab_ids.append("jobsearch")
    if "resume"    in results: tab_labels.append("📝 Resume Feedback"); tab_ids.append("resume")
    if "cover"     in results: tab_labels.append("✉️ Cover Letter");    tab_ids.append("cover")
    if "skill"     in results: tab_labels.append("📊 Skill Gap");        tab_ids.append("skill")
    if "jd"        in results: tab_labels.append("🎯 JD Match");         tab_ids.append("jd")
    if "interview" in results: tab_labels.append("🎤 Interview Prep");   tab_ids.append("interview")

    tabs = st.tabs(tab_labels)

    for tab, tab_id in zip(tabs, tab_ids):
        content = results[tab_id]
        with tab:

            # ── Job Search tab ───────────────────────────────────────────────
            if tab_id == "jobsearch":
                if isinstance(content, str):
                    st.error(content)
                    st.caption("This usually means the Adzuna API call failed (bad keys, no quota, or bad params) "
                               "or the Groq ranking call failed. Check your ADZUNA_APP_ID / ADZUNA_APP_KEY in .env.")
                else:
                    jobs = content.get("jobs", [])
                    ranking = content.get("ranking", "")
                    location_label = target_location.strip() if target_location.strip() else "all of India"

                    st.markdown(f"**Found {len(jobs)} live listings** for *{st.session_state.get('role','')}* in *{location_label}*")

                    if ranking:
                        with st.expander("🏆 AI-ranked top matches", expanded=True):
                            st.markdown(ranking)

                    st.markdown("---")
                    st.markdown("**All listings:**")
                    for job in jobs:
                        salary = ""
                        if job.get("salary_min") and job.get("salary_max"):
                            salary = f" · ₹{int(job['salary_min']):,} - ₹{int(job['salary_max']):,}"
                        st.markdown(f"""
                        <div class="job-card">
                            <div class="job-title">{job['title']}</div>
                            <div class="job-company">{job['company']}</div>
                            <div class="job-meta">📍 {job['location']}{salary} · {job['contract_type']}</div>
                            <div class="job-desc">{job['description'][:280]}...</div>
                            <a class="apply-btn" href="{job['url']}" target="_blank">🔗 View & Apply</a>
                        </div>
                        """, unsafe_allow_html=True)

            # ── Resume tab ──────────────────────────────────────────────────
            elif tab_id == "resume":
                score = extract_score(content, "Score:")
                ats   = extract_score(content, "ATS Score:")

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-num">{score}</div>
                        <div class="score-label">Overall Score /10</div>
                    </div>""", unsafe_allow_html=True)
                with m2:
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-num">{ats}</div>
                        <div class="score-label">ATS Readiness /10</div>
                    </div>""", unsafe_allow_html=True)
                with m3:
                    role_shown = st.session_state.get("role", "—")
                    st.markdown(f"""
                    <div class="score-box">
                        <div class="score-num" style="font-size:1.3rem;padding-top:10px">{role_shown}</div>
                        <div class="score-label">Target Role</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown(content)

            # ── Cover Letter tab ─────────────────────────────────────────────
            elif tab_id == "cover":
                st.markdown("**Generated cover letter — edit and copy as needed:**")
                edited = st.text_area(
                    "Cover Letter",
                    value=content,
                    height=480,
                    label_visibility="collapsed",
                )
                if st.button("📋 Copy to clipboard", key="copy_cover"):
                    st.code(edited, language=None)
                    st.success("Select all and copy from the code block above ↑")

            # ── Skill Gap tab ────────────────────────────────────────────────
            elif tab_id == "skill":
                st.markdown(content)

            # ── JD Match tab ─────────────────────────────────────────────────
            elif tab_id == "jd":
                match_pct = extract_score(content, "Match:")
                st.markdown(f"""
                <div class="score-box" style="max-width:200px">
                    <div class="score-num">{match_pct}</div>
                    <div class="score-label">JD Match Score</div>
                </div>""", unsafe_allow_html=True)
                st.markdown(content)

            # ── Interview tab ────────────────────────────────────────────────
            elif tab_id == "interview":
                st.markdown(content)
                st.markdown("---")
                st.info("💡 **Tip:** Practice each answer out loud. Record yourself and watch it back.")

st.markdown("---")
st.caption("Built with Streamlit, Groq (LLaMA 3.3 70B), and Adzuna · A multi-agent job search assistant · ")