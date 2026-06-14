from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

BOT_TOKEN = os.getenv("8659021262:AAHLH0VcPf-KQuf2Rev7h7n23gEs78X1P08")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TELEGRAM_API = f"https://api.telegram.org/bot{8659021262:AAHLH0VcPf-KQuf2Rev7h7n23gEs78X1P08}"

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
