import telebot
from telebot.apihelper import ApiTelegramException
import os

# بهتره توکن رو از Environment Variable بگیری
BOT_TOKEN = os.getenv("8276989335:AAH7BcioFOhQ5rJUNRxPyt9TPcWAqM1Kogs")

bot = telebot.TeleBot(BOT_TOKEN)


MAX_SAFE_SIZE = 45 * 1024 * 1024  # حدود 45MB (برای جلوگیری از خطا)


@bot.message_handler(content_types=['document', 'video'])
def handle_file(message):
    try:
        file_id = None
        file_size = 0
        file_name = "unknown"

        if message.document:
            file_id = message.document.file_id
            file_size = message.document.file_size
            file_name = message.document.file_name

        elif message.video:
            file_id = message.video.file_id
            file_size = message.video.file_size
            file_name = "video.mp4"

        if not file_id:
            bot.reply_to(message, "❌ فایل پیدا نشد")
            return

        # 🔥 اگر فایل خیلی بزرگ بود → اصلاً API call نزن
        if file_size and file_size > MAX_SAFE_SIZE:
            bot.reply_to(
                message,
                "⚠️ فایل خیلی بزرگه و تلگرام اجازه پردازش مستقیم نمی‌ده.\n"
                "لطفاً از لینک مستقیم یا فایل کوچیک‌تر استفاده کن."
            )
            return

        file = bot.get_file(file_id)

        if not file or not file.file_path:
            bot.reply_to(message, "❌ فایل قابل دریافت نیست")
            return

        link = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

        bot.reply_to(
            message,
            f"📥 لینک دانلود شما:\n\n{link}\n\n📦 نام فایل: {file_name}"
        )

    except ApiTelegramException as e:
        bot.reply_to(message, f"❌ خطای تلگرام:\n{e}")

    except Exception as e:
        bot.reply_to(message, f"❌ خطای ناشناخته:\n{str(e)}")


# برای اینکه روی Render نخوابه
print("Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
