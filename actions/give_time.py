"""Module that gives the user the time and date"""
import oscar_functions, oscar_defaults
from datetime import datetime

def give_time(runtime):
    """Gives the user the time and date."""
    time = None
    #If 12-hour clock
    if (runtime.settings["use_12_hour_clock"].state):
        time = datetime.now().strftime("%A, %B %d, at %I:%M %p")
    #If 24-hour clock
    else:
        time = datetime.now().strftime("%A, %B %d, at %H:%M")
    print(runtime.responses["disp_time"].get_line("<time>", time))
