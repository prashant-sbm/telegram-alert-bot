def detect_theme(title):

    title = title.lower()

    if any(word in title for word in [
        "war",
        "missile",
        "army",
        "navy",
        "defense",
        "defence"
    ]):
        return "DEFENSE"

    elif any(word in title for word in [
        "oil",
        "crude",
        "iran",
        "opec",
        "energy"
    ]):
        return "OIL_GAS"

    elif any(word in title for word in [
        "fed",
        "powell",
        "inflation",
        "interest rate"
    ]):
        return "BANKING"

    elif any(word in title for word in [
        "openai",
        "anthropic",
        "chatgpt",
        "ai"
    ]):
        return "AI_TECH"

    elif any(word in title for word in [
        "chip",
        "semiconductor",
        "taiwan"
    ]):
        return "ELECTRONICS"

    return None