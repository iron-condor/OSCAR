"""Module that OSCAR uses to schedule a command for a later time"""
import oscar_functions

#Schedules a command to be executed after a given time period.
def schedule_command(runtime):
    """Allows OSCAR to schedule a command to be executed later"""
    time = runtime.schedule()
    if time is not None:
        bash_command = None
        if "\"" in runtime.command:
            index1 = runtime.command.find("\"") + 1
            index2 = runtime.command.find("\"", index1 + 1, len(runtime.command))
            bash_command = "sleep " + str(time) + " && " + runtime.command[index1:index2]
            oscar_functions.subprocess_cmd(bash_command)

        else:
            bash_command = "sleep " + str(time) + " && " + input(runtime.responses["prompt_command_to_schedule"].get_line())
            oscar_functions.subprocess_cmd(bash_command)
        print(runtime.responses["command_scheduled"].get_line())
