"""Module that provides method to let the user configure their settings"""
import oscar_functions, oscar_defaults
import sys, json, re, pickle
from pathlib import Path

def configure_settings(runtime):
    """Allows the user to view and adjust their settings"""
    print(runtime.get_response(32))
    setting_changed = 0
    print("Name: " + runtime.settings[0])
    clock_type = "12-hour" if runtime.settings[1] else "24-hour"
    print("Clock type: " + clock_type)
    path_chooser = "File manager" if runtime.settings[2] else "Let me type it out"
    print("File path chooser: " + path_chooser)
    to_change = input("").lower()
    if "name" in to_change:
        runtime.settings[0] = input("Name: ")
        setting_changed = 1
    if "clock" in to_change:
        clock_type = None
        clock_type_raw = input("New clock type: ")
        for clock_string in runtime.inputs[12][0]:
            if re.search(clock_string, clock_type_raw):
                clock_type = 0
        if clock_type == None:
            for clock_string in runtime.inputs[13][0]:
                if re.search(clock_string, clock_type_raw):
                    clock_type = 1
        runtime.settings[1] = clock_type
        setting_changed = 1
    if "file" in to_change or "path" in to_change:
        path_type = None
        path_type_raw = input("File path chooser: ")
        for path_string in runtime.inputs[16][0]:
            if re.search(path_string, path_type_raw):
                path_type = 1
        if path_type == None:
            for path_string in runtime.inputs[17][0]:
                if re.search(path_string, path_type_raw):
                    path_type = 0
        runtime.settings[2] = path_type
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
        with open(settings_file, 'wb') as final_settings:
            pickle.dump(runtime.settings, final_settings)
        print(runtime.get_response(36))
    else:
        print(runtime.get_response(37))
