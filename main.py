import os
import telebot

print("🚀 Starting bot...")

# ✅ درست: خواندن توکن از متغیر محیطی به نام BOT_TOKEN
BOT_TOKEN = os.getenv("8276989335:AAEMMygR7yaUlCV7WhMoI0WP6u5wf2MiOls")

print("DEBUG BOT_TOKEN:", BOT_TOKEN)

if not BOT_TOKEN:
    print("❌ BOT_TOKEN is NOT loaded from Render Environment Variables")
    print("👉 Go to Render → Environment → Add BOT_TOKEN")
    exit(1)  # خارج شدن با خطا تا دیپلوی fail شود و لاگ بدهد

print("✅ BOT_TOKEN loaded successfully")

bot = telebot.TeleBot(BOT_TOKEN)

# هندلر فایل‌های مستند (فیلم، سند)
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

        bot.reply_to(message, f"📥 لینک دانلود داخلی:\n{download_link}")

    except Exception as e:
        bot.reply_to(message, f"❌ خطا در پردازش:\n{e}")

print("🤖 Bot is running and polling...")
bot.infinity_polling()
