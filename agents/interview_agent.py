
from .base import call_groq, Groq

SYSTEM = """You are a senior technical interviewer at a top-tier tech company who has 
conducted 500+ interviews for AI/ML roles. You create realistic, role-specific interview 
questions and teach candidates exactly how to answer them using the STAR method."""

def generate_interview_prep(client: Groq, resume: str, role: str, job_description: str = "") -> str:
    jd_section = f"\nJOB DESCRIPTION:\n{job_description}" if job_description else ""

    prompt = f"""Create a comprehensive interview preparation guide for a **{role}** interview 
based on this candidate's resume.

## Round 1: HR / Behavioral Questions (3 questions)
Pull from actual resume experiences. For each question:
- The question
- Why interviewers ask this
- A sample STAR-format answer using details from their resume

## Round 2: Technical Conceptual Questions (4 questions)
Based on skills listed in the resume. For each:
- The question
- Key points to cover in the answer
- Common mistakes to avoid

## Round 3: System Design / Case Study (2 questions)
Role-appropriate. For each:
- The question
- A structured approach to answer it
- What the interviewer is really evaluating

## Your Likely Weak Spots
Based on the resume, what topics might this candidate struggle with in a {role} interview.
Be direct — this helps them prepare better.

## 5 Questions YOU Should Ask the Interviewer
Smart questions that signal seriority and genuine interest.

---
RESUME:
{resume}
{jd_section}
"""
    return call_groq(client, SYSTEM, prompt)
