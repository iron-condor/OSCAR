"""Module that greets the user"""
from datetime import datetime
import oscar_defaults

def greet(runtime):
    """Greets the user, based on what time of day it is."""
    user = oscar_defaults.settings_array[0]
    hour = datetime.now().hour
    greeting = ""
    if hour >= 18 or hour < 7:
        greeting = runtime.get_response(1, "<user>", user)
    else:
        greeting = runtime.get_response(0, "<user>", user)
    print(greeting)
