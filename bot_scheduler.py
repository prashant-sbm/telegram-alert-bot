import schedule
import time
import market_report_bot


# ==========================================
# ALERT 1 - PRE MARKET REPORT
# ==========================================

def morning_report():

    try:

        print("Running Morning Report...")

        report = market_report_bot.generate_report()

        market_report_bot.send_telegram_message(report)

        print("Morning Report Sent")

    except Exception as e:

        print("Morning Report Error:", e)


# ==========================================
# ALERT 2 - MARKET OPEN REMINDER
# ==========================================

def market_open_alert():

    try:

        message = """
🔔 MARKET OPEN ALERT

Market Opened

Focus on:

✅ Top Themes
✅ Top Ranked Stocks
✅ Opening Range High

Wait for confirmation before entry.
"""

        market_report_bot.send_telegram_message(message)

        print("Market Open Alert Sent")

    except Exception as e:

        print("Market Open Alert Error:", e)


# ==========================================
# ALERT 3 - THEME UPDATE
# ==========================================

def theme_update():

    try:

        report = market_report_bot.generate_report()

        message = (
            "📈 MID-DAY THEME UPDATE\n\n"
            "Re-evaluating market themes...\n\n"
            + report[:2000]
        )

        market_report_bot.send_telegram_message(message)

        print("Theme Update Sent")

    except Exception as e:

        print("Theme Update Error:", e)


# ==========================================
# ALERT 4 - MOMENTUM WATCH
# ==========================================

def momentum_alert():

    try:

        message = """
🚀 MOMENTUM CHECK

Review Top Opportunities:

• Check strongest theme
• Check top ranked stocks
• Avoid weak sectors

Look for breakout continuation setups.
"""

        market_report_bot.send_telegram_message(message)

        print("Momentum Alert Sent")

    except Exception as e:

        print("Momentum Alert Error:", e)


# ==========================================
# ALERT 5 - MARKET CLOSE REPORT
# ==========================================

def closing_report():

    try:

        report = market_report_bot.generate_report()

        message = (
            "📋 MARKET CLOSE REPORT\n\n"
            + report[:2500]
        )

        market_report_bot.send_telegram_message(message)

        print("Closing Report Sent")

    except Exception as e:

        print("Closing Report Error:", e)


# ==========================================
# STARTUP MESSAGE
# ==========================================

try:

    market_report_bot.send_telegram_message(
        "🤖 Scheduler Started Successfully"
    )

except Exception as e:

    print("Startup Message Error:", e)


# ==========================================
# SCHEDULES
# ==========================================

# PRE-MARKET REPORT
schedule.every().day.at("08:45").do(
    morning_report
)

# MARKET OPEN ALERT
schedule.every().day.at("09:20").do(
    market_open_alert
)

# MID-DAY THEME UPDATE
schedule.every().day.at("11:00").do(
    theme_update
)

# MOMENTUM CHECK
schedule.every().day.at("14:30").do(
    momentum_alert
)

# CLOSING REPORT
schedule.every().day.at("15:10").do(
    closing_report
)

print("=================================")
print("BOT SCHEDULER RUNNING")
print("08:45 PRE-MARKET REPORT")
print("09:20 MARKET OPEN ALERT")
print("11:00 THEME UPDATE")
print("14:30 MOMENTUM ALERT")
print("15:10 CLOSING REPORT")
print("=================================")

while True:

    schedule.run_pending()

    time.sleep(30)