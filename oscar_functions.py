"""Module that contains code commonly used by actions, and core OSCAR components"""
import os
import sys
import subprocess
import collections
import re
from tkinter import filedialog
from random import randint
from actions import *
from classes import *
from tkinter import *
import oscar_defaults
import actions

def get_directory() -> "string":
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

def subprocess_cmd(bash_command):
    """Runs commands as a detached subprocess.

    Used in command scheduling, alongside with the /usr/bin/sleep command.
    Sample input: subprocess_cmd("sleep 60 && poweroff")
    """
    subprocess.Popen(bash_command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setpgrp)

def open_file_manager(location) -> str:
    """Opens a file manager window for the user to select a file from

    Returns
    -------
    String
        The path to the file chosen by the user
    """
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir = location, title = "Select file")
    return root.filename

def close_oscar(self):
    """Closes the program.

    This function exists due to an error in jsonpickle, in which sys.exit() is mistakenly serialized as a dictionary
    """
    sys.exit()

def convert_and_format_time(total_time) -> str:
    """Takes time in seconds as an argument, and converts it to the lowest expressable value in days/hours/minutes/seconds

    Arguments
    ---------
    total_time : float
        The total time in seconds until an event

    Returns
    -------
    String
        A string that reflects the time until an event happens in days/hours/minutes/seconds
        Ex: "2 days 5 hours 3 minutes and 10 seconds"
        Ex: "5 minutes and 30 seconds"
    """
    time_string = ""
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
    seconds = float(total_time)
    if seconds > 0:
        if time_string:
            time_string += "and"
        if seconds > 1 or seconds < 1:
            time_string += " %.3f seconds" % seconds
        else:
            time_string += " 1 second"
    else:
        time_string = time_string[:len(time_string) - 1]
    return time_string

class Runtime:
    """The runtime instance that OSCAR runs through"""

    def __init__(self):
        #The responses, inputs, settings, and groups lists to be loaded or generated
        self.responses = {}
        self.inputs = {}
        self.settings = {}
        self.groups = {}
        #Dictionary of API keys to be loaded or generated
        self.api_keys = {}

        #Boolean that tells if it's the user's first time launching OSCAR
        self.first_time = True
        #String that stores the command that the user last entered
        self.command = ""

    def get_yes_no(self, confirm, parsing_type=None) -> bool:
        """Decides if a particular string is a positive or negative statement.

        In other words, it can read a string as yes/no.

        Arguments
        ---------
        confirm : String
            Variable that contains the string to be parsed
        parsing_type (optional) : any
            If this variable is defined, it checks if the string means no
            If the variable is left undefined, it checks if the string means yes

        Returns
        -------
        Boolean
            The boolean value indicating whether or not the string means yes or no.
            If passed with a parsing_type specified, the method will return True if the string
            means no, and False if the string means Yes.
            If passed without a parsing_type specified, the method will return True if the string
            means Yes, and False if the string means No.

        May be deprecated in the future, and replaced with a classification algorithm
        """
        contained_yes = ""
        if parsing_type is None:
            for i in range(0, len(self.inputs["input_is_yes"].positive_matches)):
                if contained_yes == "":
                    if re.search(self.inputs["input_is_yes"].positive_matches[i], confirm):
                        contained_yes = self.inputs["input_is_yes"].positive_matches[i]
                    if contained_yes != "" and len(self.inputs["input_is_yes"].negative_matches):
                        for antiword in self.inputs["input_is_yes"].negative_matches:
                            if re.search(antiword, confirm):
                                contained_yes = ""
                if contained_yes != "":
                    return True
            return False

        for i in range(0, len(self.inputs["input_is_no"].positive_matches)):
            if contained_yes == "":
                if re.search(self.inputs["input_is_no"].positive_matches[i], confirm):
                    contained_yes = self.inputs["input_is_no"].positive_matches[i]
                if contained_yes != "" and len(self.inputs["input_is_no"].negative_matches):
                    for antiword in self.inputs["input_is_no"].negative_matches:
                        if re.search(antiword, confirm):
                            contained_yes = ""
            else:
                return True

    def open_in_browser(self, url):
        """Opens URL in the user's browser. If it fails, prompt the user to open it theirself."""
        if sys.platform == 'win32':
            print(self.responses["opening_link"].get_line())
            os.startfile(url)
        elif sys.platform == 'darwin':
            print(self.responses["opening_link"].get_line())
            subprocess.Popen(['open', url])
        else:
            try:
                print(self.responses["opening_link"].get_line())
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print(self.responses["cant_open_url"].get_line("<url>", url))

    def schedule(self) -> float:
        """Returns the time in seconds until a scheduled event. Interprets text from the user in standard time units

        Returns
        -------
        float
            Returns the total time in seconds until a scheduled event
        """
        time_units = collections.OrderedDict([
            ("\\bsecs?\\b|\\bseconds?\\b", 1),
            ("\\bmins?\\b|\\bminutes?\\b", 60),
            ("\\bhours?\\b", 3600),
            ("\\bdays?\\b", 86400)
        ])
        total_time = 0.0
        for key in time_units:
            occurences = re.findall(key, self.command)
            if occurences:
                for item in occurences:
                    index = self.command.find(item)
                    index = self.command.rfind(' ', 0, index - 1) + 1
                    #This bit's here to ignore false positives.
                    #For example: "I'll be heading to bed in a minute, so can you shut down my computer in 2 min?"
                    try:
                        num = float(self.command[index:(self.command.find(' ', index))])
                        total_time += (num * time_units[key])
                    except Exception:
                        continue
        if total_time != 0:
            time_string = convert_and_format_time(total_time)
            confirm = input(self.responses["confirm_scheduled_time"].get_line("<time_string>", time_string).lower())
            while True:
                if self.get_yes_no(confirm):
                    return total_time
                elif self.get_yes_no(confirm, 1):
                    print(self.responses["scheduled_task_cancelled"].get_line())
                    break
                else:
                    confirm = input(self.responses["confirm_yes_no"].get_line()).lower()
        else:
            print(self.responses["rephrase_scheduled_task"].get_line())

    def receive_command(self):
        """Receives the user's command and processes the input appropriately"""
        if self.first_time:
            self.responses = oscar_defaults.responses_dict
            self.inputs = oscar_defaults.inputs_dict
            self.settings = oscar_defaults.settings_dict
            self.groups = oscar_defaults.groups_array
            self.programs = oscar_defaults.programs_array
            self.contacts = oscar_defaults.contacts_array
            self.api_keys = oscar_defaults.api_keys
            actions.greet(self)
            self.first_time = False
        self.command = input("").lower()
        contained_keyword = ""
        found_keyword = False
        for input_type in self.inputs:
            if contained_keyword == "" and self.inputs[input_type].function:
                for keyword in self.inputs[input_type].positive_matches:
                    if re.search(keyword, self.command):
                        contained_keyword = keyword
                if contained_keyword != "" and len(self.inputs[input_type].negative_matches):
                    for antiword in self.inputs[input_type].negative_matches:
                        if re.search(antiword, self.command):
                            contained_keyword = ""
            if contained_keyword != "":
                found_keyword = True
                self.inputs[input_type].function(self, *self.inputs[input_type].parameters)
                break
        if not found_keyword:
            print(self.responses["ambiguous_request"].get_line())
