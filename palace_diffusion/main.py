import os

from DiffusionBot import error_handler, handle_image, handle_message, start
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

load_dotenv()
token = os.getenv("TG_TOKEN")


if __name__ == "__main__":
    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler("start", start)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    image_handler = MessageHandler(filters.Document.IMAGE | filters.PHOTO, handle_image)

    application.add_handler(start_handler)
    application.add_handler(text_handler)
    application.add_handler(image_handler)
    application.add_error_handler(error_handler)

    application.run_polling()
