"""Module that provides a method to let the user configure their settings"""
import oscar_functions, oscar_defaults
import sys, json, re, pickle
from pathlib import Path

def configure_settings(runtime):
    """Allows the user to view and adjust their settings

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    print(runtime.responses["prompt_configure_settings"].get_line())
    setting_changed = False
    print("Name: " + runtime.settings["name"].state)
    clock_type = "12-hour" if runtime.settings["use_12_hour_clock"].state else "24-hour"
    print("Clock type: " + clock_type)
    path_chooser = "File manager" if runtime.settings["use_file_manager"].state else "Let me type it out"
    print("File path chooser: " + path_chooser)
    to_change = input("").lower()
    if "name" in to_change:
        runtime.settings["name"].state = input("Name: ")
        setting_changed = True
    if "clock" in to_change:
        clock_type = None
        clock_type_raw = input("New clock type: ")
        for clock_string in runtime.inputs["twenty_four_hour_clock_input"].positive_matches:
            if re.search(clock_string, clock_type_raw):
                clock_type = 0
        if clock_type == None:
            for clock_string in runtime.inputs["twelve_hour_clock_input"].positive_matches:
                if re.search(clock_string, clock_type_raw):
                    clock_type = 1
        runtime.settings["use_12_hour_clock"].state = clock_type
        setting_changed = True
    if "file" in to_change or "path" in to_change:
        path_type = None
        path_type_raw = input("File path chooser: ")
        for path_string in runtime.inputs["file_manager_input"].positive_matches:
            if re.search(path_string, path_type_raw):
                path_type = 1
        if path_type == None:
            for path_string in runtime.inputs["type_out_paths_input"].positive_matches:
                if re.search(path_string, path_type_raw):
                    path_type = 0
        runtime.settings["use_file_manager"].state = path_type
        setting_changed = True
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
        print(runtime.responses["disp_settings_have_updated"].get_line())
    else:
        print(runtime.responses["disp_settings_not_updated"].get_line())
