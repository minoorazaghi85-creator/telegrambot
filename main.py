import os
import threading
from flask import Flask
import telebot

app = Flask(__name__)

# دریافت توکن از متغیرهای محیطی رندر
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN environment variable not set!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

@app.route('/')
def index():
    return "I'm alive!"

@app.route('/health')
def health():
    return "OK", 200

# --- منطق ربات تلگرام (در یک Thread جداگانه) ---
@bot.message_handler(content_types=['document', 'video'])
def handle_file(message):
    try:
        file_id = None
        if message.document:
            file_id = message.document.file_id
        elif message.video:
            file_id = message.video.file_id

        if not file_id:
            bot.reply_to(message, "❌ فایل نامعتبره")
            return

        file_info = bot.get_file(file_id)
        download_link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        bot.reply_to(message, f"📥 لینک دانلود:\n{download_link}")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا در پردازش:\n{e}")
# --- پایان منطق ربات ---

def run_bot():
    """تابعی برای اجرای ربات در یک Thread جداگانه"""
    print("🤖 Starting Telegram bot polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # اجرای ربات در یک Thread مجزا
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    # دریافت پورت از متغیر محیطی Render (پیش‌فرض: 10000)
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Starting Flask server on port {port}...")
    # سرور Flask را برای Render روشن نگه می‌دارد
    app.run(host="0.0.0.0", port=port)
