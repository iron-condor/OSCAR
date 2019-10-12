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
        self.responses_dict = oscar_defaults.responses_dict
        self.inputs_dict = oscar_defaults.inputs_dict
        self.settings_dict = oscar_defaults.settings_dict
        self.programs_array = oscar_defaults.programs_array
        self.groups_array = oscar_defaults.groups_array
        self.load_responses()
        self.load_inputs()
        self.load_programs()
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
        """Returns the directory that OSCAR uses to store his files. OS-dependent.

        Returns
        -------
        String
            The path to the directory that OSCAR saves his files in
        """
        if sys.platform == "win32":
            return "C:\\Program Files(x86)\\Oscar"
        elif sys.platform == "darwin":
            return str(Path.home()) + "/Library/Preferences/Oscar"
        else:
            return str(Path.home()) + "/.config/oscar"

    def walkthrough(self):
        """Walks the user through the available setting options, and assigns them from user choice"""
        introduction = ""
        username_raw = input(self.responses_dict["whats_your_name"].get_line())
        for intro in self.inputs_dict["name_input"].positive_matches:
            if re.search(intro, username_raw):
                introduction = intro
        username = username_raw
        if introduction != "":
            username = username_raw[(re.search(introduction, username_raw).end()) + 1:]
        self.settings_dict["name"].state = username

        use_twelve_hour_clock = None
        while use_twelve_hour_clock is None:
            clock_type_raw = input(self.responses_dict["prompt_clock_type"].get_line("<user>", username))
            for clock_string in self.inputs_dict["twenty_four_hour_clock_input"].positive_matches:
                if re.search(clock_string, clock_type_raw):
                    use_twelve_hour_clock = False
            if use_twelve_hour_clock is None:
                for clock_string in self.inputs_dict["twelve_hour_clock_input"].positive_matches:
                    if re.search(clock_string, clock_type_raw):
                        clock_type = True
        if use_twelve_hour_clock:
            print(self.responses_dict["selected_12hr_clock"].get_line("<user>", username))
        else:
            print(self.responses_dict["selected_12hr_clock"].get_line("<user>", username))
        self.settings_dict["use_twelve_hour_clock"].state = use_twelve_hour_clock

        use_file_manager = None
        while use_file_manager is None:
            path_type_raw = input(self.responses_dict["prompt_select_files_method"].get_line())
            for path_string in self.inputs_dict["file_manager_input"].positive_matches:
                if re.search(path_string, path_type_raw):
                    use_file_manager = True
            if use_file_manager is None:
                for path_string in self.inputs_dict["type_out_paths_input"].positive_matches:
                    if re.search(path_string, path_type_raw):
                        use_file_manager = False
        if use_file_manager:
            print(self.responses_dict["disp_chosen_to_use_file_manager"].get_line())
        else:
            print(self.responses_dict["disp_chosen_to_type_out_paths"].get_line())
        self.settings_dict["use_file_manager"].state = use_file_manager


    def load_responses(self):
        """Loads the responses file if it exists. If it doesn't exist, the method generates one.

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\responses
            macOS: ~/Library/Preferences/Oscar/responses
            linux: ~/.config/oscar/responses
        """
        responses = self.save_or_load_config("responses", self.responses_dict)
        if responses:
            self.responses_dict_dict = responses

    def load_inputs(self):
        """Loads the inputs file if it exists. If it doesn't exist, the method generates one

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\inputs
            macOS: ~/Library/Preferences/Oscar/inputs
            linux: ~/.config/oscar/inputs
        """
        inputs = self.save_or_load_config("inputs", self.inputs_dict)
        if inputs:
            oscar_defaults.inputs_dict = inputs

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
        settings = self.save_or_load_config("settings", self.settings_dict)
        if settings:
            oscar_defaults.settings_dict = settings
        else:
            confirm = input("It doesn't seem like you have a settings file yet. "
                            "Would you like me to walk you through setting it up"
                            ", or just keep the defaults for now?\n")
            do_walkthrough = None
            contained_walkthrough = ""
            for i in range(0, len(self.inputs_dict["walkthrough_input"].positive_matches)):
                if contained_walkthrough == "":
                    if re.search(self.inputs_dict["walkthrough_input"].positive_matches[i], confirm):
                        contained_walkthrough = self.inputs_dict["walkthrough_input"].positive_matches[i]
                    if contained_walkthrough != "" and len(self.inputs_dict["walkthrough_input"].negative_matches):
                        for antiword in self.inputs_dict["walkthrough_input"].negative_matches:
                            if re.search(antiword, confirm):
                                contained_walkthrough = ""
                if contained_walkthrough != "":
                    do_walkthrough = True
                    break
            if do_walkthrough:
                self.walkthrough()
            else:
                self.settings_dict["name"].state = getpass.getuser()
            self.save_or_load_config("settings", self.settings_dict, force_write=True)

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

    def load_programs(self):
        """Loads the programs file if it exists. If it doesn't exist, a blank one is generated.

        Files
        -----
        Creates a file at...

            Windows: C:\\Program Files(x86)\\Oscar\\programs
            macOS: ~/Library/Preferences/Oscar/programs
            linux: ~/.config/oscar/programs
        """
        programs = self.save_or_load_config("programs", self.programs_array)
        if programs:
            oscar_defaults.programs_array = programs
