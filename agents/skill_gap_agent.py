from .base import call_groq, Groq

SYSTEM = """You are a technical skills analyst who specializes in AI/ML and software 
engineering career development. You identify exact skill gaps and give concrete, 
resource-backed learning roadmaps."""

def analyze_skill_gap(client: Groq, resume: str, role: str, job_description: str = "") -> str:
    jd_section = f"\nJOB DESCRIPTION:\n{job_description}" if job_description else ""

    prompt = f"""Perform a detailed skill gap analysis for a candidate targeting **{role}** roles.

## Skills You Already Have ✅
List 6-8 relevant skills visible in the resume. Be specific (e.g. "PyTorch for CNN training", 
not just "Python").

## Critical Skill Gaps ❌
List 6-8 skills that are missing or underdeveloped for {role} roles. 
Explain WHY each gap matters for this specific role.

## Priority Learning Roadmap
Give a 3-phase learning plan (30 days / 60 days / 90 days):
- What to learn
- Specific free resource (Coursera, fast.ai, YouTube channel, paper, GitHub repo)
- How to demonstrate it on resume/GitHub

## Quick Wins (This Week)
2-3 things the candidate can do in the next 7 days to immediately strengthen their profile.

---
RESUME:
{resume}
{jd_section}
"""
    return call_groq(client, SYSTEM, prompt)
