import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/", methods=["GET"])
def home():
    return "Telegram Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message", {})
    text = message.get("text", "")
    chat = message.get("chat", {})
    chat_id = chat.get("id")

    if chat_id and text.startswith("/start"):

        welcome_text = (
            "🌐 Welcome to our Service Center\n\n"
            "Your gateway to our services worldwide.\n"
            "Choose an option below to get started. 👇"
        )

        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🚀 REGISTER NOW",
                        "url": "https://example.com/register"
                    }
                ],
                [
                    {
                        "text": "🎁 PROMOTIONS",
                        "url": "https://example.com/promotions"
                    }
                ],
                [
                    {
                        "text": "📢 OFFICIAL CHANNEL",
                        "url": "https://t.me/example"
                    },
                    {
                        "text": "💬 SUPPORT",
                        "url": "https://t.me/example"
                    }
                ]
            ]
        }

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": welcome_text,
                "reply_markup": keyboard
            },
            timeout=10
        )

    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
