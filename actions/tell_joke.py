"""Tells the user a joke, using pyjokes"""
from random import randint
import pyjokes

def tell_joke(runtime):
    """Selects a neutral joke from pyjokes, and tells it to the user

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    joke_list = pyjokes.neutral
    print(joke_list[randint(0, len(joke_list) - 1)])
