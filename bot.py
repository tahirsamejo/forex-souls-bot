import anthropic
import requests
import schedule
import time
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def get_gold_signal():
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": """You are a professional gold (XAUUSD) trader. 
                Generate a realistic trading signal for XAUUSD right now.
                
                Format it EXACTLY like this:
                
📊 XAUUSD SIGNAL

🔴 SELL / 🟢 BUY: [choose one]
📍 Entry Zone: [price range]
🎯 TP1: [price]
🎯 TP2: [price]  
🎯 TP3: [price]
🛑 Stop Loss: [price]
📈 Bias: [Bearish/Bullish]

💡 Reason: [2-3 lines explanation using technical terms like MSS, POI, SSL, liquidity, etc]

⚠️ Wait for confirmation. Manage risk properly.

#XAUUSD #Gold #ForexSignals #FOREX_SOULS"""
            }
        ]
    )
    return message.content[0].text

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, json=payload)
    print(f"Sent: {response.status_code}")

def post_signal():
    print("Generating signal...")
    signal = get_gold_signal()
    send_to_telegram(signal)
    print("Posted!")

# Post every hour
schedule.every(1).hours.do(post_signal)

# Post immediately on start
post_signal()

print("Bot running...")
while True:
    schedule.run_pending()
    time.sleep(60)
