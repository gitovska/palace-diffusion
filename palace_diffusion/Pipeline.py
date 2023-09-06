from Logger import LOGGER
from transformers import AutoTokenizer, Pipeline, pipeline
from dotenv import load_dotenv
import os
import torch


def retrieve_model() -> str:
    return "meta-llama/Llama-2-7b-chat-hf"


def initialise_llama(model: str, token: str) -> tuple[AutoTokenizer, Pipeline]:
    if torch.cuda.is_available():
        LOGGER.info(f"Loading Model on cuda: {torch.cuda.current_device()}")
    else:
        LOGGER.info(f"Loading Model on CPU")
    return (
        AutoTokenizer.from_pretrained(model),
        pipeline(
            "text-generation",
            model=model,
            torch_dtype=torch.float16,
            device_map="auto",
            token=token,
        ),
    )


model = retrieve_model()
load_dotenv()
token = os.getenv("HF_TOKEN")
TOKENIZER, PIPELINE = initialise_llama(model, token)
