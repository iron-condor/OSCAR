import pyjokes
from random import randint
def tell_joke():
    joke_list = pyjokes.neutral
    print(joke_list[randint(0, len(joke_list) - 1)])
