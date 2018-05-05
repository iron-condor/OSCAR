# Developer: iron-condor
# Dependencies: duckduckgo-python3 (find on github), xdg-utils
import oscar_defaults
import oscar_functions
from pathlib import Path
import json
import os

#Loads the responses file if it exists. If it doesn't, one is automatically generated for the user.
def load_responses():
    responses_array = oscar_defaults.responses_array
    directory = str(Path.home()) + "/.config/oscar"
    if not os.path.exists(directory):
        os.makedirs(directory)
    responses_file = Path(str(Path.home()) + "/.config/oscar/responses")
    try:
        responses = open(responses_file, 'r')
    except FileNotFoundError:
        print("It doesn't seem like you have a responses config file generated. I'll do that quickly.")
        responses = open(responses_file, 'w')
        responses.write(json.dumps(responses_array, indent=4))
        print("...and done! You can find it here: " + str(responses_file))
    else:
        responses_array = json.load(responses)

#Loads the inputs file if it exists. If it doesn't, one is automatically generated for the user.
def load_inputs():
    inputs_array = oscar_defaults.inputs_array
    directory = str(Path.home()) + "/.config/oscar"
    if not os.path.exists(directory):
        os.makedirs(directory)
    inputs_file = Path(str(Path.home()) + "/.config/oscar/inputs")
    try:
        inputs = open(inputs_file, 'r')
    except FileNotFoundError:
        print("It doesn't seem like you have an input config file generated. I'll do that quickly.")
        inputs = open(inputs_file, 'w')
        inputs.write(json.dumps(inputs_array, indent=4))
        print("...and done! You can find it here: " + str(inputs_file))
    else:
        inputs_array = json.load(inputs)

load_responses()
load_inputs()
while (True):
    oscar_functions.receive_command()
