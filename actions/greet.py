"""Module that greets the user"""
from datetime import datetime
import oscar_defaults

def greet(runtime):
    """Greets the user, based on what time of day it is."""
    user = oscar_defaults.settings_dict["name"].state
    hour = datetime.now().hour
    greeting = ""
    if hour >= 18 or hour < 7:
        greeting = runtime.responses["nighttime_greetings"].get_line("<user>", user)
    else:
        greeting = runtime.responses["daytime_greetings"].get_line("<user>", user)
    print(greeting)
