import requests
import time
from datetime import datetime, timedelta
import random
import os
from flask import Flask
from threading import Thread

# 1. إعدادات التليجرام
TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# 2. إعداد خادم الويب (ليظل البوت نشطاً على Render)
app = Flask(__name__)
@app.route('/')
def home(): return "نظام السيادة يعمل بكامل طاقته!"

# 3. دالة إرسال التليجرام
def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except: pass

# 4. دالة جلب البيانات (الأسعار والسيولة)
def get_market_data(pair):
    try:
        url = "https://scanner.tradingview.com/forex/scan"
        payload = {"symbols": {"tickers": [pair]}, "columns": ["close", "SMA20", "SMA9", "EMA200", "volume"]}
        response = requests.post(url, json=payload, timeout=5)
        d = response.json()['data'][0]['d']
        return {"price": d[0], "sma20": d[1], "sma9": d[2], "ema200": d[3], "volume": d[4]}
    except: return None

# 5. منطق التداول (الدالة التي طلبتها)
def run_trading_bot():
    PAIRS = {"FX:EURUSD": 500, "FX:GBPUSD": 500, "FX:USDJPY": 600, "FX:USDCHF": 400, "FX:AUDUSD": 400, "FX:USDCAD": 400, "FX:NZDUSD": 400, "FX:EURGBP": 400, "FX:EURJPY": 500, "FX:GBPJPY": 500, "FX:AUDJPY": 500, "FX:EURAUD": 500}
    stats = {"win": 0, "loss": 0}
    pending_trades = []
    current_stake = 10 
    MAX_STAKE = 160
    
    send_telegram_msg("🚀 نظام السيادة (النسخة السحابية) بدأ العمل.")
    
    while True:
        current_time = time.time()
        sentiment = random.uniform(-1, 1) 
        
        for pair, min_vol in PAIRS.items():
            data = get_market_data(pair)
            if data:
                symbol = pair.split(':')[1]
                trend_ok = (data['price'] > data['ema200'] and sentiment > 0) or (data['price'] < data['ema200'] and sentiment < 0)
                diff = abs(data['sma9'] - data['sma20'])
                
                if data['volume'] >= min_vol and trend_ok and diff < (data['price'] * 0.0004):
                    action = "شراء" if data['sma9'] > data['sma20'] else "بيع"
                    if not any(t['symbol'] == symbol for t in pending_trades):
                        send_telegram_msg(f"🔔 إشارة تنفيذ!\nالعملة: {symbol}\nالاتجاه: {action}\nالرهان: {current_stake}$")
                        pending_trades.append({'pair': pair, 'symbol': symbol, 'action': action, 'entry_price': data['price'], 'expiry': current_time + 300})

        for trade in pending_trades[:]:
            if current_time >= trade['expiry']:
                final_data = get_market_data(trade['pair'])
                if final_data:
                    win = (trade['action'] == "شراء" and final_data['price'] > trade['entry_price']) or (trade['action'] == "بيع" and final_data['price'] < trade['entry_price'])
                    if win:
                        stats['win'] += 1
                        current_stake = 10
                        send_telegram_msg(f"✅ ربح ({trade['symbol']}) | رصيد الأرباح: {stats['win']}")
                    else:
                        stats['loss'] += 1
                        current_stake = min(current_stake * 2, MAX_STAKE)
                        send_telegram_msg(f"❌ خسارة ({trade['symbol']}) | الرهان القادم: {current_stake}$")
                pending_trades.remove(trade)
        time.sleep(60)

# 6. تشغيل النظامين معاً (خادم الويب + البوت)
if __name__ == '__main__':
    Thread(target=run_trading_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
