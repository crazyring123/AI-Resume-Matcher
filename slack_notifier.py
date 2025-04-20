import requests

SLACK_TOKEN = "xoxb-8767528992406-8773988400517-gTteBozwpdasPvRFmKUXi6Ew"
CHANNEL_ID = "C08NKFK6EGN"  # all-ai-resume-screen

def send_slack_notification(message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": CHANNEL_ID,
        "text": message
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        if not response_data.get("ok"):
            raise Exception(f"Slack API Error: {response_data}")
        return "✅ Notification sent to Slack successfully."
    except Exception as e:
        return f"❌ Failed to send Slack notification: {e}"
