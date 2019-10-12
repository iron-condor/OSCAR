"""Allows OSCAR to say 'You're welcome!' """

def thanks(runtime):
    """Responds to the user thanking OSCAR"""
    print(runtime.responses["youre_welcome"].get_line())
