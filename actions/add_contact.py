"""Module that contains a function for adding and saving a new contact"""
import vobject
from classes import Contact
import pickle
import os
import sys
from pathlib import Path

def add_contact(runtime):
    """Manages the interaction with the user for adding a new contact

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
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

    contacts = []
    with open(contacts_file, 'rb') as file:
        contacts = pickle.load(file)

    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")

    contacts.append(Contact(first_name, last_name, phone_numbers=[phone_number]))

    print("Contact added successfully")

    with open(contacts_file, 'wb') as file:
        pickle.dump(contacts, file)
    runtime.contacts = contacts
    print("Contacts saved successfully")
