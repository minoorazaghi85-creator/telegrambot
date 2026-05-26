import telebot
import os
import sys

BOT_TOKEN = os.getenv("8276989335:AAF2O9HzuhtkemO3O60WRRe1pdcNL82exHg")

if not BOT_TOKEN:
    print("BOT_TOKEN is missing")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['document', 'video'])
def handle_file(message):
    try:
        file_id = None

        if message.document:
            file_id = message.document.file_id
        elif message.video:
            file_id = message.video.file_id

        if not file_id:
            bot.reply_to(message, "فایل نامعتبر ❌")
            return

        file = bot.get_file(file_id)
        link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        bot.reply_to(message, f"📥 لینک دانلود:\n{link}")

    except Exception as e:
        bot.reply_to(message, f"خطا:\n{e}")


print("Bot is running...")
bot.infinity_polling()
