import os
import time
import threading
import requests
from flask import Flask

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

app = Flask(__name__)

@app.route("/")
def home():
    return "Sports trading alert bot is running."

def send_discord_alert(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK_URL")
        return

    response = requests.post(
        DISCORD_WEBHOOK_URL,
        json={"content": message},
        timeout=10
    )

    if response.status_code not in (200, 204):
        print("Discord error:", response.status_code, response.text)

def bot_loop():
    time.sleep(5)
    send_discord_alert("✅ Sports trading alert bot is live on Render.")

    while True:
        # Later: add tennis score + Betfair odds logic here
        print("Bot heartbeat: running")
        time.sleep(60)

threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
