import requests

from impact_analyzer import (
    analyze_market_impact,
    format_telegram_output,
    save_theme_history,
    STOCK_SCORES,
    REASONS,
    THEME_SCORES,
    THEME_REASONS
)

# ==========================================
# CONFIG
# ==========================================

NEWS_API_KEY = "ecfe71c7a41042c38f8bdc58b6fac9c3"
BOT_TOKEN    = "7961670645:AAFjvkLR3DELvlHlkEl-2Kc41CxXeUIefJ4"
CHAT_ID      = "242367281"

# ==========================================
# MULTI-SOURCE NEWS FEED
# Tier 1: Reuters, Bloomberg, WSJ, FT (weight 3)
# Tier 2: CNBC, Barrons, MarketWatch   (weight 2)
# Tier 3: broader financial             (weight 1)
# ==========================================

NEWS_SOURCES = [
    "reuters",
    "bloomberg",
    "the-wall-street-journal",
    "financial-times",
    "cnbc",
    "barrons",
    "marketwatch",
    "the-economist",
    "business-insider",
    "fortune"
]


def fetch_news():
    """
    Fetch from Tier 1-3 financial sources first.
    Falls back to business top-headlines if < 5 results.
    Deduplicates by title.
    """
    seen         = set()
    all_articles = []

    # --- Primary: financial sources ---
    sources_str = ",".join(NEWS_SOURCES)
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"sources={sources_str}&"
        f"apiKey={NEWS_API_KEY}"
    )

    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        for article in data.get("articles", []):
            title = article.get("title", "")
            if title and title not in seen:
                seen.add(title)
                all_articles.append(article)
        print(f"Primary feed: {len(all_articles)} articles")
    except Exception as e:
        print(f"Primary fetch error: {e}")

    # --- Fallback: US business headlines ---
    if len(all_articles) < 5:
        fallback_url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"category=business&country=us&"
            f"apiKey={NEWS_API_KEY}"
        )
        try:
            resp = requests.get(fallback_url, timeout=10)
            data = resp.json()
            for article in data.get("articles", []):
                title = article.get("title", "")
                if title and title not in seen:
                    seen.add(title)
                    all_articles.append(article)
            print(f"After fallback: {len(all_articles)} articles")
        except Exception as e:
            print(f"Fallback fetch error: {e}")

    return all_articles


def send_telegram_message(message):
    url     = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text":    message[:3900]
    }
    response = requests.post(url, json=payload, timeout=20)
    print("\nSTATUS:", response.status_code)
    print(response.text)


def reset_scores():
    for stock in STOCK_SCORES:
        STOCK_SCORES[stock] = 0
    REASONS.clear()
    for theme in THEME_SCORES:
        THEME_SCORES[theme] = 0
    for theme in THEME_REASONS:
        THEME_REASONS[theme].clear()


def generate_report():
    articles = fetch_news()

    reset_scores()

    important_news = []

    # ==========================================
    # GARBAGE FILTER — pre-analysis
    # ==========================================
    IGNORE_KEYWORDS = [
        "prime day", "shopping", "coupon", "discount",
        "lost item", "lost items",
        "celebrity", "movie", "music",
        "football", "cricket", "nba",
        "social security", "retirement",
        "travel", "vacation",
        "lifestyle", "fashion",
        "breast milk", "butterflies",
        "uber", "amazon deal", "best buy",
        "horoscope", "recipe", "weather",
        "box office", "album", "reality tv"
    ]

    # Process up to 20 articles with source name for weighting
    for article in articles[:20]:
        title  = article.get("title", "")
        source = article.get("source", {}).get("name", "")

        if not title:
            continue

        lower_title = title.lower()

        if any(kw in lower_title for kw in IGNORE_KEYWORDS):
            print(f"FILTERED: {title[:60]}")
            continue

        important_news.append(title)

        try:
            analyze_market_impact(title, source=source)
        except Exception as e:
            print(f"Analysis error: {e}")

    # Rank stocks
    ranked_stocks = sorted(
        STOCK_SCORES.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_scored = [
        (s, sc) for s, sc in ranked_stocks
        if sc > 0
    ]

    # ==========================================
    # REPORT HEADER
    # ==========================================
    report  = "📊 PRE-MARKET REPORT\n\n"
    report += "🌍 GLOBAL NEWS SCANNER\n\n"
    report += "⚠ HIGH IMPACT NEWS\n\n"

    for i, news in enumerate(important_news[:5], start=1):
        report += f"{i}. {news[:120]}\n\n"

    # ==========================================
    # MAIN INTELLIGENCE BLOCK
    # (Coverage → Themes → Trending → Regime →
    #  Bias → Trade Quality → Trade → Stocks)
    # ==========================================
    report += format_telegram_output(top_scored)

    return report


if __name__ == "__main__":
    print("STARTING BOT...")

    try:
        report = generate_report()
        print("\nREPORT GENERATED\n")
        print(report)
        send_telegram_message(report)
        print("\nDONE")

    except Exception as e:
        print("\nERROR:")
        print(e)