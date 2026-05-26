import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# فعال کردن logging برای فهم بهتر از خطاها
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# خواندن توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    logger.error("خطا: متغیر محیطی BOT_TOKEN پیدا نشد!")
    exit(1)

# آدرس عمومی که Render به سرویس شما داده
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/webhook"
PORT = int(os.getenv("PORT", 10000))

# --- منطق ربات (دستورات و پاسخ‌ها) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستور /start"""
    await update.message.reply_text('سلام! من یک ربات تلگرام هستم.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به هر پیام متنی"""
    user_message = update.message.text
    await update.message.reply_text(f'تو گفتی: {user_message}')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به فایل‌ها و فیلم‌ها"""
    try:
        file = None
        if update.message.document:
            file = await update.message.document.get_file()
        elif update.message.video:
            file = await update.message.video.get_file()

        if not file:
            await update.message.reply_text("❌ فایل نامعتبره")
            return

        download_link = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
        await update.message.reply_text(f"📥 لینک دانلود:\n{download_link}")

    except Exception as e:
        logger.error(f"خطا در پردازش فایل: {e}")
        await update.message.reply_text(f"❌ خطا در پردازش:\n{e}")

# --- راه‌اندازی اپلیکیشن و تنظیم Webhook ---
def main():
    # ساخت اپلیکیشن
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, handle_file))

    # راه‌اندازی Webhook
    logger.info(f"تنظیم Webhook روی آدرس: {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook",
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
