import oscar_defaults
import getpass
from datetime import datetime
import duckduckgo
import os
import sys
import subprocess
import collections
import re
from random import randint
import pyjokes

responses = []
inputs = []
settings = []
firstTime = True

#Runs commands as a detached subprocess. In other words, if OSCAR is closed, the commands ran here continue existing.
#Used in command scheduling, alongside with the /usr/bin/sleep command.
#Sample input: subprocess_cmd("sleep 60 && poweroff")
def subprocess_cmd(bash_command):
    subprocess.Popen(bash_command,stdout=subprocess.PIPE, shell=True, preexec_fn=os.setpgrp)

#Decides if a particular string is a positive or negative statement. In other words, it can read a string as yes/no.
#If the type is none, it checks if the string means yes
#If the type is anything besides none, it checks if the string means no
def get_yes_no(confirm, type = None):
    global inputs
    contained_yes = ""
    if type == None:
        for i in range(0, len(inputs[9][0])):
            if contained_yes == "":
                if re.search(inputs[9][0][i],confirm):
                    contained_yes = inputs[9][0][i]
                if contained_yes != "" and len(inputs[9][1]):
                    for antiword in inputs[9][1]:
                        if re.search(antiword, confirm):
                            contained_yes = ""
            if contained_yes != "":
                return True
                break
        return False
    else:
        for i in range(0, len(inputs[8][0])):
            if contained_yes == "":
                if re.search(inputs[8][0][i], confirm):
                    contained_yes = inputs[8][0][i]
                if contained_yes != "" and len(inputs[8][1]):
                    for antiword in inputs[8][1]:
                        if re.search(antiword, confirm):
                            contained_yes = ""
            if contained_yes != "":
                return True
                break
        return False

#Randomly fetches an appropriate response from the responses array.
#Index is the index in the first dimension of the array.
#Delimiter is the string to be replaced
#Replacement is the string with which the delimiter is replaced
def get_response(index, delimiter = None, replacement = None):
    if delimiter == None or replacement == None:
        if responses:
            return responses[index][randint(0, len(responses[index]) - 1)]
        else:
            return oscar_defaults.responses_array[index][randint(0, len(oscar_defaults.responses_array[index]) - 1)]
    else:
        return get_response(index).replace(delimiter, replacement)

#Greets the user. responses[0] for daytime greetings, responses[1] for nighttime greetings.
def greet():
    global responses
    user = oscar_defaults.settings_array[0]
    hour = datetime.now().hour
    greeting = ""
    if hour >= 18 or hour < 7:
        greeting = get_response(1, "<user>", user)
    else:
        greeting = get_response(0, "<user>", user)
    print(greeting)

#Gives the user the time and date.
def give_time():
    day = datetime.now().day
    weekday = datetime.now().weekday
    month = datetime.now().month
    hour = datetime.now().hour
    minute = datetime.now().minute
    time = None
    #If 12-hour clock
    if (settings[1]):
        time = datetime.now().strftime("%A, %B %d, at %I:%M %p")
    #If 24-hour clock
    else:
        time = datetime.now().strftime("%A, %B %d, at %H:%M")
    print(get_response(5, "<time>", time))

#Opens a given URL in the user's browser. If unsuccessful, prompts the user to open it his/herself.
def open_in_browser(url):
    if sys.platform == 'win32':
        print(get_response(23))
        os.startfile(url)
    elif sys.platform == 'darwin':
        print(get_response(23))
        subprocess.Popen(['open', url])
    else:
        try:
            print(get_response(23))
            subprocess.Popen(['xdg-open', url])
        except OSError:
            get_response(7, "<url>", url)

#Searches and interprets a given string. Can extract summaries from some sites and services. Uses duckduckgo
def search(identifier_string, command):
    index = re.search(identifier_string, command).end()
    query = command[index:]
    if query.endswith("?"):
        query = query[:-1]
    if query != "":
        answer = duckduckgo.get_zci(query)
        duck_query = duckduckgo.query(query)
        if answer != "":
            print(answer + "\n")
            if duck_query.type != "nothing":
                confirm = input(get_response(4)).lower()
                if get_yes_no(confirm):
                    open_in_browser(duck_query.related[0].url)
                else:
                    print(get_response(19))
            elif answer.startswith("http"):
                confirm = input(get_response(3)).lower()
                if get_yes_no(confirm):
                    open_in_browser(answer)
                else:
                    print(get_response(20))

        else:
            confirm = input(get_response(3)).lower()
            if get_yes_no(confirm):
                for c in query:
                    if c == ' ':
                        c = '+'
                open_in_browser("https://www.duckduckgo.com/?q=" + query)
            else:
                print(get_response(20))
    else:
        print(get_response(2))

