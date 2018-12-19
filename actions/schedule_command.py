import oscar_functions

#Schedules a command to be executed after a given time period.
def schedule_command():
    time = oscar_functions.schedule()
    if time != None:
        bash_command = None;
        if "\"" in oscar_functions.command:
            index1 = oscar_functions.command.find("\"") + 1
            index2 = oscar_functions.command.find("\"", index1 + 1, len(oscar_functions.command))
            bash_command = "sleep " + str(time) + " && " + oscar_functions.command[index1:index2]
            oscar_functions.subprocess_cmd(bash_command)

        else:
            bash_command = "sleep " + str(time) + " && " + input(oscar_functions.get_response(22))
            oscar_functions.subprocess_cmd(bash_command)
        print(oscar_functions.get_response(21))
