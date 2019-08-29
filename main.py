"""Module that starts the program, and loads/saves files"""
# Dependencies: duckduckgo-python3, jsonpickle, xdg-utils (if using linux)
import oscar_defaults
import oscar_functions
import sys
from pathlib import Path
import jsonpickle
import json
import os
import re
import getpass

def walkthrough():
    """Walks the user through the available setting options, and assigns them based on user choice"""
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

    path_type = None
    while path_type == None:
        path_type_raw = input(oscar_functions.get_response(33))
        for path_string in inputs_array[16][0]:
            if re.search(path_string, path_type_raw):
                path_type = 1
        if path_type == None:
            for path_string in inputs_array[17][0]:
                if re.search(path_string, path_type_raw):
                    path_type = 0
    if path_type:
        print(oscar_functions.get_response(34))
    else:
        print(oscar_functions.get_response(35))
    settings_array[2] = path_type


def load_responses():
    """Loads the responses file if it exists. If it doesn't exist, the method generates one.

    Files
    -----
    Creates a file at...

        Windows: C:\\Program Files(x86)\\Oscar\\responses
        macOS: ~/Library/Preferences/Oscar/responses
        linux: ~/.config/oscar/responses
    """
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

def load_inputs():
    """Loads the inputs file if it exists. If it doesn't exist, the method generates one

    Files
    -----
    Creates a file at...

        Windows: C:\\Program Files(x86)\\Oscar\\inputs
        macOS: ~/Library/Preferences/Oscar/inputs
        linux: ~/.config/oscar/inputs
    """
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
        inputs.write(jsonpickle.dumps(inputs_array))
        print("There you go! If you need it, it's here: " + str(inputs_file))
    else:
        temp_loaded = inputs.read()
        oscar_defaults.inputs_array = jsonpickle.decode(temp_loaded)

def load_settings():
    """Loads the settings file if it exists. Otherwise, it prompts the user for the walkthrough

    If the settings file does not exist, the method will tell this to the user, and ask them if they would
    like to have OSCAR generate the file with defaults, or if they would like to be prompted about each of
    the settings, in order to choose them.

    Files
    -----
    Creates a file at...

        Windows: C:\\Program Files(x86)\\Oscar\\settings
        macOS: ~/Library/Preferences/Oscar/settings
        linux: ~/.config/oscar/settings
    """
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

def load_groups():
    """Loads the groups file if it exists. If it doesn't exist, a blank one is generated.

    Files
    -----
    Creates a file at...

        Windows: C:\\Program Files(x86)\\Oscar\\groups
        macOS: ~/Library/Preferences/Oscar/groups
        linux: ~/.config/oscar/groups
    """
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
    try:
        groups = open(groups_file, 'r')
    except FileNotFoundError:
        print("It seems you've not got a groups file. Let me fix that for you quickly...")
        groups = open(groups_file, 'w')
        groups.write(json.dumps(groups_array, indent=4))
        print("Finished - have a file path: " + str(groups_file))
    else:
        oscar_defaults.groups_array = json.load(groups)

load_responses()
load_inputs()
load_groups()
load_settings()
while (True):
    oscar_functions.receive_command()
