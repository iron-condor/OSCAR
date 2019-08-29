"""Module that allows OSCAR to schedule a shutdown for a later time"""
import oscar_functions
import sys

def schedule_shutdown():
    """Schedules a shutdown to be performed after a given time period."""
    time = oscar_functions.schedule()
    if time != None:
        shell_command = None
        if sys.platform == "win32":
            shell_command = "shutdown -s -t " + str(time) + " -c Shutting down. Have a lovely rest of your day."
        elif sys.platform == "darwin":
            shell_command = "sleep " + str(time) + "osascript -e 'tell app \"System Events\" to shut down'"
        else:
            shell_command = "sleep " + str(time) + " && poweroff"
        oscar_functions.subprocess_cmd(shell_command)
        print(oscar_functions.get_response(12))
