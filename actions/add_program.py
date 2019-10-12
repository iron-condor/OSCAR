"""Prompts the user to add a new program to the list of programs that OSCAR knows about"""
import pickle
import os
import sys
from pathlib import Path
import oscar_defaults
import oscar_functions
from config_structures import Program

def add_program(runtime):
    """Method that prompts the user to add a new program to OSCAR's list"""
    print(runtime.responses["prompt_select_file_for_new_program"].get_line())
    file_path = None
    program_aliases = []
    #If the user wants a file manager
    if runtime.settings["use_file_manager"].state:
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
            print(runtime.responses["disp_not_valid_file_path"].get_line())
    #If the user has already registered this program before
    if file_path in [p.executable_path for p in runtime.programs]:
        print(runtime.responses["program_already_registered"].get_line())
        return
    #Prompt the user for the program's name
    print(runtime.responses["prompt_for_aliases"].get_line())
    print(runtime.responses["tutorial_enter_multiple_names"].get_line())
    while True:
        aliases_raw = input()
        #If the user entered more than one name
        if ", " in aliases_raw:
            aliases = aliases_raw.split(", ")
            already_exists = False
            existing_aliases = []
            for alias_group in [p.aliases for p in runtime.programs]:
                for alias in alias_group:
                    if alias in aliases:
                        existing_aliases.append(alias)
                        already_exists = True
            if already_exists:
                print(runtime.responses["all_aliases_in_use"].get_line())
            else:
                program_aliases = aliases
                break
        else:
            already_exists = False
            for alias_group in [p.aliases for p in runtime.programs]:
                for alias in alias_group:
                    if alias == aliases_raw:
                        already_exists = True
            if already_exists:
                print(runtime.responses["all_aliases_in_use"].get_line())
            else:
                program_aliases = [aliases_raw]
                break
    runtime.programs.append(Program(program_aliases, file_path))
    programs_array = runtime.programs
    directory = None
    programs_file = None
    if sys.platform == "win32":
        directory = "C:\\Program Files(x86)\\Oscar"
        programs_file = Path(directory + "\\programs")
    elif sys.platform == "darwin":
        directory = str(Path.home()) + "/Library/Preferences/Oscar"
        programs_file = Path(directory + "/programs")
    else:
        directory = str(Path.home()) + "/.config/oscar"
        programs_file = Path(directory + "/programs")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(programs_file, 'wb') as updated_programs:
        pickle.dump(programs_array, updated_programs)
    print(runtime.responses["program_has_been_added"].get_line())
