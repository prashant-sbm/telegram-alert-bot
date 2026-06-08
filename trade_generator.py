def generate_trade_setup(title):

    title = title.lower()

    # OIL / WAR NEWS

    if any(word in title for word in [
        "iran",
        "israel",
        "war",
        "oil",
        "crude"
    ]):

        return """
🏆 TOP OPPORTUNITIES

1. ONGC
Reason: Higher crude prices

2. RELIANCE
Reason: Energy strength

3. GAIL
Reason: Gas sector momentum

4. HPCL
Reason: Oil supply disruption

5. IOC
Reason: Refining theme

Confidence: 82%
Holding: 1-3 Days
"""

    # FED / RATE NEWS

    elif any(word in title for word in [
        "fed",
        "powell",
        "interest rate",
        "inflation",
        "rate"
    ]):

        return """
🏆 TOP OPPORTUNITIES

1. SBIN
Reason: Banking momentum

2. HDFCBANK
Reason: Strong financials

3. ICICIBANK
Reason: Rate sensitivity

4. AXISBANK
Reason: Sector strength

5. KOTAKBANK
Reason: Banking theme

Confidence: 75%
Holding: 1-5 Days
"""

    # CHINA / CHIP NEWS

    elif any(word in title for word in [
        "china",
        "taiwan",
        "semiconductor",
        "chip"
    ]):

        return """
🏆 TOP OPPORTUNITIES

1. DIXON
Reason: Electronics manufacturing

2. KAYNES
Reason: EMS demand

3. TATAELXSI
Reason: Technology theme

4. BEL
Reason: Strategic electronics

5. HAL
Reason: Defense electronics

Confidence: 70%
Holding: 2-7 Days
"""

    return ""