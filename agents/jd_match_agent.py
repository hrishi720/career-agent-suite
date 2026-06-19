from .base import call_groq, Groq

SYSTEM = """You are an ATS system and hiring manager combined. You analyze how well 
a candidate's resume matches a specific job description and give precise, 
data-driven match analysis."""

def match_jd(client: Groq, resume: str, role: str, job_description: str = "") -> str:
    if job_description:
        prompt = f"""Analyze how well this resume matches the job description for a **{role}** role.

## Match Score
Give an overall match percentage. Format: "Match: XX%"
Break it down: Technical skills match: X%, Experience match: X%, Keywords match: X%

## Matched Keywords ✅
List every keyword/requirement from the JD that appears in the resume.

## Missing Keywords ❌
List every keyword/requirement from the JD that is ABSENT from the resume.

## Tailoring Recommendations
Give 5 specific changes to make to the resume to better target this exact job.
For each change, show before → after example where possible.

## Should You Apply?
Give a straight recommendation: Apply now / Apply after improvements / Not a fit yet.
One paragraph, be direct.

---
RESUME:
{resume}

JOB DESCRIPTION:
{job_description}
"""
    else:
        prompt = f"""No specific job description was provided. Analyze the resume against 
typical **{role}** requirements from top Indian tech companies (Google, Microsoft, Flipkart, 
Swiggy, startups hiring in 7-9 LPA range).

## Estimated Match Score
Format: "Match: ~XX% (estimated against typical {role} JDs)"

## What's Strong for {role} Roles ✅
Skills and experience that align well with the market.

## What's Typically Required But Missing ❌
Common requirements for {role} roles that aren't visible in this resume.

## Resume Tailoring Tips
5 specific ways to make this resume stronger for {role} job applications.

---
RESUME:
{resume}
"""
    return call_groq(client, SYSTEM, prompt)
