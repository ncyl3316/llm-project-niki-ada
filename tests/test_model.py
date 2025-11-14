#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 00:05:53 2025

@author: nikichan
"""

import unittest
from src.model import load_model, get_response

class TestModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model, cls.tokenizer = load_model()

    def test_factual_query(self):
        prompt = "What is the capital of Japan?"
        response = get_response(prompt, self.model, self.tokenizer)
        self.assertIn("Tokyo", response)

    def test_code_generation(self):
        prompt = "Write a Python function that returns the square of a number."
        response = get_response(prompt, self.model, self.tokenizer)
        self.assertTrue("def" in response and "return" in response)

if __name__ == "__main__":
    unittest.main()
