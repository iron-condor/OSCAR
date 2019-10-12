"""Module that contains structures to be imported from config files"""
from random import randint

class Response:
    """Class that represents Oscar's responses to a certain event"""
    def __init__(self, name, lines):
        """Constructor for the Response object

        Arguments
        ---------
        name : string
            A unique name used to identify the response
        lines : list[string]
            A list of response lines, from which OSCAR can choose
        """
        self.name = name
        self.lines = lines

    def get_line(self, delimiter=None, replacement=None) -> "string":
        """Randomly fetches an appropriate response from the list of responses.

        Arguments
        ---------
        delimiter (optional) : string
            A string to be replaced with replacement. For example, "<user>"
        replacement (optional) : string
            A string that replaces the delimiter. For example, "foo"

        Returns
        -------
        String
            Returns a random string from the response set, with any delimiters replaced
        """
        if delimiter is None or replacement is None:
            return self.lines[randint(0, len(self.lines) - 1)]
        else:
            return self.get_line().replace(delimiter, replacement)

class Input:
    """Class that represents Oscar's inputs that correlate to a certain function or idea"""
    def __init__(self, name, positive_matches=[], negative_matches=[], function=None, parameters={}):
        """Constructor for the Input object

        Arguments
        ---------
        name : string
            A unique name used to identify the Input
        positive_matches : list[string]
            A list of RegEx strings that, if found in the user's input, mark it as a positive match for this
            Input class.
        negative_matches : list[string]
            A list of RegEx strings that, if found in the user's input, mark it as a false positive for this
            Input class.
        function : function/method
            A function to be called if this Input is found as a match
        parameters : dictionary
            A dictionary of parameters to be provided to the function, in the event that it is to be called.
        """
        self.name = name
        self.positive_matches = positive_matches
        self.negative_matches = negative_matches
        self.function = function
        self.parameters = parameters

class Setting:
    """Class that represents a setting/preference for the user"""
    def __init__(self, name, state):
        """Constructor for the Setting object

        Arguments
        ---------
        name : string,
            A unique name used to identify the Setting
        state : *
            The state of the setting.
            Ex: If the setting is the user's name, state is a string representing the user's name
            Ex: If the setting represents whether or not the user prefers the 12-hour clock,
            the state is a boolean
        """
        self.name = name
        self.state = state

class Program:
    """Class that represents a Program that OSCAR can launch"""
    def __init__(self, aliases, executable_path):
        """Constructor for the Program class

        Arguments
        ---------
        aliases : list[string]
            A list of strings that represent the program.
            Ex: ["firefox", "ff", "browser"]
        executable_path : string
            A string that points to the absolute filepath of the program's executable
            Ex: "/usr/bin/firefox"
        """
        self.aliases = aliases
        self.executable_path = executable_path

class Program_Group:
    """Class that represents a group of programs that OSCAR can launch"""
    def __init__(self, aliases, program_aliases):
        """Constructor for the Program_Group object

        Arguments
        ---------
        aliases : list[string]
            A list of strings that represent the group
            Ex: ["chill", "relax"]
        program_aliases: list[string]
            A list of aliases that match the programs in the group.
            There should only be one alias provided per progrma.
            Ex: ["music player", "reddit"]
        """
        self.aliases = aliases
        self.program_aliases = program_aliases
