"""Allows OSCAR to say 'You're welcome!' """

def thanks(runtime):
    """Responds to the user thanking OSCAR

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    print(runtime.responses["youre_welcome"].get_line())
