import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def calculate_match_score(resume_info, job_description):
    messages = [
        {"role": "system", "content": "You are a job match evaluator."},
        {"role": "user", "content": f"""
Compare the candidate's resume information with the job description and return a match score out of 100.

Resume Info:
\"\"\"
{resume_info}
\"\"\"

Job Description:
\"\"\"
{job_description}
\"\"\"

Respond only with:
Match Score: <score>%
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
