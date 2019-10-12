"""Module that provides code for launching programs that OSCAR knows about"""
import re
import oscar_functions

def launch_program(runtime):
    """Code that allows OSCAR to launch a program he has been told about"""
    runtime.command = runtime.command.lower()
    confirmed_aliases = []
    alias_paths = []
    #Searches the "command" for aliases, and adds their info to the above lists
    for alias_group in [p.aliases for p in runtime.programs]:
        for alias in alias_group:
            alias = "\\b" + alias + "\\b"
            if re.search(alias, runtime.command):
                contains_alias = False
                for path in alias_paths:
                    if path == [p.executable_path for p in runtime.programs][[p.aliases for p in runtime.programs].index(alias_group)]:
                        contains_alias = True
                if not contains_alias:
                    #Add the alias to the list
                    confirmed_aliases.append(alias)
                    #Add its file path to the list
                    alias_paths.append([p.executable_path for p in runtime.programs][[p.aliases for p in runtime.programs].index(alias_group)])
    for path in alias_paths:
        oscar_functions.subprocess_cmd(path)
    if (len(confirmed_aliases) > 1):
        print(runtime.responses["launching_programs"].get_line())
    elif (len(confirmed_aliases) > 0):
        print(runtime.responses["launching_program"].get_line())
    else:
        print(runtime.responses["couldnt_find_program_requested"].get_line())
