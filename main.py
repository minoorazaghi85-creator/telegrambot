import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# فعال کردن لاگ برای پیگیری خطاها
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- تنظیمات اولیه و متغیرها ---
TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
if not TOKEN:
    logger.error("متغیر محیطی BOT_TOKEN یافت نشد!")
    exit(1)
if not RENDER_EXTERNAL_URL:
    logger.error("متغیر محیطی RENDER_EXTERNAL_URL یافت نشد! لطفاً آن را در Environment اضافه کنید.")
    exit(1)

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 10000))

# --- منطق ربات (دستورات و پاسخ‌ها) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستور /start"""
    await update.message.reply_text('سلام! من یک ربات تلگرام هستم.')

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به فایل‌ها و فیلم‌ها"""
    try:
        file = None
        if update.message.document:
            file = await update.message.document.get_file()
            await update.message.reply_text(f"📄 نام فایل: {update.message.document.file_name}")
        elif update.message.video:
            file = await update.message.video.get_file()
            await update.message.reply_text("🎬 فایل ویدیویی دریافت شد.")

        if not file:
            await update.message.reply_text("❌ فرمت فایل پشتیبانی نمی‌شود.")
            return

        download_link = f"https://api.telegram.org/file/bot{TOKEN}/{file.file_path}"
        await update.message.reply_text(f"📥 لینک دانلود فایل شما:\n{download_link}")

    except Exception as e:
        logger.error(f"خطا در پردازش فایل: {e}")
        await update.message.reply_text(f"❌ خطا در پردازش فایل:\n{e}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پاسخ به دستورات ناشناخته"""
    await update.message.reply_text("متاسفم، این دستور را نمی‌فهمم!")

def main():
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, handle_file))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info(f"راه‌اندازی Webhook روی آدرس: {WEBHOOK_URL}")
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=WEBHOOK_PATH,
        webhook_url=WEBHOOK_URL,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
