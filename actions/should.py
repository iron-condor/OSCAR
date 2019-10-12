"""Module that allows OSCAR to randomly decide something for the user"""
from random import randint

def should(runtime):
    """Tells the user if someone should or should not perform an action.

    Variations
    ----------
    "Or" mode:
        Tells the user if they should perform one action, "or" another
    "Yes/no" mode:
        Responds as to whether the user should or should not do one particular action.
    """
    #If we're in yes/no mode
    if " or " not in runtime.command.lower():
        if randint(0, 1):
            print(runtime.responses["you_should"].get_line())
        else:
            print(runtime.responses["you_shouldnt"].get_line())
    elif " or " in runtime.command:
        #Cut out the "should i" part of the string
        should_index = runtime.command.find("should ")
        #The string "should " is 7 characters
        should_index += 7
        end_of_next_word = runtime.command.find(" ", should_index)
        string = runtime.command[end_of_next_word + 1:]
        if string.endswith("?"):
            string = string[:-1]
        options = string.split(" or ")
        rand_index = randint(0, len(options) - 1)
        option = options[rand_index]
        print(runtime.responses["should_option"].get_line("<option>", option))
