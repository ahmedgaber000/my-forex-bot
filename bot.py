import requests
import time
import random
from flask import Flask
from threading import Thread
import os

# --- إعداد الخادم ---
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
stats = {"win": 0, "loss": 0}
current_stake = 10 
sentiment = 0

def send_msg(text):
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")
    except: pass

# --- رسالة الترحيب ---
send_msg("🚀 نظام السيادة يعمل الآن!")

# --- الحلقة الرئيسية ---
while True:
    try:
        # 1. فحص أوامر تليجرام أولاً
        updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=1&offset=-1", timeout=5).json()
        if updates.get('result'):
            msg = updates['result'][0]['message']
            if msg.get('text') == '/stats':
                send_msg(f"📊 الإحصائيات:\n✅ رابح: {stats['win']}\n❌ خاسر: {stats['loss']}\n💰 الرهان: {current_stake}$")
    except: pass

    # 2. مراقبة السوق (كود المراقبة الخاص بك)
    sentiment = random.uniform(-1, 1)
    # هنا سيتم تنفيذ كودك المعتاد لمراقبة العملات ...
    
    time.sleep(30) # البوت سيفحص الأوامر والسوق كل 30 ثانية
