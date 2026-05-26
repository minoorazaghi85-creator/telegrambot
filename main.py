import telebot

bot = telebot.TeleBot("توکن-رباتت")

@bot.message_handler(content_types=['document', 'video'])
def handle_file(message):
    file_id = message.document.file_id if message.document else message.video.file_id
    file = bot.get_file(file_id)
    link = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
    
    bot.reply_to(message, f"لینک دانلود:\n{link}")

bot.polling()
