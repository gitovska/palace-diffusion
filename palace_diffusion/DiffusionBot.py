import os

from Database import retrieve_recent_chat_history, write_row
from Llama import generate_reply
from Logger import LOGGER
from Pipeline import PIPELINE
from telegram import Update
from telegram.ext import ContextTypes


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

    LOGGER.info(f'{message_type.capitalize()} user chat ({chat_id}): "{message_text}"')

    chat_history = retrieve_recent_chat_history(chat_id)

    if message_type == "group":
        if bot_username in message_text:
            new_text = message_text.replace(bot_username, "").strip()
            reply = generate_reply(new_text, chat_history, PIPELINE)
        else:
            return
    else:
        reply = generate_reply(message_text, chat_history, PIPELINE)
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
    caption = update.message.caption

    if update.message.document:
        file_id = update.message.document.file_id
        file_unique_id = update.message.document.file_unique_id
        _, file_extension = os.path.splitext(update.message.document.file_name)
    else:
        file_id = update.message.photo[-1].file_id
        file_unique_id = update.message.photo[-1].file_unique_id

    LOGGER.info(
        f'{message_type.capitalize()} with photo ({file_unique_id}), user chat ({chat_id}): "{caption}"'
    )

    image = await context.bot.get_file(file_id)

    if caption is not None:
        await image.download_to_drive(
            f"../data/images/{chat_id}_{file_unique_id}{file_extension if update.message.document else '.jpg'}"
        )

        with open(f"../data/images/{chat_id}_{file_unique_id}.txt", "w") as f:
            f.write(caption)

        LOGGER.info(f"Image {file_unique_id} saved with caption: {caption}")

        chat_history = retrieve_recent_chat_history(chat_id)
        reply = generate_reply(caption, chat_history, PIPELINE)

        await context.bot.send_message(chat_id=chat_id, text=reply)

    else:
        reply = "Nice photo babe, but would you mind sending it again with a caption?"
        await context.bot.send_message(chat_id=chat_id, text=reply)

    row = {
        "chat_id": [chat_id],
        "message_id": [message_id],
        "message_text": [caption],
        "reply_text": [reply.strip()],
    }

    write_row(row, chat_id)


def retrieve_bot_username() -> str:
    return "PalaceDiffusion_Bot"


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.error(f"Update {update} caused error {context.error}")
