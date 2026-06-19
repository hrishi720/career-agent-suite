import requests
from .base import call_groq, Groq


def search_jobs_adzuna(
    app_id: str,
    app_key: str,
    role: str,
    location: str = "",
    country: str = "in",
    results_per_page: int = 15,
    max_days_old: int = 30,
) -> list[dict]:
    """
    Search live job listings using the Adzuna API.
    Free tier: https://developer.adzuna.com/  (signup -> get app_id + app_key)
    country: 'in' for India, 'us', 'gb', etc.
    location: optional — if blank, searches the whole country.
    """
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": results_per_page,
        "what": role,
        "max_days_old": max_days_old,
        "content-type": "application/json",
    }
    if location and location.strip():
        params["where"] = location.strip()

    response = requests.get(url, params=params, timeout=15)
    if not response.ok:
        try:
            err_body = response.json()
            err_msg = err_body.get("exception") or err_body.get("display_message") or str(err_body)
        except Exception:
            err_msg = response.text[:300]
        raise RuntimeError(f"Adzuna API error ({response.status_code}): {err_msg}")
    data = response.json()

    jobs = []
    for item in data.get("results", []):
        jobs.append({
            "title": item.get("title", "—"),
            "company": item.get("company", {}).get("display_name", "Unknown"),
            "location": item.get("location", {}).get("display_name", "—"),
            "salary_min": item.get("salary_min"),
            "salary_max": item.get("salary_max"),
            "description": item.get("description", ""),
            "url": item.get("redirect_url", "#"),
            "created": item.get("created", ""),
            "contract_type": item.get("contract_time") or "Not specified",
        })
    return jobs


SYSTEM_RANK = """You are a job search assistant that ranks job listings by how well 
they match a candidate's resume. You are precise, honest, and concise."""


def rank_and_summarize_jobs(client: Groq, resume: str, role: str, jobs: list[dict]) -> str:
    """Use Groq to rank fetched jobs against the resume and give a short reason for each."""
    if not jobs:
        return "No jobs found. Try a different role or location."

    jobs_text = ""
    for i, j in enumerate(jobs[:10], 1):
        salary = ""
        if j["salary_min"] and j["salary_max"]:
            salary = f" | Salary: ₹{int(j['salary_min']):,} - ₹{int(j['salary_max']):,}"
        jobs_text += f"\n{i}. {j['title']} at {j['company']} ({j['location']}){salary}\n   {j['description'][:200]}...\n   Link: {j['url']}\n"

    prompt = f"""Here is a candidate's resume and a list of live job postings for **{role}** roles.

Rank the TOP 5 jobs that best fit this candidate. For each, give:
- Job number and title
- Match score out of 10
- One-line reason why it fits (or doesn't fully fit)
- The link (copy it exactly as given)

Be honest — if none are a great fit, say so.

RESUME:
{resume}

JOB LISTINGS:
{jobs_text}
"""
    return call_groq(client, SYSTEM_RANK, prompt)