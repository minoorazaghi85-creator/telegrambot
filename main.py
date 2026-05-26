import os
print("ENV TEST:", dict(os.environ))
import telebot

print("🚀 Starting bot...")

BOT_TOKEN = os.getenv("8276989335:AAEMMygR7yaUlCV7WhMoI0WP6u5wf2MiOls")

print("DEBUG BOT_TOKEN:", BOT_TOKEN)

# اگر توکن نبود، کرش نکنه (فقط لاگ بده)
if not BOT_TOKEN:
    print("❌ BOT_TOKEN is NOT loaded from Render Environment Variables")
    print("👉 Go to Render → Environment → Add BOT_TOKEN")
else:
    print("✅ BOT_TOKEN loaded successfully")


bot = telebot.TeleBot(BOT_TOKEN) if BOT_TOKEN else None


if bot:

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

            file = bot.get_file(file_id)
            link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

            bot.reply_to(message, f"📥 لینک دانلود:\n{link}")

        except Exception as e:
            bot.reply_to(message, f"❌ خطا:\n{e}")


    print("🤖 Bot is running...")
    bot.infinity_polling()

else:
    print("⛔ Bot NOT started because BOT_TOKEN is missing")
