import requests

API_KEY = "ecfe71c7a41042c38f8bdc58b6fac9c3"

url = (
    "https://newsapi.org/v2/top-headlines?"
    "category=business"
    "&language=en"
    "&country=us"
    f"&apiKey={API_KEY}"
)

try:
    response = requests.get(url, timeout=10)

    print("Status Code:", response.status_code)

    data = response.json()

    print("\nFULL RESPONSE:")
    print(data)

    if data.get("status") == "ok":

        print("\nLATEST HEADLINES:\n")

        for i, article in enumerate(data.get("articles", [])[:5], start=1):
            print(f"{i}. {article.get('title')}")

    else:

        print("\nAPI ERROR:")
        print("Status :", data.get("status"))
        print("Code   :", data.get("code"))
        print("Message:", data.get("message"))

except Exception as e:
    print("ERROR:", e)