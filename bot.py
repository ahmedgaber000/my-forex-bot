import requests
import time
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل بكامل طاقته!"

# تشغيل خادم الويب (لضمان بقاء البوت حياً على Render)
Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# --- المتغيرات التي طورتها أنت (النسخة 20000) ---
stats = {"win": 0, "loss": 0, "total_profit": 20000.11}
current_stake = 10 
sentiment = "مستقر"

def send_msg(text):
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")
    except: pass

# --- الدورة الرئيسية ---
last_update_id = 0
send_msg("🚀 نظام السيادة (النسخة 20000.11) يعمل الآن.")

while True:
    try:
        # 1. منطق التداول الخاص بك (هنا يتم تحديث الإحصائيات)
        # (أضف هنا كود مراقبة السوق الخاص بك)
        
        # 2. فحص أوامر تليجرام
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
        res = requests.get(url, timeout=40).json()
        
        if res.get('result'):
            for update in res['result']:
                last_update_id = update['update_id']
                if 'message' in update and 'text' in update['message']:
                    if update['message']['text'] == '/stats':
                        # هذا هو التقرير الذي يظهر كل ما طورناه
                        report = (
                            f"📊 تقرير نظام السيادة:\n"
                            f"------------------------\n"
                            f"💰 إجمالي الأرباح: {stats['total_profit']}\n"
                            f"✅ الصفقات الرابحة: {stats['win']}\n"
                            f"❌ الصفقات الخاسرة: {stats['loss']}\n"
                            f"🧠 حالة السوق: {sentiment}\n"
                            f"💸 الرهان الحالي: {current_stake}$"
                        )
                        send_msg(report)
    except:
        time.sleep(5)
    
    time.sleep(1)
