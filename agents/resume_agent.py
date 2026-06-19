from .base import call_groq, Groq

SYSTEM = """You are a senior technical recruiter and resume expert with 10+ years of experience 
hiring for AI/ML and software engineering roles at top tech companies. 
You give honest, specific, and actionable resume feedback."""

def analyze_resume(client: Groq, resume: str, role: str) -> str:
    prompt = f"""Analyze this resume for a **{role}** position. Give a detailed review with:

## Overall Score
Give a score out of 10 with one sentence justification. Format: "Score: X/10"

## ATS Readiness
Rate ATS compatibility out of 10. Format: "ATS Score: X/10"
Mention if keywords for {role} are present or missing.

## Top 3 Strengths
What works well in this resume.

## Top 3 Weaknesses
Be honest. What's holding this resume back.

## Impact & Metrics
Does the resume use numbers/metrics? Point to specific bullet points that are weak 
and rewrite them with stronger impact.

## Specific Action Items
Give exactly 5 actionable improvements the candidate should make this week.

---
RESUME:
{resume}
"""
    return call_groq(client, SYSTEM, prompt)
