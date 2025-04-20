import requests

SLACK_BOT_TOKEN = "xoxb-8767528992406-8773988400517-gTteBozwpdasPvRFmKUXi6Ew"
url = "https://slack.com/api/conversations.list"

headers = {
    "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
}

response = requests.get(url, headers=headers)
channels = response.json().get("channels")

if channels:
    for channel in channels:
        print(f"Name: {channel['name']} - ID: {channel['id']}")
else:
    print("No channels found or token might be incorrect.")
