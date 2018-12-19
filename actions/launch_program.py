import oscar_functions
import re

def launch_program():
    oscar_functions.command = oscar_functions.command.lower()
    confirmed_aliases = []
    alias_paths = []
    #Searches the "command" for aliases, and adds their info to the above lists
    for alias_group in oscar_functions.groups[0][0]:
        for alias in alias_group:
            alias = "\\b" + alias + "\\b"
            if re.search(alias, oscar_functions.command):
                contains_alias = False
                for path in alias_paths:
                    if path == oscar_functions.groups[0][1][oscar_functions.groups[0][0].index(alias_group)]:
                        contains_alias = True
                if not contains_alias:
                    #Add the alias to the list
                    confirmed_aliases.append(alias)
                    #Add its file path to the list
                    alias_paths.append(oscar_functions.groups[0][1][oscar_functions.groups[0][0].index(alias_group)])
    for path in alias_paths:
        oscar_functions.subprocess_cmd(path)
    if (len(confirmed_aliases) > 1):
        print(oscar_functions.get_response(28))
    elif (len(confirmed_aliases) > 0):
        print(oscar_functions.get_response(29))
    else:
        print(oscar_functions.get_response(30))
