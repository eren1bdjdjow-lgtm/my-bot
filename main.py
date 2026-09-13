main.py
import os
import requests
import telebot
from flask import Flask

app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

API_TOKEN = '8848035868:AAGv6fFzztbu8q42YEVhiG5J9DZUWs0wk94'
bot = telebot.TeleBot(API_TOKEN)
CHANNEL_ID = '@dhdkskwb' 

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"تنبيه الاشتراك: {e}")
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_subscribed(user_id):
        bot.reply_to(message, "⚠️ أهلاً بك! أرسل رابط تيك توك للتحميل بدون علامة مائية مباشرة.")
    else:
        bot.reply_to(message, f"❌ يجب الاشتراك في القناة أولاً لاستخدام البوت:\nhttps://t.me\n\nأرسل /start بعد الاشتراك.")

@bot.message_handler(func=lambda message: "tiktok.com" in message.text)
def download_tiktok(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        bot.reply_to(message, f"❌ يجب الاشتراك في القناة أولاً:\nhttps://t.me")
        return
    url = message.text
    bot.reply_to(message, "⏳ جاري جلب الفيديو بدون علامة مائية...")
    api_url = f"https://tikwm.com{url}"
    try:
        response = requests.get(api_url).json()
        if response.get('code') == 0:
            video_url = response['data']['play']
            caption = response['data'].get('title', 'تم التحميل بنجاح!')
            bot.send_video(message.chat.id, video_url, caption=f"🎬 {caption}")
        else:
            bot.reply_to(message, "❌ فشل استخراج الفيديو. تأكد أن الرابط صحيح.")
    except Exception as e:
        bot.reply_to(message, "❌ حدث خطأ، أعد المحاولة لاحقاً.")

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: bot.polling(none_stop=True)).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
