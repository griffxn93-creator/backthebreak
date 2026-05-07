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
    send_discord_alert("✅ BackTheBreak bot live. Scanner starting.")

    while True:
        # TEST DATA — later this will come from live scores
        match = {
            "name": "Test Player A vs Test Player B",
            "score": "3-3",
            "server": "Player B",
            "point_score": "15-30",
            "player_a_odds": 1.72,
            "player_b_odds": 2.20,
        }

        score_zone = match["score"] in ["2-2", "3-3", "4-4"]
        pressure = match["point_score"] in ["0-30", "15-30", "30-40", "40-A"]

        if score_zone and pressure:
            send_discord_alert(
                f"🎾 WATCH — possible Back The Break setup\n\n"
                f"Match: {match['name']}\n"
                f"Score: {match['score']}\n"
                f"Server: {match['server']}\n"
                f"Point score: {match['point_score']}\n"
                f"Odds: {match['player_a_odds']} / {match['player_b_odds']}\n\n"
                f"Action: WATCH — wait for confirmed break."
            )

        time.sleep(300)
threading.Thread(target=bot_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
