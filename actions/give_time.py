"""Module that gives the user the time and date"""
import oscar_functions, oscar_defaults
from datetime import datetime

def give_time():
    """Gives the user the time and date."""
    day = datetime.now().day
    weekday = datetime.now().weekday
    month = datetime.now().month
    hour = datetime.now().hour
    minute = datetime.now().minute
    time = None
    #If 12-hour clock
    if (oscar_functions.settings[1]):
        time = datetime.now().strftime("%A, %B %d, at %I:%M %p")
    #If 24-hour clock
    else:
        time = datetime.now().strftime("%A, %B %d, at %H:%M")
    print(oscar_functions.get_response(5, "<time>", time))
