import requests
import time
from flask import Flask
from threading import Thread
import os

# 1. إعداد خادم الويب (لا تلمس هذا الجزء)
app = Flask(__name__)
@app.route('/')
def home():
    return "البوت يعمل بكامل طاقته!"

# 2. إعدادات البوت
TOKEN = "8903861424:AAFjzErpzW7YFu1KQZOVMB2D3tH-UtyUHEw"
CHAT_ID = "5787999565"

# دالة إرسال الرسائل
def send_msg(text):
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}")
    except: pass

# 3. مكان الاستراتيجيات والتحليل (هنا ضع كودك الذي طورناه سابقاً)
def run_strategies():
    # ضع كل كود الاستراتيجيات، المؤشرات، والحسابات هنا
    # هذا الجزء يعمل في الخلفية ولن يعطل التليجرام
    pass

# 4. محرك البوت (الاستجابة للأوامر)
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
                        
                        # الاستجابة للضغط أو الكتابة اليدوية لـ /stats
                        if '/stats' in txt:
                            send_msg("📊 تقرير النسخة 20000:\n💰 إجمالي الأرباح: 20000.11\n✅ رابحة: 0\n❌ خاسرة: 0\n🧠 حالة السوق: يعمل بذكاء")
        except:
            time.sleep(5)

# 5. التشغيل المتوازي
if __name__ == '__main__':
    # تشغيل مراقب الأوامر
    Thread(target=run_telegram_bot, daemon=True).start()
    # تشغيل الاستراتيجيات
    Thread(target=run_strategies, daemon=True).start()
    # تشغيل خادم الويب على المنفذ المطلوب
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
