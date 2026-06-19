from .base import call_groq, Groq

SYSTEM = """You are an expert cover letter writer who crafts compelling, 
personalized cover letters for tech and AI/ML roles. You write in a confident 
but human tone — never generic or corporate-sounding."""

def write_cover_letter(client: Groq, resume: str, role: str, job_description: str = "") -> str:
    jd_section = f"\nJOB DESCRIPTION:\n{job_description}" if job_description else ""

    prompt = f"""Write a professional and personalized cover letter for a **{role}** position.

Rules:
- Keep it under 350 words
- Start with a strong opening hook (not "I am writing to apply for...")
- Mention 2-3 specific achievements from the resume with numbers if available
- Show genuine enthusiasm for the role/company
- End with a confident call to action
- Sound like a real human, not a template
- If a job description is provided, mirror its language and address specific requirements

RESUME:
{resume}
{jd_section}

Write the full cover letter now. Do not add any commentary before or after it.
"""
    return call_groq(client, SYSTEM, prompt)
