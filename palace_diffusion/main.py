import os

from telegram.ext import filters, ApplicationBuilder, CommandHandler, MessageHandler

from dotenv import load_dotenv

from DiffusionBot import handle_message, start, error_handler

from Logger import LOGGER

load_dotenv()
token = os.getenv("TG_TOKEN")


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler("start", start)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    # image_handler = MessageHandler(filters.Document, incoming_image)
    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_error_handler(error_handler)
    application.run_polling()
