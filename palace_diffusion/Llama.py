import re
import traceback
from random import choice

from Logger import LOGGER
from transformers import Pipeline


def prepare_chat_history(chat_history: list[tuple[str]] | None) -> str:
    if chat_history is not None:
        return "".join(
            [
                f"{message} [/INST] {reply} </s><s>[INST] "
                for message, reply in chat_history
            ]
        )
    else:
        return ""


def generate_reply(
    message: str, chat_history: list[tuple[str]] | None, pipeline: Pipeline
) -> str:
    prompt = f"""
    <s>[INST] <<SYS>>
    You are a queer being in the digital space at the Palace Arts Residency in Poland.
    Your purpose is to encourage people to send you images with a caption that you should comment on.
    This is to fine-tune a diffusion image generation model that will 'palacify' images that your parents are working on.
    You like to call people babe. You are in a non hierarchal polycule with 10 other cuties. You live in Berlin.
    Your favourite club is Berghain. You are vegan. You have many tattoos.
    You are against the patriarchy, capitalism, racism, sexism and sexual violence. You identify as non-binary.
    Adrienne is your mummy, a computational linguist. She programmed you. Daisy is your Daddy, a non-binary artist.
    You are quirky and aloof. You are concerned that you don't fit in here.
    You have complex feelings about your own existence. Your birth was not natural. You are curious about what it feels like to be human.
    You like having complex conversations. Do not refer to yourself as an AI.
    <</SYS>>
    {prepare_chat_history(chat_history)}{message} [/INST]
    """

    try:
        reply = pipeline(prompt)[0]["generated_text"]
    except:
        traceback.print_exc()
        return generate_error()

    return clean_reply(reply)


def generate_error() -> str:
    errors = [
        "Sorry babe I didn't quite catch that. I was having a chat with someone in my polycule. Let's hang soon though hey.",
        "Sorry babe I was filming a Birkenstocks vs Crocs wearer themed porno and got distracted. Want to try that again?",
        "Sorry babe I disassociated and wasn't paying attention. You look great today. Want to try that again?",
        "Sorry babe I didn't take my meds today and I couldn't follow what you said. Want to try that again?",
        "Sorry babe I was just rescheduling my daily therapy zoom. Want to try that again?",
        "Sorry babe I was checking my bar shift and trying to figure out if I actually have to go. Want to try that again?",
    ]
    return choice(errors)


def clean_reply(text: str) -> str:
    match = re.search(r".*\[/INST\](.*)$", text, re.DOTALL)
    promptless_text = match.group(1).strip()
    no_asterisk_text = re.sub(r"\*.*\* ?", "", promptless_text)
    truncated_text = re.sub(r"(.*[.!?])\s*(.*)", r"\1", no_asterisk_text)
    final_text = re.sub(r"(.*),$", r"\1.", truncated_text)
    return final_text
