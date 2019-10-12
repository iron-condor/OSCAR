"""Allows OSCAR to start a stopwatch, and time the user"""
import time
import oscar_functions

start_time = 0

def start_stopwatch():
    """Begins a stopwatch"""
    global start_time
    start_time = time.time()

def stop_stopwatch():
    """Stops the stopwatch"""
    stop_time = time.time()
    return stop_time - start_time

def stopwatch(runtime):
    """Manages the starting and stopping of the stopwatch"""
    print(runtime.responses["stopwatch_started"].get_line())
    start_stopwatch()
    input()
    final_time = stop_stopwatch()
    formatted_time = oscar_functions.convert_and_format_time(final_time)
    print(runtime.responses["disp_time_passed"].get_line("<time_string>", formatted_time))
