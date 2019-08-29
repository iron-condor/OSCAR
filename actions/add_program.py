"""Prompts the user to add a new program to the list of programs that OSCAR knows about"""
import oscar_functions, oscar_defaults
import os, sys, json
from pathlib import Path

def add_program():
    """Method that prompts the user to add a new program to OSCAR's list"""
    print(oscar_functions.get_response(38))
    #If the user wants a file manager
    file_path = None
    if oscar_functions.settings[2]:
        file_path = oscar_functions.open_file_manager(Path.home())
        #If the user didn't choose a file
        if len(file_path) == 0:
            return
    #If the user prefers to type out paths manually
    else:
        while True:
            file_path = input()
            program = file_path.split(" ")[0]
            #If the file is there, break out of the loop
            if os.path.isfile(program):
                break
            #If it isn't, prompt the user to reselect the file
            else:
                print(oscar_functions.get_response(39))
    #If the user has already registered this program before
    if file_path in oscar_functions.groups[0][1]:
        print(oscar_functions.get_response(43))
        return
    #Add the file path to the groups array
    oscar_functions.groups[0][1].append(file_path)
    #Prompt the user for the program's name
    print(oscar_functions.get_response(40))
    print(oscar_functions.get_response(41))
    while True:
        aliases_raw = input()
        #If the user entered more than one name
        if ", " in aliases_raw:
            aliases = aliases_raw.split(", ")
            already_exists = False
            existing_aliases = []
            for alias_group in oscar_functions.groups[0][0]:
                for alias in alias_group:
                    if alias in aliases:
                        existing_aliases.append(alias)
                        already_exists = True
            if already_exists:
                print(oscar_functions.get_response(44))
            else:
                oscar_functions.groups[0][0].append(aliases)
                break
        else:
            already_exists = False
            for alias_group in oscar_functions.groups[0][0]:
                for alias in alias_group:
                    if alias == aliases_raw:
                        already_exists = True
            if already_exists:
                print(oscar_functions.get_response(44))
            else:
                aliases_raw = [aliases_raw]
                oscar_functions.groups[0][0].append(aliases_raw)
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
    print(oscar_functions.get_response(42))
