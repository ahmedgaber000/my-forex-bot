import requests
import time
from flask import Flask
from threading import Thread
import os

# 1. إعداد خادم الويب (للـ Render)
app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل بكامل طاقته!"
Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# 2. الإعدادات والتوكن
TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# دالة إرسال الرسائل
def send_msg(text):
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")
    except: pass

# 3. حارس الأوامر (يستجيب لـ /stats دون تعطيل الاستراتيجيات)
def check_telegram_commands():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?limit=1&offset=-1"
        res = requests.get(url, timeout=2).json()
        if res.get('result'):
            msg = res['result'][0]['message'].get('text')
            if msg == '/stats':
                # هنا سيتم عرض إحصائياتك (20000.11)
                send_msg(f"📊 تقرير النسخة 20000:\n💰 إجمالي الأرباح: 20000.11\n✅ رابحة: 0\n❌ خاسرة: 0\n🧠 حالة السوق: مستقر")
    except: pass

# 4. كود الاستراتيجيات والتحليل (هنا تضع كل ما طورته سابقاً)
def run_strategies():
    # ضع كود التحليلات والاستراتيجيات الخاص بك هنا
    # البوت سيقوم بتنفيذ هذا الكود في كل دورة
    pass

# 5. الدورة الرئيسية (المحرك)
send_msg("🚀 نظام السيادة (النسخة 20000.11) يعمل الآن بكامل استراتيجياته.")

while True:
    # أ- فحص الأوامر
    check_telegram_commands()
    
    # ب- تشغيل استراتيجياتك
    run_strategies()
    
    # ج- الانتظار بين الدورات
    time.sleep(1)
