# ==========================================
# STOCK SCORING ENGINE
# ==========================================

import json
import os
from datetime import date

STOCK_SCORES = {}
REASONS = {}

THEME_SCORES = {
    "AI":            0,
    "OIL_GAS":       0,
    "DEFENSE":       0,
    "BANKING":       0,
    "SEMICONDUCTOR": 0
}

THEME_REASONS = {
    "AI":            [],
    "OIL_GAS":       [],
    "DEFENSE":       [],
    "BANKING":       [],
    "SEMICONDUCTOR": []
}

MARKET_BIAS = "Neutral"

# ==========================================
# STOCK LIST
# ==========================================

ALL_STOCKS = [
    "ONGC", "IOC", "BPCL",
    "HPCL", "OIL", "GAIL",
    "RELIANCE",
    "HAL", "BEL", "BDL",
    "BEML", "GRSE",
    "COCHINSHIP", "MAZDOCK",
    "HDFCBANK", "ICICIBANK",
    "SBIN", "KOTAKBANK",
    "AXISBANK", "INDUSINDBK",
    "BANKBARODA", "PNB",
    "TCS", "INFY", "WIPRO",
    "HCLTECH", "TECHM",
    "LTIM", "PERSISTENT",
    "TATAELXSI",
    "DIXON", "KAYNES",
    "INDIGO", "SPICEJET",
    "ASIANPAINT", "BERGER"
]

for stock in ALL_STOCKS:
    STOCK_SCORES[stock] = 0

# ==========================================
# SECTORS
# ==========================================

OIL_GAS = [
    "ONGC", "IOC", "BPCL",
    "HPCL", "OIL", "GAIL",
    "RELIANCE"
]

DEFENSE = [
    "HAL", "BEL", "BDL",
    "BEML", "GRSE",
    "COCHINSHIP", "MAZDOCK"
]

BANKING = [
    "HDFCBANK", "ICICIBANK",
    "SBIN", "KOTAKBANK",
    "AXISBANK", "INDUSINDBK",
    "BANKBARODA", "PNB"
]

EMS = [
    "DIXON",
    "KAYNES"
]

AVIATION = [
    "INDIGO",
    "SPICEJET"
]

PAINTS = [
    "ASIANPAINT",
    "BERGER"
]

AI_IT = [
    "TECHM",
    "LTIM",
    "PERSISTENT",
    "TATAELXSI"
]

# ==========================================
# NOISE FILTER
# ==========================================

IGNORE_KEYWORDS = [
    "social security",
    "prime day",
    "shopping",
    "discount",
    "coupon",
    "celebrity",
    "entertainment",
    "retirement",
    "paper-wealthy",
    "paper wealthy",
    "lottery",
    "sports score",
    "box office",
    "album",
    "reality tv",
    "home decor",
    "recipe",
    "weather forecast",
    "horoscope",
    "uber lost",
    "lost items",
    "lifestyle",
    "movie"
]

def is_noise(title):
    t = title.lower()
    return any(word in t for word in IGNORE_KEYWORDS)

# ==========================================
# SOURCE WEIGHTS
# ==========================================

SOURCE_WEIGHTS = {
    "reuters":             3,
    "bloomberg":           3,
    "wsj":                 3,
    "wall street journal": 3,
    "financial times":     3,
    "ft":                  3,
    "cnbc":                2,
    "barron":              2,
    "economic times":      2,
    "mint":                2,
    "moneycontrol":        2,
    "yahoo":               1,
    "default":             1
}

def get_source_weight(source):
    if not source:
        return SOURCE_WEIGHTS["default"]
    s = source.lower()
    for key, weight in SOURCE_WEIGHTS.items():
        if key in s:
            return weight
    return SOURCE_WEIGHTS["default"]

# ==========================================
# THEME KEYWORD GROUPS
# ==========================================

AI_WORDS = [
    "openai", "anthropic", "chatgpt",
    "artificial intelligence", "ai-powered",
    "ai stocks", "ai fervor", "generative ai",
    "large language model", "llm", "ai chip",
    "ai demand", "ai infrastructure"
]

SEMICONDUCTOR_WORDS = [
    "chip", "chips", "semiconductor",
    "tsmc", "nvidia", "marvell",
    "amd", "intel", "fab",
    "wafer", "gpu", "foundry"
]

