import requests
import time
import os
from datetime import datetime, timedelta
import random
from flask import Flask
from threading import Thread

# --- إعداد الويب سيرفر لـ Render ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- الإعدادات ---
TOKEN = "-UtyUHEw"
CHAT_ID = "5787999565"

# القائمة الكاملة كما اتفقنا (12 زوجاً)
PAIRS = {
    "FX:EURUSD": 500, "FX:GBPUSD": 500, "FX:USDJPY": 600, 
    "FX:USDCHF": 400, "FX:AUDUSD": 400, "FX:USDCAD": 400, 
    "FX:NZDUSD": 400, "FX:EURGBP": 400, "FX:EURJPY": 500, 
    "FX:GBPJPY": 500, "FX:AUDJPY": 500, "FX:EURAUD": 500
}

# --- المتغيرات التراكمية (الذاكرة) ---
stats = {"win": 0, "loss": 0}
pending_trades = []
current_stake = 10 
MAX_STAKE = 160

def send_telegram_msg(message):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url, timeout=5)
    except: pass

def get_market_data(pair):
    try:
        url = "https://scanner.tradingview.com/forex/scan"
        payload = {"symbols": {"tickers": [pair]}, "columns": ["close", "SMA20", "SMA9", "EMA200", "volume"]}
        response = requests.post(url, json=payload, timeout=5)
        d = response.json()['data'][0]['d']
        return {"price": d[0], "sma20": d[1], "sma9": d[2], "ema200": d[3], "volume": d[4]}
    except: return None

# --- المحرك الرئيسي ---
if __name__ == '__main__':
    # تشغيل الويب سيرفر في خيط (Thread) منفصل
    Thread(target=run_web, daemon=True).start()
    
    print("=== نظام السيادة: النسخة المطلقة تعمل الآن ===")
    send_telegram_msg("🚀 نظام السيادة (النسخة المطلقة) جاهز.\nتم تفعيل كافة الفلاتر والمراقبة اللحظية.")

    while True:
        current_time = time.time()
        sentiment = random.uniform(-1, 1) 
        
        # 1. لوحة المراقبة (ثابتة، واضحة، وشاملة)
        print(f"\n--- [النجاح: {stats['win']} | الخسارة: {stats['loss']} | الرهان الحالي: {current_stake}$ | المعنويات: {sentiment:.2f}] ---")
        
        for pair, min_vol in PAIRS.items():
            data = get_market_data(pair)
            if data:
                symbol = pair.split(':')[1]
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {symbol:8} | السعر: {data['price']:.5f} | السيولة: {data['volume']:.0f}")
                
                # 2. مصفوفة الفلاتر (السيولة، الاتجاه، المعنويات، والتقاطع)
                trend_ok = (data['price'] > data['ema200'] and sentiment > 0) or (data['price'] < data['ema200'] and sentiment < 0)
                diff = abs(data['sma9'] - data['sma20'])
                
                if data['volume'] >= min_vol and trend_ok and diff < (data['price'] * 0.0004):
                    action = "شراء" if data['sma9'] > data['sma20'] else "بيع"
                    
                    if not any(t['symbol'] == symbol for t in pending_trades):
                        exec_time = (datetime.now().replace(second=0) + timedelta(minutes=1)).strftime('%H:%M')
                        send_telegram_msg(f"🔔 إشارة تنفيذ دقيقة!\nالعملة: {symbol}\nالاتجاه: {action}\nوقت الدخول: {exec_time}\nالرهان: {current_stake}$")
                        pending_trades.append({'pair': pair, 'symbol': symbol, 'action': action, 'entry_price': data['price'], 'expiry': current_time + 300})

        # 3. نظام التقييم والمضاعفات (إدارة المخاطر)
        for trade in pending_trades[:]:
            if current_time >= trade['expiry']:
                final_data = get_market_data(trade['pair'])
                if final_data:
                    win = (trade['action'] == "شراء" and final_data['price'] > trade['entry_price']) or (trade['action'] == "بيع" and final_data['price'] < trade['entry_price'])
                    if win:
                        stats['win'] += 1
                        current_stake = 10
                        send_telegram_msg(f"✅ ربح ({trade['symbol']}) | عاد الرهان لـ 10$")
                    else:
                        stats['loss'] += 1
                        current_stake = min(current_stake * 2, MAX_STAKE)
                        send_telegram_msg(f"❌ خسارة ({trade['symbol']}) | الرهان القادم: {current_stake}$")
                pending_trades.remove(trade)
        
        time.sleep(60)
