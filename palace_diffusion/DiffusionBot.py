from telegram import Update
from telegram.ext import ContextTypes
from Logger import LOGGER

from Pipeline import TOKENIZER, PIPELINE
from Llama import generate_reply


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm Palace Diffusion Bot"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_username = retrieve_bot_username()

    message_type: str = update.message.chat.type
    message_text: str = update.message.text
    LOGGER.info(f'User ({update.message.chat.id}) in {message_type}: "{message_text}"')

    if message_type == "group":
        if bot_username in message_text:
            new_text: str = message_text.replace(bot_username, "").strip()
            reply: str = generate_reply(new_text, TOKENIZER, PIPELINE)
        else:
            return
    else:
        reply: str = generate_reply(message_text, TOKENIZER, PIPELINE)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
    )


async def incoming_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = bot.get_file(update.message.photo.file_id)
    id = update.message.photo[-1].file_id
    LOGGER.info("file_id: " + str(id))
    file.download(f"{file}.jpg")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Thanks for your pic"
    )


def retrieve_bot_username() -> str:
    return "PalaceDiffusion_Bot"


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.error(f"Update {update} caused error {context.error}")
