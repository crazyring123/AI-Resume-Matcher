import requests
import json

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}
data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! Can you tell me a joke?"}
    ],
    "temperature": 0.5
}

response = requests.post(url, headers=headers, json=data)
print("Status:", response.status_code)
print("Response:")
print(response.text)