# TIGHTENED — no satellite/security/strategic
DEFENSE_WORDS = [
    "war",
    "missile",
    "military",
    "army",
    "navy",
    "air force",
    "defense",
    "defence",
    "fighter jet",
    "drone",
    "artillery",
    "weapon"
]

OIL_WORDS = [
    "oil", "crude", "opec",
    "iran", "israel", "petroleum",
    "energy prices", "refinery", "brent",
    "wti", "natural gas", "lng",
    "oil price", "crude price"
]

BANK_WORDS = [
    "fed", "powell", "inflation",
    "interest rate", "rate hike", "rate cut",
    "rbi", "repo rate", "liquidity",
    "monetary policy", "bond yield",
    "treasury yield", "10-year yield"
]

# ==========================================
# BIAS + RISK + MOOD MAPS
# ==========================================

BIAS_MAP = {
    "AI":            "Bullish IT",
    "SEMICONDUCTOR": "Bullish Electronics",
    "DEFENSE":       "Risk Off",
    "OIL_GAS":       "Energy Inflation",
    "BANKING":       "Banking Volatility"
}

MOOD_MAP = {
    "AI":            "RISK ON",
    "SEMICONDUCTOR": "RISK ON",
    "DEFENSE":       "RISK OFF",
    "OIL_GAS":       "RISK OFF",
    "BANKING":       "NEUTRAL"
}

RISK_MAP = {
    "DEFENSE":       "HIGH",
    "OIL_GAS":       "HIGH",
    "BANKING":       "MEDIUM",
    "AI":            "LOW",
    "SEMICONDUCTOR": "LOW"
}

SECTOR_LEADER = {
    "AI":            AI_IT,
    "SEMICONDUCTOR": EMS,
    "DEFENSE":       DEFENSE,
    "OIL_GAS":       OIL_GAS,
    "BANKING":       BANKING
}

# ==========================================
# SIGNAL GRADE ENGINE
# ==========================================

def get_signal_grade(max_score):
    if max_score >= 25:
        return "A+", "Very Strong", "High Conviction Trade"
    elif max_score >= 18:
        return "A",  "Strong",      "Trade with Confidence"
    elif max_score >= 12:
        return "B",  "Moderate",    "Trade with Caution"
    elif max_score >= 8:
        return "C",  "Weak",        "Reduce Position Size"
    else:
        return "D",  "Very Weak",   "Avoid Aggressive Trades"

def is_no_trade_day(ranked_stocks):
    if not ranked_stocks:
        return True
    return ranked_stocks[0][1] < 10  # lowered from 15 to 10

# ==========================================
# MULTI-DAY THEME MEMORY
# ==========================================

THEME_HISTORY_FILE = "theme_history.json"

