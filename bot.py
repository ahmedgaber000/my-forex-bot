import requests
import time
from datetime import datetime, timedelta
import random
from flask import Flask
from threading import Thread
import os

# --- إعداد الخادم لـ Render ---
app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل!"
def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
Thread(target=run_web, daemon=True).start()

# --- الإعدادات ---
TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"
PAIRS = {
    "FX:EURUSD": 500, "FX:GBPUSD": 500, "FX:USDJPY": 600, 
    "FX:USDCHF": 400, "FX:AUDUSD": 400, "FX:USDCAD": 400, 
    "FX:NZDUSD": 400, "FX:EURGBP": 400, "FX:EURJPY": 500, 
    "FX:GBPJPY": 500, "FX:AUDJPY": 500, "FX:EURAUD": 500
}

stats = {"win": 0, "loss": 0}
current_stake = 10 
sentiment = 0

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except: pass

# --- نظام الاستماع للأوامر ---
def listen_to_telegram():
    last_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_id + 1}"
            resp = requests.get(url, timeout=10).json()
            if resp.get('result'):
                for update in resp['result']:
                    last_id = update['update_id']
                    if 'message' in update and update['message'].get('text') == '/stats':
                        msg = f"📊 إحصائيات النظام:\n✅ رابحة: {stats['win']}\n❌ خاسرة: {stats['loss']}\n💰 الرهان الحالي: {current_stake}$\n🧠 المعنوية: {sentiment:.2f}"
                        send_telegram_msg(msg)
        except: pass
        time.sleep(2)

Thread(target=listen_to_telegram, daemon=True).start()

# --- مراقبة السوق ---
def get_data(pair):
    try:
        url = "https://scanner.tradingview.com/forex/scan"
        payload = {"symbols": {"tickers": [pair]}, "columns": ["close", "volume"]}
        d = requests.post(url, json=payload, timeout=5).json()['data'][0]['d']
        return {"price": d[0], "volume": d[1]}
    except: return None

while True:
    sentiment = random.uniform(-1, 1)
    current_time = time.time()
    
    # فحص العملات
    for pair in PAIRS:
        data = get_data(pair)
        # (منطق المراقبة الخاص بك يعمل هنا...)
    
    time.sleep(60)
