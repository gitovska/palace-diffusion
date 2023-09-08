from telegram import Update
from telegram.ext import ContextTypes
from Logger import LOGGER
from Pipeline import PIPELINE
from Llama import generate_reply
from Database import (
    write_row,
    retrieve_recent_chat_history,
    save_image_with_description,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    chat_history = retrieve_recent_chat_history(chat_id)
    await context.bot.send_message(
        chat_id=chat_id, text=generate_reply("Hello 👋", chat_history, PIPELINE)
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot_username = retrieve_bot_username()

    chat_id = update.message.chat.id
    message_type = update.message.chat.type
    message_id = update.message.id
    message_text = update.message.text

    LOGGER.info(f'{message_type.upper()} user chat ({chat_id}): "{message_text}"')

    chat_history = retrieve_recent_chat_history(chat_id)

    if message_type == "group":
        if bot_username in message_text:
            new_text: str = message_text.replace(bot_username, "").strip()
            reply: str = generate_reply(new_text, chat_history, PIPELINE)
        else:
            return
    else:
        reply: str = generate_reply(message_text, chat_history, PIPELINE)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=reply,
    )

    row = {
        "chat_id": [chat_id],
        "message_id": [message_id],
        "message_text": [message_text],
        "reply_text": [reply.strip()],
    }

    write_row(row, chat_id)


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_type = update.message.chat.type
    message_id = update.message.id
    message_text = update.message.text
    file_id = update.message.photo[-1].file_id

    LOGGER.info(
        f'{message_type.upper()} with photo ({file_id}), user chat ({chat_id}): "{message_text}"'
    )

    image = context.bot.get_file(file_id)
    save_image_with_description(image, file_id, chat_id, message_text)

    await context.bot.send_message(
        chat_id=chat_id, text=generate_reply(message_text, chat_history, PIPELINE)
    )

    row = {
        "chat_id": [chat_id],
        "message_id": [message_id],
        "message_text": [message_text],
        "reply_text": [reply.strip()],
    }

    write_row(row, chat_id)


def retrieve_bot_username() -> str:
    return "PalaceDiffusion_Bot"


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.error(f"Update {update} caused error {context.error}")
