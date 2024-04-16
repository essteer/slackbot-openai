# -*- coding: utf-8 -*-

# Toggle terminal print-outs
VERBOSE = False

# Master dict to store different discussions
THREADS_DICT = dict()

MODEL = "zero-one-ai/Yi-34B-Chat"

MAX_TOKENS = 1500
TEMPERATURE = 0.1
TOP_K = 5
TOP_P = 0.7
REPETITION_PENALTY = 1.1

MAP_ID_MODEL = {
    "U06SZHDL487": "alpaca-7b", 
    "U06U2UKPERE": "Llama-2-13b-chat-hf", 
    "U06SZGFGNLF": "Mistral-7B-Instruct-v0.1", 
    "U06T5FVMMKL": "Yi-34B-Chat",
    "U06U9E0BGVC": "Intro-bot"
}
MAP_MODEL_ID = {
    "alpaca-7b": "U06SZHDL487",
    "Llama-2-13b-chat-hf": "U06U2UKPERE",
    "Mistral-7B-Instruct-v0.1": "U06SZGFGNLF",
    "Yi-34B-Chat": "U06T5FVMMKL", 
    "Intro-bot": "U06U9E0BGVC"
}

DEVS = {
    "U06PSGU9JJG": "ES",
}
