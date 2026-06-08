import requests
from impact_analyzer import analyze_market_impact

NEWS_API_KEY = "ecfe71c7a41042c38f8bdc58b6fac9c3"

BOT_TOKEN = "7961670645:AAFjvkLR3DELvlHlkEl-2Kc41CxXeUIefJ4"
CHAT_ID = "242367281"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, data=data)

    if response.status_code == 200:
        print("Telegram message sent successfully!")
    else:
        print("Telegram error:", response.text)


news_url = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business"
    "&language=en"
    "&country=us"
    f"&apiKey={NEWS_API_KEY}"
)

response = requests.get(news_url)
data = response.json()

message = "🚨 MARKET NEWS UPDATE 🚨\n\n"

keywords = [
    "iran",
    "israel",
    "war",
    "russia",
    "ukraine",
    "china",
    "taiwan",
    "fed",
    "federal reserve",
    "rbi",
    "oil",
    "crude",
    "inflation",
    "interest rate",
    "stock market",
    "nifty",
    "sensex",
    "tariff",
    "sanction"
]

for article in data.get("articles", []):

    title = article.get("title", "")

    if any(keyword in title.lower() for keyword in keywords):

        impact = analyze_market_impact(title)

        message += (
            f"📰 {title}\n"
            f"{impact}\n\n"
        )

send_telegram_message(message)

print("Done.")