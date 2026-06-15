from fastapi import FastAPI, Request
import httpx
import os
import asyncio

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ✅ Set webhook on startup (async)
@app.on_event("startup")
async def set_webhook():
    async with httpx.AsyncClient() as client:
        await client.get(f"{TELEGRAM_API}/setWebhook", params={
            "url": WEBHOOK_URL
        })

# ✅ Optional: health check (para ma-test sa browser)
@app.get("/")
async def root():
    return {"status": "alive"}

# ✅ Webhook (FAST response, no blocking)
@app.post("/")
async def webhook(req: Request):
    data = await req.json()

    # ⚠️ Background processing (para hindi mag timeout)
    asyncio.create_task(handle_update(data))

    return {"ok": True}

# ✅ Background handler (dito ginagawa lahat ng logic)
async def handle_update(data):
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        async with httpx.AsyncClient() as client:
            await client.post(f"{TELEGRAM_API}/sendMessage", json={
                "chat_id": chat_id,
                "text": f"Echo: {text}"
            })
