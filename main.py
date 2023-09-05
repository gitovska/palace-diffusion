import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
)

load_dotenv()

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def incoming_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm not ready to talk yet. I'm in my image processing era.",
    )


async def incoming_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = bot.get_file(update.message.photo.file_id)
    id = update.message.photo[-1].file_id
    print("file_id: " + str(id))
    file.download(f"{file}.jpg")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks for your pic"
    )


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), incoming_text)
    start_handler = CommandHandler("start", start)
    image_handler = MessageHandler(filters.Document, incoming_image)
    application.add_handler(start_handler)
    application.add_handler(text_handler)

    application.run_polling()
