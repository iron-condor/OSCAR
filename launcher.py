"""Module that starts the program, and loads/saves files"""
# Dependencies: duckduckgo-python3, jsonpickle, xdg-utils (if using linux)
import sys
from pathlib import Path
import pickle
import os
import re
import getpass
import oscar_defaults
import oscar_functions

class Launcher:
    """Manages loading OSCAR files and launching OSCAR"""

    def __init__(self):
        self.directory = self.get_directory()
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.responses_array = oscar_defaults.responses_array
        self.inputs_array = oscar_defaults.inputs_array
        self.settings_array = oscar_defaults.settings_array
        self.groups_array = oscar_defaults.groups_array
        self.load_responses()
        self.load_inputs()
        self.load_groups()
        self.load_settings()
        self.runtime = oscar_functions.Runtime()

    def start(self):
        """Starts OSCAR"""
        while True:
            self.runtime.receive_command()

    def save_or_load_config(self, filename, to_save, force_write=False):
        """Loads a config file if it exists, creates the file if it doesn't

        Arguments
        ---------
        filename : string
            The filename to be loaded from or saved to
        to_save : pickleable object or primitive
            The content to be saved, if the config doesn't exist
        force_write : boolean
            Determines whether or not the to_save variable is written
            regardless of whether or not there is a config already found

        Returns
        -------
        Pickleable object
            Returns the object stored in the file, if it exists.
            Otherwise, returns None
        """
        content_file = Path(self.directory + "/" + filename)
        try:
            content = open(content_file, 'rb')
        except FileNotFoundError:
            print("Generating", filename, "config...")
            with open(content_file, 'wb') as file:
                pickle.dump(to_save, file)
        else:
            if not force_write:
                return pickle.load(content)
        return None

    def get_directory(self) -> "string":
        """Returns the directory that OSCAR uses to store his files. OS-dependent."""
        if sys.platform == "win32":
            return "C:\\Program Files(x86)\\Oscar"
        elif sys.platform == "darwin":
            return str(Path.home()) + "/Library/Preferences/Oscar"
        else:
            return str(Path.home()) + "/.config/oscar"

    def walkthrough(self):
        """Walks the user through the available setting options, and assigns them from user choice"""
        introduction = ""
        username_raw = input(self.runtime.get_response(24))
        for intro in self.inputs_array[14][0]:
            if re.search(intro, username_raw):
                introduction = intro
        username = username_raw
        if introduction != "":
            username = username_raw[(re.search(introduction, username_raw).end()) + 1:]
        self.settings_array[0] = username

        clock_type = None
        while clock_type is None:
            clock_type_raw = input(self.runtime.get_response(25, "<user>", username))
            for clock_string in self.inputs_array[12][0]:
                if re.search(clock_string, clock_type_raw):
                    clock_type = 0
            if clock_type is None:
                for clock_string in self.inputs_array[13][0]:
                    if re.search(clock_string, clock_type_raw):
                        clock_type = 1
        if clock_type:
            print(self.runtime.get_response(27, "<user>", username))
        else:
            print(self.runtime.get_response(26, "<user>", username))
        self.settings_array[1] = clock_type

        path_type = None
        while path_type is None:
            path_type_raw = input(self.runtime.get_response(33))
            for path_string in self.inputs_array[16][0]:
                if re.search(path_string, path_type_raw):
                    path_type = 1
            if path_type is None:
                for path_string in self.inputs_array[17][0]:
                    if re.search(path_string, path_type_raw):
                        path_type = 0
        if path_type:
            print(self.runtime.get_response(34))
        else:
            print(self.runtime.get_response(35))
        self.settings_array[2] = path_type


    def load_responses(self):
        """Loads the responses file if it exists. If it doesn't exist, the method generates one.

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\responses
            macOS: ~/Library/Preferences/Oscar/responses
            linux: ~/.config/oscar/responses
        """
        responses = self.save_or_load_config("responses", self.responses_array)
        if responses:
            oscar_defaults.responses_array = responses

    def load_inputs(self):
        """Loads the inputs file if it exists. If it doesn't exist, the method generates one

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\inputs
            macOS: ~/Library/Preferences/Oscar/inputs
            linux: ~/.config/oscar/inputs
        """
        inputs = self.save_or_load_config("inputs", self.inputs_array)
        if inputs:
            oscar_defaults.inputs_array = inputs

    def load_settings(self):
        """Loads the settings file if it exists. Otherwise, it prompts the user for the walkthrough

        If the settings file does not exist, the method will tell this to the user, and ask them if
        they would like to have OSCAR generate the file with defaults, or if they would like to
        be prompted about each of the settings, in order to choose them.

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\settings
            macOS: ~/Library/Preferences/Oscar/settings
            linux: ~/.config/oscar/settings
        """
        settings = self.save_or_load_config("settings", self.settings_array)
        if settings:
            oscar_defaults.settings_array = settings
        else:
            confirm = input("It doesn't seem like you have a settings file yet."
                            "Would you like me to walk you through setting it up"
                            ", or just keep the defaults for now?\n")
            do_walkthrough = None
            contained_walkthrough = ""
            for i in range(0, len(self.inputs_array[10][0])):
                if contained_walkthrough == "":
                    if re.search(self.inputs_array[10][0][i], confirm):
                        contained_walkthrough = self.inputs_array[10][0][i]
                    if contained_walkthrough != "" and len(self.inputs_array[10][1]):
                        for antiword in self.inputs_array[10][1]:
                            if re.search(antiword, confirm):
                                contained_walkthrough = ""
                if contained_walkthrough != "":
                    do_walkthrough = True
                    break
            if do_walkthrough:
                self.walkthrough()
            else:
                self.settings_array[0] = getpass.getuser()
            self.save_or_load_config("settings", self.settings_array, force_write=True)

    def load_groups(self):
        """Loads the groups file if it exists. If it doesn't exist, a blank one is generated.

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\groups
            macOS: ~/Library/Preferences/Oscar/groups
            linux: ~/.config/oscar/groups
        """
        groups = self.save_or_load_config("groups", self.groups_array)
        if groups:
            oscar_defaults.groups_array = groups
