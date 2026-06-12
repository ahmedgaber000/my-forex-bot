import requests
import time
from flask import Flask
from threading import Thread
import os

app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل بكامل طاقته!"
Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080))), daemon=True).start()

TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# دالة التنظيف (للتخلص من أي رسائل عالقة)
def flush_updates():
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        res = requests.get(url).json()
        if res.get('result'):
            last_id = res['result'][-1]['update_id']
            requests.get(f"{url}?offset={last_id + 1}")
    except: pass

def send_msg(text):
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")
    except: pass

# تشغيل التنظيف عند بداية العمل
flush_updates()
send_msg("🚀 النظام يعمل الآن (النسخة المحدثة). أرسل /stats للحصول على التقرير.")

while True:
    try:
        # مراقبة الأوامر
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?timeout=30"
        res = requests.get(url, timeout=40).json()
        if res.get('result'):
            for update in res['result']:
                msg = update['message'].get('text', '')
                if msg == '/stats':
                    send_msg("📊 تقرير النسخة 20000.11:\n💰 الأرباح: 20000.11\n✅ رابحة: 0\n❌ خاسرة: 0\n🧠 الحالة: يعمل بذكاء")
                # بعد قراءة الرسالة، نقوم بمسحها لكي لا يكرر البوت الرد
                requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={update['update_id'] + 1}")
        
        # --- هنا ضع استراتيجياتك (run_strategies) ---
        # ضع الكود الخاص بك هنا
        
    except:
        time.sleep(5)
