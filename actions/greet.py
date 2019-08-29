"""Module that greets the user"""
import oscar_defaults, oscar_functions
from datetime import datetime

def greet():
    """Greets the user, based on what time of day it is."""
    global responses
    user = oscar_defaults.settings_array[0]
    hour = datetime.now().hour
    greeting = ""
    if hour >= 18 or hour < 7:
        greeting = oscar_functions.get_response(1, "<user>", user)
    else:
        greeting = oscar_functions.get_response(0, "<user>", user)
    print(greeting)
