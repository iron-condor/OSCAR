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
from tkinter import filedialog
from tkinter import *
import pyjokes
from pathlib import Path
import json

responses = []
inputs = []
settings = []
groups = []
firstTime = True
command = None

#Runs commands as a detached subprocess. In other words, if OSCAR is closed, the commands ran here continue existing.
#Used in command scheduling, alongside with the /usr/bin/sleep command.
#Sample input: subprocess_cmd("sleep 60 && poweroff")
def subprocess_cmd(bash_command):
    subprocess.Popen(bash_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setpgrp)

def open_file_manager(location):
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir = location, title = "Select file")
    return root.filename

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
def search():
    global command, inputs
    identifier_string = None
    for string in inputs[1][0]:
        if re.search(string, command):
            identifier_string = string
            break
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
                if answer.startswith("https://www.youtu.be") or answer.startswith("https://www.youtube.com"):
                    confirm = input(get_response(31))
                else:
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
def schedule():
    global command
    time_units = collections.OrderedDict([
        ("\\bsecs?\\b|\\bseconds?\\b", 1),
        ("\\bmins?\\b|\\bminutes?\\b", 60),
        ("\\bhours?\\b", 3600),
        ("\\bdays?\\b", 86400)
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
def schedule_command():
    global command
    time = schedule()
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
def schedule_shutdown():
    global command
    time = schedule()
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
def should():
    global command
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

def launch_program():
    global command
    command = command.lower()
    confirmed_aliases = []
    alias_paths = []
    #Searches the "command" for aliases, and adds their info to the above lists
    for alias_group in groups[0][0]:
        for alias in alias_group:
            if re.search(alias, command):
                #Add the alias to the list
                confirmed_aliases.append(alias)
                #Add its file path to the list
                alias_paths.append(groups[0][1][groups[0][0].index(alias_group)])
    for path in alias_paths:
        subprocess_cmd(path)
    if (len(confirmed_aliases) > 1):
        print(get_response(28))
    elif (len(confirmed_aliases) > 0):
        print(get_response(29))
    else:
        print(get_response(30))

#Allows the user to view and adjust their settings
def configure_settings():
    global settings, inputs;
    print(get_response(32))
    setting_changed = 0
    print("Name: " + settings[0])
    clock_type = "12-hour" if settings[1] else "24-hour"
    print("Clock type: " + clock_type)
    path_chooser = "File manager" if settings[2] else "Let me type it out"
    print("File path chooser: " + path_chooser)
    to_change = input("").lower()
    if "name" in to_change:
        settings[0] = input("Name: ")
        setting_changed = 1
    if "clock" in to_change:
        clock_type = None
        clock_type_raw = input("New clock type: ")
        for clock_string in inputs[12][0]:
            if re.search(clock_string, clock_type_raw):
                clock_type = 0
        if clock_type == None:
            for clock_string in inputs[13][0]:
                if re.search(clock_string, clock_type_raw):
                    clock_type = 1
        settings[1] = clock_type
        setting_changed = 1
    if "file" in to_change or "path" in to_change:
        path_type = None
        path_type_raw = input("File path chooser: ")
        for path_string in inputs[16][0]:
            if re.search(path_string, path_type_raw):
                path_type = 1
        if path_type == None:
            for path_string in inputs[17][0]:
                if re.search(path_string, path_type_raw):
                    path_type = 0
        settings[2] = path_type
        setting_changed = 1
    if setting_changed:
        settings_file = None
        if sys.platform == "win32":
            directory = "C:\\Program Files(x86)\\Oscar"
            settings_file = Path(directory + "\\settings")
        elif sys.platform == "darwin":
            directory = str(Path.home()) + "/Library/Preferences/Oscar"
            settings_file = Path(directory + "/settings")
        else:
            directory = str(Path.home()) + "/.config/oscar"
            settings_file = Path(directory + "/settings")
        final_settings = open(settings_file, 'w')
        final_settings.write(json.dumps(settings, indent=4))
        print(get_response(36))
    else:
        print(get_response(37))


#Adds a program to the list of programs that Oscar recognizes
def add_program():
    global groups
    print(get_response(38))
    #If the user wants a file manager
    file_path = None
    if settings[2]:
        file_path = open_file_manager(Path.home())
    #If the user prefers to type out paths manually
    else:
        while True:
            file_path = input()
            #If the file is there, break out of the loop
            if os.path.isfile(file_path):
                break
            #If it isn't, prompt the user to reselect the file
            else:
                print(get_response(39))
    #If the user has already registered this program before
    if file_path in groups[0][1]:
        print(get_response(43))
        return
    #Add the file path to the groups array
    groups[0][1].append(file_path)
    #Prompt the user for the program's name
    print(get_response(40))
    print(get_response(41))
    while True:
        aliases_raw = input()
        #If the user entered more than one name
        if ", " in aliases_raw:
            aliases = aliases_raw.split(", ")
            already_exists = False
            existing_aliases = []
            for alias_group in groups[0][0]:
                for alias in alias_group:
                    if alias in aliases:
                        existing_aliases.append(alias)
                        already_exists = True
            if already_exists:
                print(get_response(44))
            else:
                groups[0][0].append(aliases)
                break
        else:
            already_exists = False
            for alias_group in groups[0][0]:
                for alias in alias_group:
                    if alias == aliases_raw:
                        already_exists = True
            if already_exists:
                print(get_response(44))
            else:
                aliases_raw = [aliases_raw]
                groups[0][0].append(aliases_raw)
                break
    groups_array = oscar_defaults.groups_array
    directory = None
    groups_file = None
    if sys.platform == "win32":
        directory = "C:\\Program Files(x86)\\Oscar"
        groups_file = Path(directory + "\\groups")
    elif sys.platform == "darwin":
        directory = str(Path.home()) + "/Library/Preferences/Oscar"
        groups_file = Path(directory + "/groups")
    else:
        directory = str(Path.home()) + "/.config/oscar"
        groups_file = Path(directory + "/groups")
    if not os.path.exists(directory):
        os.makedirs(directory)
    updated_groups = open(groups_file, 'w')
    updated_groups.write(json.dumps(groups_array, indent=4))
    print(get_response(42))

#Responds to the user thanking oscar
def thanks():
    print(get_response(6))

#Closes the program. This function exists due to an error in jsonpickle, in which sys.exit() is mistakenly serialized as a dictionary
def close_oscar():
    sys.exit()

#Receives the command and processes the input appropriately
def receive_command():
    global responses, inputs, settings, groups, firstTime, command
    if firstTime:
        responses = oscar_defaults.responses_array
        inputs = oscar_defaults.inputs_array
        settings = oscar_defaults.settings_array
        groups = oscar_defaults.groups_array
        greet()
        firstTime = False
    command = input("").lower()
    contained_keyword = ""
    found_keyword = False
    for input_type in range(0, len(inputs)):
        if contained_keyword == "" and inputs[input_type][2] != 0:
            for keyword in inputs[input_type][0]:
                if re.search(keyword, command):
                    contained_keyword = keyword
            if contained_keyword != "" and len(inputs[input_type][1]):
                for antiword in inputs[input_type][1]:
                    if re.search(antiword, command):
                        contained_keyword = ""
        if contained_keyword != "":
            found_keyword = True
            inputs[input_type][2]()
            break
    if not found_keyword:
        print(get_response(16))
