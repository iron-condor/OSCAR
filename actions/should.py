import oscar_functions
from random import randint

#Tells the user if someone should or should not perform an action.
#It offers 2 variants
#   - "Or" mode: Tells the user if they should perform one action, "or" another
#   - "Yes/no" mode: Responds as to whether the user should or should not do one particular action.
def should():
    #If we're in yes/no mode
    if " or " not in oscar_functions.command.lower():
        if randint(0, 1):
            print(oscar_functions.get_response(17))
        else:
            print(oscar_functions.get_response(18))
    elif " or " in oscar_functions.command:
        #Cut out the "should i" part of the string
        should_index = oscar_functions.command.find("should ")
        #The string "should " is 7 characters
        should_index += 7
        end_of_next_word = oscar_functions.command.find(" ", should_index)
        string = oscar_functions.command[end_of_next_word + 1:]
        if string.endswith("?"):
            string = string[:-1]
        options = string.split(" or ")
        randIndex = randint(0, len(options) - 1)
        option = options[randIndex]
        print(oscar_functions.get_response(14, "<option>", option))
