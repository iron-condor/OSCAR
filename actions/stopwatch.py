"""Allows OSCAR to start a stopwatch, and time the user"""
import oscar_functions, oscar_defaults
import time

start_time = 0

def start_stopwatch():
    """Begins a stopwatch"""
    global start_time
    start_time = time.time()

def stop_stopwatch():
    """Stops the stopwatch"""
    stop_time = time.time()
    return stop_time - start_time

def stopwatch():
    """Manages the starting and stopping of the stopwatch"""
    print(oscar_functions.get_response(45))
    start_stopwatch()
    input()
    final_time = stop_stopwatch()
    formatted_time = oscar_functions.convert_and_format_time(final_time)
    print(oscar_functions.get_response(46, "<time_string>", formatted_time))
