"""Module that provides a method to let Oscar text people in the user's contacts"""
import vobject
from classes import Contact
import pickle
from pushbullet import Pushbullet
import re
import sys
from pathlib import Path
import os

def send_text(text, phone_number, api_key):
    """Sends a text from the first phone the user has associated with the API key

    Arguments
    ---------
    text : String
        The text to be sent to the user
    phone_number : String
        The phone number for the text to be sent to
    api_key : String
        The Pushbullet API key to be used
    """
    pb = Pushbullet(api_key=api_key)
    pb.push_sms(pb.devices[0], phone_number, text)

def text_person(runtime):
    """Interacts with the user to get the person they want to text, the text message, and the API key if necessary

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    if "pushbullet" in runtime.api_keys:
        contacts = runtime.contacts
        to_text = None
        skip_confirm = False
        for person in contacts:
            if (person.first_name is not None and re.search("\\b" + person.first_name.lower() + "\\b", runtime.command.lower())) \
            or (person.last_name is not None and re.search("\\b" + person.last_name.lower() + "\\b", runtime.command.lower())):
                if (len(person.phone_numbers) > 0):
                    if (str(person.first_name) + " " + str(person.last_name)).lower() in runtime.command.lower():
                        skip_confirm = True
                        to_text = person
                    else:
                        name_string = person.first_name
                        if person.first_name and person.last_name:
                            name_string = person.first_name + " " + person.last_name
                        elif person.first_name and not person.last_name:
                            name_string = person.first_name
                        elif person.last_name and not person.first_name:
                            name_string = person.last_name

                        confirm = input(runtime.responses["verify_person_to_text"].get_line("<person>", name_string)).lower()

                        if runtime.get_yes_no(confirm):
                            to_text = person
                else:
                    print(runtime.responses["no_phone_number_found"].get_line())
        if to_text is None:
            print(runtime.responses["cant_find_in_contacts"].get_line())
        else:
            text = input(runtime.responses["prompt_what_texting"].get_line())
            try:
                send_text(text, to_text.phone_numbers[0], runtime.api_keys["pushbullet"])
                print(runtime.responses["text_sent_successfully"].get_line())
            except Exception:
                print(runtime.responses["text_failed"].get_line())
    else:
        confirm = input(runtime.responses["prompt_want_to_add_api_key"].get_line("<api>", "Pushbullet")).lower()
        if runtime.get_yes_no(confirm):
            pb_api_key = input(runtime.responses["prompt_api_key"].get_line("<api>", "Pushbullet"))
            runtime.api_keys["pushbullet"] = pb_api_key

            api_keys_dict = runtime.api_keys
            directory = None
            api_keys_file = None
            if sys.platform == "win32":
                directory = "C:\\Program Files(x86)\\Oscar"
                api_keys_file = Path(directory + "\\api_keys")
            elif sys.platform == "darwin":
                directory = str(Path.home()) + "/Library/Preferences/Oscar"
                api_keys_file = Path(directory + "/api_keys")
            else:
                directory = str(Path.home()) + "/.config/oscar"
                api_keys_file = Path(directory + "/api_keys")
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(api_keys_file, 'wb') as updated_api_keys:
                pickle.dump(api_keys_dict, updated_api_keys)
            print(runtime.responses["api_key_has_been_added"].get_line())
            text_person(runtime)
        else:
            print(runtime.responses["cant_text_without_api_key"].get_line())
