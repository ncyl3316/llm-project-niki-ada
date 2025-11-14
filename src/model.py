#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 23:19:44 2025

@author: nikichan
"""

from transformers import AutoTokenizer, AutoModelForCausalLM

def load_model(model_id: str = "google/gemma-2b-it"):
    """Loads the model and tokenizer.

    Behavior:
    - If `bitsandbytes` is installed and a CUDA device is available, try 4-bit quantized load.
    - Otherwise fall back to CPU load without quantization.
    """
    # lazy imports so this file can be imported even if some packages are missing
    try:
        import torch
    except Exception:
        torch = None

    # Try to import BitsAndBytesConfig if bitsandbytes package is available
    quantization_config = None
    try:
        from transformers import BitsAndBytesConfig
        import bitsandbytes as bnb  # noqa: F401
        bnb_available = True
    except Exception:
        BitsAndBytesConfig = None  # type: ignore
        bnb_available = False

    use_quant = False
    device_map = "cpu"
    kwargs = {}

    if bnb_available and torch is not None and torch.cuda.is_available():
        # GPU available and bitsandbytes installed: prefer 4-bit quant
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        use_quant = True
        device_map = "auto"
        kwargs["torch_dtype"] = torch.float16
    else:
        # CPU-only fallback (or bitsandbytes missing)
        device_map = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    load_kwargs = {"device_map": device_map}
    if quantization_config is not None:
        load_kwargs["quantization_config"] = quantization_config
    # include optional kwargs like torch_dtype only when set
    load_kwargs.update({k: v for k, v in kwargs.items() if v is not None})

    model = AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
    return model, tokenizer


def get_response(prompt: str, model, tokenizer, max_length: int = 150):
    """Generates a response from the model given a prompt.

    This function is robust to CPU-only and CUDA devices. It will:
    - tokenize the prompt, move tensors to the model device
    - run generation under `torch.no_grad()`
    - decode and return the generated text
    """
    try:
        import torch
    except Exception:
        torch = None

    # Determine model device. Prefer first parameter device, otherwise CPU.
    device = None
    try:
        device = next(model.parameters()).device
    except Exception:
        # fallback to CPU
        device = "cpu"

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt")
    if torch is not None and isinstance(device, torch.device):
        inputs = {k: v.to(device) for k, v in inputs.items()}

    gen_kwargs = dict(
        max_new_tokens=max_length,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id,
    )

    if torch is not None:
        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
    else:
        # If torch isn't available, raise a helpful error
        raise RuntimeError("PyTorch is required for generation but is not available in the environment.")

    # decode the first sequence
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text.strip()
