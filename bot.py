import requests
import json
import os

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)


def get_live():
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": CHANNEL_ID,
        "eventType": "live",
        "type": "video",
        "key": YOUTUBE_API_KEY
    }
    r = requests.get(url, params=params).json()
    return r["items"][0] if r.get("items") else None


def send_telegram(video_id, title):
    text = (
        "🔴 Neuer Lügenbrecher Livestream!\n\n"
        f"{title}\n\n"
        f"https://www.youtube.com/watch?v={video_id}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    })


def main():
    posted = load_state()
    live = get_live()

    if live:
        vid = live["id"]["videoId"]
        title = live["snippet"]["title"]
        if vid not in posted:
            send_telegram(vid, title)
            posted.append(vid)
            save_state(posted)


if __name__ == "__main__":
    main()
