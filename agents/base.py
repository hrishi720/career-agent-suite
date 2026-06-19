from groq import Groq


def get_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)


def call_groq(client: Groq, system_prompt: str, user_prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Single call to Groq. Returns the text response."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.7,
    )
    return response.choices[0].message.content
