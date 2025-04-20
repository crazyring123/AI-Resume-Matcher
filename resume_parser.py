import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def extract_resume_info(resume_text):
    messages = [
        {"role": "system", "content": "You are an expert resume parser."},
        {"role": "user", "content": f"""
Extract the following fields from the resume below:
- Name
- Email
- Phone
- Education
- Skills
- Experience
Provide the output as bullet points.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""}
    ]

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
