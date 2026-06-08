def get_trade_grade(score):

    if score >= 25:
        return "A+"

    elif score >= 18:
        return "A"

    elif score >= 12:
        return "B"

    elif score >= 8:
        return "C"

    return "D"


def should_trade(score):

    return score >= 10