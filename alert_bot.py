from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "7961670645:AAFjvkLR3DELvlHlkEl-2Kc41CxXeUIefJ4"
CHAT_ID = "242367281"


def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


@app.route('/webhook', methods=['POST'])
def webhook():

    data = request.json

    message = data.get("message", "🚨 New Trading Alert")

    send_telegram_message(message)

    return "Alert Sent Successfully"


@app.route('/')
def home():
    return "Telegram Trading Alert Bot is Running 🚀"


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)