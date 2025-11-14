#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 23:25:07 2025

@author: nikichan
"""

from src.model import load_model, get_response

model, tokenizer = load_model()

print("Demo started. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = get_response(user_input, model, tokenizer)
    print(f"Model: {response}\n")
