from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# ✅ use ENV VARIABLES properly
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.on_event("startup")
def set_webhook():
    requests.get(f"{TELEGRAM_API}/setWebhook", params={
        "url": WEBHOOK_URL
    })

@app.post("/")
async def webhook(req: Request):
    data = await req.json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        requests.post(f"{TELEGRAM_API}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"Echo: {text}"
        })

    return {"ok": True}
