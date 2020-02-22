"""Module that contains a method for importing the user's contacts from a .vcf file"""
import vobject
from classes import Contact
import pickle
import os
import sys
from pathlib import Path
import oscar_functions

def import_contacts(runtime):
    """Imports the user's contacts from a VCF file

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    try:
        print(runtime.responses["prompt_contacts_file_location"].get_line())
        file_path = None
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
                #If the file is there, break out of the loop
                if os.path.isfile(file_path):
                    break
                #If it isn't, prompt the user to reselect the file
                print(runtime.responses["disp_not_valid_file_path"].get_line())

        s = None
        with open(file_path, 'r') as file:
            s = file.read();
        v = vobject.readComponents(s)
        contacts = []
        for item in v:
            contacts.append(item)

        arr = []

        i = 0

        for thing in contacts:
            flags = [x for x in thing.contents]
            arr.append({})
            for flag in flags:
                string = str(thing.contents[flag])
                string = string[string.index("}") + 1:-2].strip()
                arr[i][flag] = string
            i += 1

        contacts = arr
        contacts = [Contact(vcf_dict=c) for c in contacts]

        directory = None
        contacts_file = None

        if sys.platform == "win32":
            directory = "C:\\Program Files(x86)\\Oscar"
            contacts_file = Path(directory + "\\contacts")
        elif sys.platform == "darwin":
            directory = str(Path.home()) + "/Library/Preferences/Oscar"
            contacts_file = Path(directory + "/contacts")
        else:
            directory = str(Path.home()) + "/.config/oscar"
            contacts_file = Path(directory + "/contacts")
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(contacts_file, 'wb') as updated_contacts:
            pickle.dump(contacts, updated_contacts)
        runtime.contacts = contacts
        print(runtime.responses["contacts_imported"].get_line())
    except Exception:
        print(runtime.responses["failed_to_import_contacts"].get_line())
