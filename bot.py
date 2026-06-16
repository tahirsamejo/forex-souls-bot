import requests
import schedule
import time
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
GEMINI_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

def get_gold_signal():
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={}".format(GEMINI_API_KEY)
    payload = {
        "contents": [{
            "parts": [{
                "text": "You are a professional XAUUSD trader. Generate a trading signal in plain text only, no emojis. Format exactly like this:\n\nXAUUSD SIGNAL\nDirection: BUY or SELL\nEntry Zone: price\nTP1: price\nTP2: price\nTP3: price\nStop Loss: price\nBias: Bearish or Bullish\nReason: explanation using terms like MSS, POI, SSL, liquidity\n\nWait for confirmation. Manage risk properly.\n#XAUUSD #Gold #ForexSignals #FOREX_SOULS"
            }]
        }]
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        print("API Response: {}".format(data))
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text
    except Exception as e:
        print("Error: {}".format(e))
        print("Full response: {}".format(response.text))
        return "Signal generation failed. Please try again."

def send_to_telegram(text):
    url = "https://api.telegram.org/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text
    }
    response = requests.post(url, json=payload)
    print("Sent: {}".format(response.status_code))

def post_signal():
    print("Generating signal...")
    signal = get_gold_signal()
    send_to_telegram(signal)
    print("Posted!")

schedule.every(1).hours.do(post_signal)
post_signal()

print("Bot running...")
while True:
    schedule.run_pending()
    time.sleep(60)
