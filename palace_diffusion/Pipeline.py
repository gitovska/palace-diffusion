import torch
from Logger import LOGGER
from transformers import AutoModelForCausalLM, AutoTokenizer, Pipeline, pipeline


def retrieve_model_name() -> str:
    return "TheBloke/Llama-2-7B-chat-GPTQ"


def initialise_llama(model_name: str) -> Pipeline:
    if torch.cuda.is_available():
        LOGGER.info(f"Loading model on GPU; cuda: device {torch.cuda.current_device()}")
    else:
        LOGGER.info(f"Loading Model on CPU")

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float16, device_map="auto", revision="main"
    )

    return pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        do_sample=True,
        max_new_tokens=100,
        temperature=0.7,
        top_p=0.85,
        repetition_penalty=1.15,
    )


model_name = retrieve_model_name()
torch.cuda.empty_cache()
PIPELINE = initialise_llama(model_name)
