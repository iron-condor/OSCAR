# Developer: iron-condor
# Dependencies: duckduckgo-python3 (find on github), xdg-utils
import oscar_defaults
import oscar_functions
from sys import platform
from pathlib import Path
import json
import os
import re
import getpass

#Walks the user through generating their settings
def walkthrough():
    inputs_array = oscar_defaults.inputs_array
    settings_array = oscar_defaults.settings_array
    introduction = ""
    username_raw = input(oscar_functions.get_response(24))
    for intro in inputs_array[14][0]:
        if re.search(intro, username_raw):
            introduction = intro
    username = username_raw
    if introduction != "":
        username = username_raw[(re.search(introduction, username_raw).end()) + 1:]
    settings_array[0] = username

    clock_type = None
    while clock_type == None:
        clock_type_raw = input(oscar_functions.get_response(25, "<user>", username))
        for clock_string in inputs_array[12][0]:
            if re.search(clock_string, clock_type_raw):
                clock_type = 0
        if clock_type == None:
            for clock_string in inputs_array[13][0]:
                if re.search(clock_string, clock_type_raw):
                    clock_type = 1
    if clock_type:
        print(oscar_functions.get_response(27, "<user>", username))
    else:
        print(oscar_functions.get_response(26, "<user>", username))
    settings_array[1] = clock_type


#Loads the responses file if it exists. If it doesn't, one is automatically generated for the user.
def load_responses():
    responses_array = oscar_defaults.responses_array
    directory = None
    responses_file = None
    if sys.platform == "win32":
        directory = "C:\\Program Files(x86)\\Oscar"
        responses_file = Path(directory + "\\responses")
    elif sys.platform == "darwin":
        directory = str(Path.home()) + "/Library/Preferences/Oscar"
        responses_file = Path(directory + "/responses")
    else:
        directory = str(Path.home()) + "/.config/oscar"
        responses_file = Path(directory + "/responses")
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        responses = open(responses_file, 'r')
    except FileNotFoundError:
        print("It doesn't seem like you have a responses config file generated. I'll do that quickly.")
        responses = open(responses_file, 'w')
        responses.write(json.dumps(responses_array, indent=4))
        print("...and done! You can find it here: " + str(responses_file))
    else:
        oscar_defaults.responses_array = json.load(responses)

#Loads the inputs file if it exists. If it doesn't, one is automatically generated for the user.
def load_inputs():
    inputs_array = oscar_defaults.inputs_array
    directory = None
    inputs_file = None
    if sys.platform == "win32":
        directory = "C:\\Program Files(x86)\\Oscar"
        inputs_file = Path(directory + "\\inputs")
    elif sys.platform == "darwin":
        directory = str(Path.home()) + "/Library/Preferences/Oscar"
        inputs_file = Path(directory + "/inputs")
    else:
        directory = str(Path.home()) + "/.config/oscar"
        inputs_file = Path(directory + "/inputs")
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        inputs = open(inputs_file, 'r')
    except FileNotFoundError:
        print("I don't see an input config. Let me take care of that.")
        inputs = open(inputs_file, 'w')
        inputs.write(json.dumps(inputs_array, indent=4))
        print("There you go! If you need it, it's here: " + str(inputs_file))
    else:
        oscar_defaults.inputs_array = json.load(inputs)

#Loads the settings file if it exists. If it doesn't, it prompts the user to select his/her settings, or allows the user to let oscar generate the defaults.
def load_settings():
    settings_array = oscar_defaults.settings_array
    directory = None
    if sys.platform == "win32":
        directory = "C:\\Program Files(x86)\\Oscar"
        settings_file = Path(directory + "\\settings")
    elif sys.platform == "darwin":
        directory = str(Path.home()) + "/Library/Preferences/Oscar"
        settings_file = Path(directory + "/settings")
    else:
        directory = str(Path.home()) + "/.config/oscar"
        settings_file = Path(directory + "/settings")
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        settings = open(settings_file, 'r')
    except FileNotFoundError:
        confirm = input("It doesn't seem like you have a settings file yet. Would you like me to walk you through setting it up, or just keep the defaults for now?\n")
        inputs_array = oscar_defaults.inputs_array
        do_walkthrough = None
        contained_walkthrough = ""
        for i in range(0, len(inputs_array[10][0])):
            if contained_walkthrough == "":
                if re.search(inputs_array[10][0][i],confirm):
                    contained_walkthrough = inputs_array[10][0][i]
                if contained_walkthrough != "" and len(inputs_array[10][1]):
                    for antiword in inputs_array[10][1]:
                        if re.search(antiword, confirm):
                            contained_walkthrough = ""
            if contained_walkthrough != "":
                do_walkthrough = True
                break
        if (do_walkthrough):
            walkthrough();
        else:
            settings_array[0] = getpass.getuser()
        settings = open(settings_file, 'w')
        settings.write(json.dumps(settings_array, indent=4))
        print("Finished. It's right here: " + str(settings_file))
    else:
        oscar_defaults.settings_array = json.load(settings)

load_responses()
load_inputs()
load_settings()
while (True):
    oscar_functions.receive_command()
