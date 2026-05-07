import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
app = Flask(name)
ALERTED = set()
@app.route("/")
def home():
return "BackTheBreak score-zone bot is running."
def send_discord_alert(message):
requests.post(DISCORD_WEBHOOK_URL, json={"content": message}, timeout=10)
def fetch_flashscore_page():
url = "https://www.flashscore.com/tennis/"
headers = {
"User-Agent": "Mozilla/5.0"
}
r = requests.get(url, headers=headers, timeout=15)
r.raise_for_status()
return r.text
def scan_scores():
html = fetch_flashscore_page()
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(" ", strip=True)
# This is basic v1 detection.
# We’ll improve selectors after seeing what Render logs show.
zones = ["2 2", "3 3", "4 4"]
alerts = []
for zone in zones:
if zone in text:
alerts.append(zone.replace(" ", "-"))
return alerts
def bot_loop():
send_discord_alert("✅ BackTheBreak score-zone bot started.")
while True:
try:
alerts = scan_scores()
for score in alerts:
key = f"score-zone-{score}"
if key not in ALERTED:
ALERTED.add(key)
send_discord_alert(
f"🎾 SCORE ZONE ALERT\n\n"
f"A tennis match appears to be at {score}.\n\n"
f"Action: Open Flashscore + Betfair.\n"
f"Wait for pressure on serve — do NOT enter until a break happens."
)
print("Scan complete:", alerts)
except Exception as e:
print("Scanner error:", str(e))
time.sleep(60)
threading.Thread(target=bot_loop, daemon=True).start()
if name == "main":
port = int(os.getenv("PORT", 10000))
app.run(host="0.0.0.0", port=port)