#Returns the time in seconds until a scheduled event. Interprets text from the user in standard time units
def schedule(command):
    time_units = collections.OrderedDict([
        ("\\bsecs?\\b|\\bseconds?\\b", 1),
        ("\\bmins?\\b|\\bminutes?\\b", 60),
        ("\\bhour\\b", 3600),
        ("\\bday\\b", 86400)
    ])
    total_time = 0.0
    for key in time_units:
        occurences = re.findall(key, command)
        if occurences:
            for item in occurences:
                index = command.find(item)
                index = command.rfind(' ', 0, index - 1) + 1
                #This bit's here to ignore false positives. For example: "I'll be heading to bed in a minute, so can you shut down my computer in 2 min?"
                try:
                    num = float(command[index:(command.find(' ', index))])
                    total_time += (num * time_units[key])
                except Exception:
                    continue
    if total_time != 0:
        time_string = ""
        orig_total_time = total_time
        days = int(total_time // 86400)
        if days > 0:
            total_time -= (days * 86400)
            if days > 1:
                time_string += str(days) + " days "
            else:
                time_string += str(days) + " day "

        hours = int(total_time // 3600)
        if hours > 0:
            total_time -= (hours * 3600)
            if hours > 1:
                time_string += str(hours) + " hours "
            else:
                time_string += str(hours) + " hour "

        minutes = int(total_time // 60)
        if minutes > 0:
            total_time -= (minutes * 60)
            if minutes > 1:
                time_string += str(minutes) + " minutes "
            else:
                time_string += str(minutes) + " minute "
        seconds = int(total_time)
        if seconds > 0:
            if time_string:
                time_string += "and"
            if seconds > 1:
                time_string += " " + str(seconds) + " seconds"
            else:
                time_string += " 1 second"
        else:
            time_string = time_string[:len(time_string) - 1]
        confirm = input(get_response(8, "<time_string>", time_string)).lower()
        while True:
            if get_yes_no(confirm):
                return orig_total_time
            elif get_yes_no(confirm, 1):
                print(get_response(9))
                break
            else:
                confirm = input(get_response(10)).lower()
    else:
        print(get_response(11))

#Schedules a command to be executed after a given time period.
def schedule_command(command):
    time = schedule(command)
    if time != None:
        bash_command = None;
        if "\"" in command:
            index1 = command.find("\"") + 1
            index2 = command.find("\"", index1 + 1, len(command))
            bash_command = "sleep " + str(time) + " && " + command[index1:index2]
            subprocess_cmd(bash_command)

        else:
            bash_command = "sleep " + str(time) + " && " + input(get_response(22))
            subprocess_cmd(bash_command)
        print(get_response(21))

#Schedules a shutdown to be performed after a given time period.
def schedule_shutdown(command):
    time = schedule(command)
    if time != None:
        shell_command = None
        if sys.platform == "win32":
            shell_command = "shutdown -s -t " + str(time) + " -c Shutting down. Have a lovely rest of your day."
        elif sys.platform == "darwin":
            shell_command = "sleep " + str(time) + "osascript -e 'tell app \"System Events\" to shut down'"
        else:
            shell_command = "sleep " + str(time) + " && poweroff"
        subprocess_cmd(shell_command)
        print(get_response(12))

#Tells the user if someone should or should not perform an action.
#It offers 2 variants
#   - "Or" mode: Tells the user if they should perform one action, "or" another
#   - "Yes/no" mode: Responds as to whether the user should or should not do one particular action.
def should(command):
    #If we're in yes/no mode
    if " or " not in command.lower():
        if randint(0, 1):
            print(get_response(17))
        else:
            print(get_response(18))
    elif " or " in command:
        #Cut out the "should i" part of the string
        should_index = command.find("should ")
        #The string "should " is 7 characters
        should_index += 7
        end_of_next_word = command.find(" ", should_index)
        string = command[end_of_next_word + 1:]
        if string.endswith("?"):
            string = string[:-1]
        options = string.split(" or ")
        randIndex = randint(0, len(options) - 1)
        option = options[randIndex]
        print(get_response(14, "<option>", option))

def tell_joke():
    joke_list = pyjokes.neutral
    print(joke_list[randint(0, len(joke_list) - 1)])

#Receives the command and processes the input appropriately
def receive_command():
    global responses, inputs, settings, firstTime
    if firstTime:
        responses = oscar_defaults.responses_array
        inputs = oscar_defaults.inputs_array
        settings = oscar_defaults.settings_array
        greet()
        firstTime = False
    command = input("").lower()
    contained_keyword = ""
    command_index = -1
    for input_type in range(0, len(inputs)):
        if contained_keyword == "":
            for keyword in inputs[input_type][0]:
                if re.search(keyword, command):
                    contained_keyword = keyword
            if contained_keyword != "" and len(inputs[input_type][1]):
                for antiword in inputs[input_type][1]:
                    if re.search(antiword, command):
                        contained_keyword = ""
        if contained_keyword != "":
            command_index = input_type
            break

    #Perform the appropriate command
    if command_index == 0:
        give_time()
    elif command_index == 1:
        search(contained_keyword, command)
    elif command_index == 2:
        should(command)
    elif command_index == 3:
        launch_program(command)
    elif command_index == 4:
        print(get_response(6))
    elif command_index == 5:
        schedule_shutdown(command)
    elif command_index == 6:
        schedule_command(command)
    elif command_index == 15:
        tell_joke()
    elif command_index == 7:
        print(get_response(15))
        sys.exit()
    else:
        print(get_response(16))
