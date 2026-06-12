import requests
import time
import os
from flask import Flask
from threading import Thread

# إعدادات البوت
TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# إرسال رسالة الترحيب فوراً عند بدء التشغيل
try:
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=🚀 النظام الآن يعمل (النسخة 20000).")
except: pass

app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل بكامل طاقته!"

# دالة مراقبة الأوامر
def run_telegram_bot():
    last_update_id = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
            res = requests.get(url, timeout=40).json()
            if res.get('result'):
                for update in res['result']:
                    last_update_id = update['update_id']
                    if 'message' in update and 'text' in update['message']:
                        txt = update['message']['text'].strip().lower()
                        if '/stats' in txt:
                            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=📊 إحصائيات النظام:\n💰 الأرباح: 20000.11\n✅ رابحة: 0\n❌ خاسرة: 0")
        except:
            time.sleep(5)

if __name__ == '__main__':
    Thread(target=run_telegram_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
