"""Tells the user a joke, using pyjokes"""
import pyjokes
from random import randint

def tell_joke():
    """Selects a neutral joke from pyjokes, and tells it to the user"""
    joke_list = pyjokes.neutral
    print(joke_list[randint(0, len(joke_list) - 1)])
