import oscar_functions, oscar_defaults
import time

start_time = 0

#Begins a stopwatch
def start_stopwatch():
    global start_time
    start_time = time.time()

#Stops the stopwatch
def stop_stopwatch():
    stop_time = time.time()
    return stop_time - start_time

#Manages the starting and stopping of the stopwatch
def stopwatch():
    print(oscar_functions.get_response(45))
    start_stopwatch()
    input()
    final_time = stop_stopwatch()
    formatted_time = oscar_functions.convert_and_format_time(final_time)
    print(oscar_functions.get_response(46, "<time_string>", formatted_time))
