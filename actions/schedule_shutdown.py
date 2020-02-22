"""Module that allows OSCAR to schedule a shutdown for a later time"""
import sys
import oscar_functions

def schedule_shutdown(runtime):
    """Schedules a shutdown to be performed after a given time period.

    Arguments
    ---------
    runtime : Runtime
        The current Oscar runtime (defined in oscar_functions.py)
    """
    time = runtime.schedule()
    if time != None:
        shell_command = None
        if sys.platform == "win32":
            shell_command = "shutdown -s -t " + str(time) + " -c Shutting down. Have a lovely rest of your day."
        elif sys.platform == "darwin":
            shell_command = "sleep " + str(time) + "osascript -e 'tell app \"System Events\" to shut down'"
        else:
            shell_command = "sleep " + str(time) + " && poweroff"
        oscar_functions.subprocess_cmd(shell_command)
        print(runtime.responses["shutdown_scheduled"].get_line())
