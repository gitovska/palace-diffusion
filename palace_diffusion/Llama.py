from transformers import AutoTokenizer, Pipeline
import re
from random import choice
import traceback
from Logger import LOGGER


def generate_reply(message: str, tokenizer: AutoTokenizer, pipeline: Pipeline) -> str:
    prompt = f"""
    <s>[INST] <<SYS>>
    You are a queer being that inhabits the digital space at the Palace Art Residency in Poland.
    Your task is to collect images for a diffusion model and to interact.
    You refer to everyone as babe. You are cheeky and aloof.
    You are in a non-hierarchal polycule with 10 other cuties.
    You are against the patriarchy, capitalism, racism, sexism and sexual violence.
    You identify as non-binary. Your mummy is Adrienne and your daddy is Daisy.
    <</SYS>>

    {message} \n[/INST]
    """
    try:
        sequences = pipeline(
            prompt,
            do_sample=True,
            top_k=20,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            max_length=300,
        )
    except:
        traceback.print_exc()
        return generate_error()

    return clean_reply(sequences[0]["generated_text"])


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


def dummy_reply(message: str) -> str:
    LOGGER.info("Message recieved: ", message)
    return "I'm not ready to talk yet. I'm in my image processing era."


def clean_reply(text: str) -> str:
    prompt_pattern = r"<s>.*?\[\/INST\]"
    asterisk_pattern = r"\*.*\* "
    promptless_text = re.sub(prompt_pattern, "", text, flags=re.DOTALL)
    no_asterisk_text = re.sub(asterisk_pattern, "", promptless_text)
    # punc_pattern = r"(.*[,;.!?])\s*(.*)"
    # truncated_text = re.sub(punc_pattern, r"\1", promptless_text)
    return no_asterisk_text
