"""Module that contains a function for updating the user's computer"""
from os import listdir
from os.path import isfile, join
import oscar_functions
from getpass import getpass
import sys

def update_computer(runtime):
    """Updates the user's computer if possible, prompting them for their root password

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    if sys.platform == "linux":
        installed_programs = [f for f in listdir("/usr/bin") if isfile(join("/usr/bin", f))]

        if "apt" in installed_programs:
            password = getpass(runtime.responses["prompt_for_password"].get_line())
            oscar_functions.subprocess_cmd("echo " + password + "| sudo -S apt update && " + "echo " + password + "| sudo -S apt -y upgrade")
            print(runtime.responses["computer_is_updating"].get_line())
        elif "dnf" in installed_programs:
            password = getpass(runtime.responses["prompt_for_password"].get_line())
            oscar_functions.subprocess_cmd("echo " + password + "| sudo -S dnf -y upgrade")
            print(runtime.responses["computer_is_updating"].get_line())
        elif "pacman" in installed_programs:
            password = getpass(runtime.responses["prompt_for_password"].get_line())
            oscar_functions.subprocess_cmd("echo " + password + "| sudo -S pacman -Syu --noconfirm")
            print(runtime.responses["computer_is_updating"].get_line())
        elif "emerge" in installed_programs:
            password = getpass(runtime.responses["prompt_for_password"].get_line())
            oscar_functions.subprocess_cmd("echo " + password + "| sudo -S emerge -uDN @world")
            print(runtime.responses["computer_is_updating"].get_line())
        else:
            print(runtime.responses["updating_not_supported_on_this_platform"].get_line())

        password = None
    else:
        print(runtime.responses["updating_not_supported_on_this_platform"].get_line())