def load_theme_history():
    if not os.path.exists(THEME_HISTORY_FILE):
        return {}
    try:
        with open(THEME_HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_theme_history():
    history = load_theme_history()
    today   = str(date.today())

    history[today] = {
        theme: score
        for theme, score in THEME_SCORES.items()
        if score > 0
    }

    # Keep only last 30 days
    keys = sorted(history.keys())
    if len(keys) > 30:
        for old_key in keys[:-30]:
            del history[old_key]

    try:
        with open(THEME_HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def get_theme_trends():
    history = load_theme_history()
    today   = str(date.today())

    # Exclude today from trend calc (not yet saved)
    past_days = sorted([d for d in history.keys() if d != today])

    if len(past_days) < 2:
        return {}

    trends = {}
    all_themes = list(THEME_SCORES.keys())

    for theme in all_themes:
        # Last 3 days scores
        recent = [
            history[d].get(theme, 0)
            for d in past_days[-3:]
        ]

        if len(recent) < 2:
            continue

        # Consecutive up/down streaks
        streak = 1
        direction = None

        for i in range(len(recent) - 1, 0, -1):
            if recent[i] > recent[i - 1]:
                if direction is None:
                    direction = "up"
                if direction == "up":
                    streak += 1
                else:
                    break
            elif recent[i] < recent[i - 1]:
                if direction is None:
                    direction = "down"
                if direction == "down":
                    streak += 1
                else:
                    break
            else:
                break

        if direction == "up" and streak >= 2:
            trends[theme] = f"↑ {streak} days in a row"
        elif direction == "down" and streak >= 2:
            trends[theme] = f"↓ weakening ({streak} days)"
        elif recent[-1] == 0 and any(s > 0 for s in recent[:-1]):
            trends[theme] = "→ faded today"

    return trends

# ==========================================
# REASON ENGINE
# ==========================================

def add_reason(stock, reason):
    if stock not in REASONS:
        REASONS[stock] = []
    if reason not in REASONS[stock]:
        REASONS[stock].append(reason)

def add_theme_reason(theme, title):
    if theme not in THEME_REASONS:
        return
    short_title = title[:120]
    if short_title not in THEME_REASONS[theme]:
        THEME_REASONS[theme].append(short_title)

# ==========================================
# MARKET BIAS
# ==========================================

def set_market_bias(bias):
    global MARKET_BIAS
    MARKET_BIAS = bias

def get_market_bias():
    return MARKET_BIAS

# ==========================================
# CONFIDENCE ENGINE
# ==========================================

def get_confidence(score):
    return min(50 + score * 3, 95)

# ==========================================
# MARKET IMPACT — THEME VOTING ENGINE
# ==========================================

def analyze_market_impact(title, source=None):
    if is_noise(title):
        return "Filtered"

    t      = title.lower()
    weight = get_source_weight(source)

    local_scores = {
        "AI":            0,
        "SEMICONDUCTOR": 0,
        "DEFENSE":       0,
        "OIL_GAS":       0,
        "BANKING":       0
    }

    for word in AI_WORDS:
        if word in t:
            local_scores["AI"] += 1

    for word in SEMICONDUCTOR_WORDS:
        if word in t:
            local_scores["SEMICONDUCTOR"] += 1

    for word in DEFENSE_WORDS:
        if word in t:
            local_scores["DEFENSE"] += 1

    for word in OIL_WORDS:
        if word in t:
            local_scores["OIL_GAS"] += 1

    for word in BANK_WORDS:
        if word in t:
            local_scores["BANKING"] += 1

    best_score = max(local_scores.values())
    if best_score == 0:
        return "Neutral"

    best_theme = max(local_scores, key=local_scores.get)

    THEME_SCORES[best_theme] += weight
    add_theme_reason(best_theme, title)

    if best_theme == "OIL_GAS":
        set_market_bias("Energy Inflation")
        for stock in OIL_GAS:
            STOCK_SCORES[stock] += 6 * weight
            add_reason(stock, "Oil prices rising due to geopolitical tensions")
        for stock in AVIATION:
            STOCK_SCORES[stock] -= 4 * weight
            add_reason(stock, "Higher fuel cost pressure")
        for stock in PAINTS:
            STOCK_SCORES[stock] -= 3 * weight
            add_reason(stock, "Crude-linked raw material cost risk")
        return "Oil Theme"

    elif best_theme == "BANKING":
        set_market_bias("Banking Volatility")
        for stock in BANKING:
            STOCK_SCORES[stock] += 5 * weight
            add_reason(stock, "Interest-rate related banking impact")
        return "Banking Theme"

    elif best_theme == "DEFENSE":
        set_market_bias("Risk Off")
        for stock in DEFENSE:
            STOCK_SCORES[stock] += 6 * weight
            add_reason(stock, "Defense theme gaining momentum")
        return "Defense Theme"

    elif best_theme == "SEMICONDUCTOR":
        set_market_bias("Bullish Electronics")
        for stock in EMS:
            STOCK_SCORES[stock] += 6 * weight
            add_reason(stock, "Semiconductor demand theme")
        return "Semiconductor Theme"

    elif best_theme == "AI":
        set_market_bias("Bullish IT")
        for stock in AI_IT:
            STOCK_SCORES[stock] += 6 * weight
            add_reason(stock, "AI adoption and software demand")
        return "AI Theme"

    return "Neutral"

# ==========================================
# THEME RANKING
# ==========================================

def get_top_themes():
    return sorted(
        THEME_SCORES.items(),
        key=lambda x: x[1],
        reverse=True
    )

# ==========================================
# MARKET INTELLIGENCE ENGINE
# ==========================================

def get_market_intelligence():
    ranked = get_top_themes()
    active = [(t, s) for t, s in ranked if s > 0]

    if not active:
        return {
            "primary_theme":   "None",
            "secondary_theme": "None",
            "market_mood":     "NEUTRAL",
            "risk_level":      "LOW",
            "market_bias":     "Neutral",
            "confidence":      50
        }

    primary   = active[0][0]
    secondary = active[1][0] if len(active) > 1 else "None"

    total      = sum(s for _, s in active)
    dominance  = active[0][1] / total if total else 0
    confidence = int(min(50 + dominance * 45, 95))

    return {
        "primary_theme":   primary,
        "secondary_theme": secondary,
        "market_mood":     MOOD_MAP.get(primary, "NEUTRAL"),
        "risk_level":      RISK_MAP.get(primary, "LOW"),
        "market_bias":     BIAS_MAP.get(primary, "Neutral"),
        "confidence":      confidence
    }

# ==========================================
# MARKET REGIME ENGINE
# ==========================================

def get_market_regime(intel, total_theme_hits):
    primary = intel["primary_theme"]

    if total_theme_hits == 0:
        return {
            "mode":        "No Theme",
            "dominant":    "None",
            "risk":        "Unknown",
            "environment": "Avoid Trading",
            "market_mood": "NO TRADE",
            "risk_level":  "VERY LOW"
        }
    elif total_theme_hits >= 5:
        mode = "High Conviction"
        env  = "Aggressive"
    elif total_theme_hits >= 3:
        mode = "Theme Driven"
        env  = "Selective"
    else:
        mode = "Thin Coverage"
        env  = "Cautious"

    risk = RISK_MAP.get(primary, "LOW")

    # =====================================
    # MARKET MOOD ENGINE
    # Based on top theme weighted score
    # =====================================
    top_theme_score = max(THEME_SCORES.values()) if THEME_SCORES else 0

    if top_theme_score < 20:
        market_mood = "NO TRADE"
        risk_level  = "VERY LOW"
    elif top_theme_score < 80:
        market_mood = "SELECTIVE"
        risk_level  = "LOW"
    elif top_theme_score < 150:
        market_mood = "ACTIVE"
        risk_level  = "MEDIUM"
    else:
        market_mood = "TRENDING"
        risk_level  = "HIGH"

    return {
        "mode":        mode,
        "dominant":    primary,
        "risk":        risk,
        "environment": env,
        "market_mood": market_mood,
        "risk_level":  risk_level
    }

# ==========================================
# NEWS COVERAGE ENGINE
# ==========================================

def get_news_coverage():
    active = [(t, s) for t, s in get_top_themes() if s > 0]
    total  = sum(s for _, s in active)

    if total >= 6:
        quality = "HIGH"
    elif total >= 3:
        quality = "MEDIUM"
    else:
        quality = "LOW"

    return {
        "strong_themes": len(active),
        "total_hits":    total,
        "quality":       quality
    }

# ==========================================
# TRADE OF THE DAY ENGINE
# ==========================================

def get_trade_of_the_day():
    ranked = get_top_themes()
    active = [(t, s) for t, s in ranked if s > 0]

    if not active:
        return None

    top_theme      = active[0][0]
    theme_strength = active[0][1]
    sector         = SECTOR_LEADER.get(top_theme, [])

    leader      = max(sector, key=lambda s: STOCK_SCORES.get(s, 0)) if sector else "N/A"
    stock_score = STOCK_SCORES.get(leader, 0)
    probability = get_confidence(stock_score)

    reasons = []
    reasons.append(f"{top_theme} strongest theme today")
    if theme_strength >= 2:
        reasons.append(f"{theme_strength} supporting headlines")
    reasons += (REASONS.get(leader, []))[:2]

    return {
        "theme":          top_theme,
        "leader":         leader,
        "theme_strength": theme_strength,
        "probability":    probability,
        "reasons":        reasons[:4]
    }

# ==========================================
# TELEGRAM FORMATTER
# ==========================================

def format_telegram_output(top_stocks):
    intel         = get_market_intelligence()
    trade         = get_trade_of_the_day()
    ranked_themes = get_top_themes()
    coverage      = get_news_coverage()
    regime        = get_market_regime(intel, coverage["total_hits"])
    trends        = get_theme_trends()

    max_score  = top_stocks[0][1] if top_stocks else 0
    no_trade   = is_no_trade_day(top_stocks)
    grade, strength, recommendation = get_signal_grade(max_score)

    THEME_LABELS = {
        "AI":            "AI / IT",
        "SEMICONDUCTOR": "Semiconductor",
        "DEFENSE":       "Defense",
        "OIL_GAS":       "Oil & Gas",
        "BANKING":       "Banking"
    }

    lines  = []
    medals = ["🥇", "🥈", "🥉"]

    # --- News Coverage ---
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("📰 NEWS COVERAGE")
    lines.append("")
    lines.append(f"Strong Themes: {coverage['strong_themes']}")
    lines.append(f"Market Impact News: {coverage['total_hits']}")
    lines.append(f"Coverage Quality: {coverage['quality']}")

    # --- Theme Strength ---
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("📊 THEME STRENGTH")
    lines.append("")

    active_themes = [(t, s) for t, s in ranked_themes if s > 0]

    for i, (theme, score) in enumerate(active_themes[:5]):
        medal = medals[i] if i < 3 else "  "
        label = THEME_LABELS.get(theme, theme)
        unit  = "headline" if score == 1 else "headlines"
        lines.append(f"{medal} {label}: {score} {unit}")

    if not active_themes:
        lines.append("No strong themes detected.")

    # --- Trending Themes (multi-day memory) ---
    if trends:
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━")
        lines.append("🔥 TRENDING THEMES")
        lines.append("")
        for theme, trend_str in trends.items():
            label = THEME_LABELS.get(theme, theme)
            lines.append(f"{label}: {trend_str}")

    # --- Market Regime ---
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("🌐 MARKET REGIME")
    lines.append("")
    lines.append(f"Mode:\n{regime['mode']}")
    lines.append("")
    lines.append(f"Dominant Theme:\n{regime['dominant']}")
    lines.append("")
    lines.append(f"Risk:\n{regime['risk']}")
    lines.append("")
    lines.append(f"Trading Environment:\n{regime['environment']}")

    # --- Market Bias ---
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("📈 MARKET BIAS")
    lines.append("")
    lines.append(f"Primary Theme:\n{intel['primary_theme']}")
    lines.append("")
    lines.append(f"Secondary Theme:\n{intel['secondary_theme']}")
    lines.append("")
    lines.append(f"Market Mood:\n{intel['market_mood']}")
    lines.append("")
    lines.append(f"Risk Level:\n{intel['risk_level']}")
    lines.append("")
    lines.append(f"Market Bias:\n{intel['market_bias']}")
    lines.append("")
    lines.append(f"Confidence:\n{intel['confidence']}%")

    # --- Trade Quality ---
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("🎯 TRADE QUALITY")
    lines.append("")
    lines.append(f"Signal Grade: {grade}")
    lines.append("")
    lines.append(f"Signal Strength: {strength}")
    lines.append("")

    if no_trade:
        lines.append("Recommendation:\nNO TRADE DAY")
        lines.append("")
        lines.append("Reason:\nNo theme has enough strength.")
        lines.append("")
        lines.append("Confidence:\n75%")
    else:
        lines.append(f"Recommendation:\n{recommendation}")

        if trade and trade["leader"] != "N/A":
            lines.append("")
            lines.append("━━━━━━━━━━━━━━━")
            lines.append("🏆 TRADE OF THE DAY")
            lines.append("")
            lines.append(f"Theme:\n{trade['theme']}")
            lines.append("")
            lines.append(f"Leader:\n{trade['leader']}")
            lines.append("")
            lines.append(f"Theme Strength:\n{trade['theme_strength']} headlines")
            lines.append("")
            lines.append(f"Grade:\n{grade}")
            lines.append("")
            lines.append(f"Confidence:\n{trade['probability']}%")
            if trade["reasons"]:
                lines.append("")
                lines.append("Why:")
                for r in trade["reasons"]:
                    lines.append(f"• {r}")

    # --- Top Stocks ---
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")
    lines.append("📋 TOP STOCKS")
    lines.append("")

    shown = 0
    for i, (stock, score) in enumerate(top_stocks[:10]):
        if score <= 0:
            continue
        conf                      = get_confidence(score)
        sg, _, _                  = get_signal_grade(score)
        medal                     = medals[i] if i < 3 else f"{i+1}."
        reasons                   = REASONS.get(stock, [])
        reason_str                = f"\n   ↳ {reasons[0]}" if reasons else ""
        lines.append(
            f"{medal} {stock} | Grade: {sg} | Score: {score} | {conf}%{reason_str}"
        )
        shown += 1

    if shown == 0:
        lines.append("No scored stocks today.")

    lines.append("")
    lines.append("━━━━━━━━━━━━━━━")

    # Save today's theme scores to history AFTER formatting
    save_theme_history()

    return "\n".join(lines)