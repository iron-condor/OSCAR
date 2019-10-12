"""Contains a list of inputs and outputs that OSCAR recognizes, as well as application groups and settings.

    Responses
    ---------
    The responses list is a list of all responses OSCAR has to choose from.
    Generally speaking, there are five responses for each possible situation, although the number varies.
    The string may contain a token to be replaced in the string that the user sees, such as <user>.
    There is no fixed list of these, they may be any token that you wish. The only requirement is that
    you use the same token that you pass to Response.get_line()

    Inputs
    ------
    The inputs list is a list of regex strings that OSCAR recognizes as inputs for a given command.
    This system will be deprecated in later versions, and replaced with a machine learning driven
    classification algorithm. However, for the moment, the system relies on this input list.
    It is important to note that if you do not want the input to call a given function,
    you may simply omit the function.

    Settings
    --------
    A list of settings that the user can configure to customize OSCAR. As of the moment, it contains the following settings
    name : string
        The name that the user wishes to be addressed by
    clock type : int
        The clock type that the user wishes to use. 0 = 24 hour, 1 = 12 hour
    file location method : int
        The method that the user wants OSCAR to use to prompt them for file locations.
        0 = just let the user type it out, 1 = give them a file explorer window

    Groups
    ------
    A list that houses the programs that the user has told OSCAR about, and their respective aliases, as well as groups.

    "Groups" are sets of applications that OSCAR associates with particular phrases or words

        Structure
        ---------
        [
            This section houses a list of programs that the user has on their computer.
            [
                Aliases for the programs, The index corresponds to the index of the executable path.
                [
                    [<String>],
                    [<String>, <String>],
                    [<String>, <String>, <String>]
                ],
                The executable paths for the programs. The index corresponds to the index of the alias.
                [
                    <Path>, <Path>, <Path>
                ]
            ],
            This section maintains the list of groups that the user has created.
            [
                #Aliases for the groups. The index corresponds to the index of the executable path.
                [
                    [<String>, <String>],
                    [<String>, <String>, <String>],
                    [<String>]
                ],
                #The lists of aliases for the various applications in each group
                [
                    [<String>],
                    [<String>, <String>],
                    [<String>, <String>]
                ]
            ]
        ]
"""
import oscar_functions
import actions
from config_structures import *

#Responses
daytime_greetings = Response("daytime_greetings",
[
    "Hey there, <user>. How can I help you today?",
    "Nice to see you again, <user>. What can I do for you?",
    "Oscar here. I'm assuming that you're <user>, what can I help you with today?",
    "What's new, pussyca- err, I mean, <user>."
])

nighttime_greetings = Response("nighttime_greetings",
[
    "Nice to see you again, <user>. What can I do for you tonight?",
    "Back so quickly, <user>? Let's hear it.",
    "Burning the midnight oil again? What can I help you with?",
    "What's new, pussyca- err, I mean, <user>."
])

search_query_blank = Response("search_query_blank",
[
    "It's hard to look up something that doesn't exist.",
    "Look man, I'm just a computer program - I can't answer a question if you don't ask it.",
    "Garbage in, garbage out."
])

search_query_no_summary = Response("search_query_no_summary",
[
    "I'm having a bit of trouble making a summary on that. Care to have a look yourself?\n",
    "This is a bit too complicated for me to understand, maybe you'd like to see it?\n",
    "Maybe it's better that you look at this yourself. Want to?\n",
    "I can't find a summary for you, sorry, but I can open it in your browser if you'd like.\n"
])

offer_source = Response("offer_source",
[
    "That's an answer and a half if I dare say. Tell me if you want to read more on your own.\n",
    "That's all I've got. Want to see more for yourself?\n",
    "Want my sources?\n",
    "If you think that was too abstract of an abstract, I can open it for you so you can see yourself.\n"
])

disp_time = Response("disp_time",
[
    "It's currently <time>.",
    "Right now? It's <time>.",
    "Do I look like a clock to you? Don't answer that. It's <time>.",
    "It's <time>, and don't ask for me to make an analog clock.",
    "Here? It's <time>. In china? I have no idea. Unless we're in china. Actually, I have no idea where we're at."
])

youre_welcome = Response("youre_welcome",
[
    "You're welcome! I love to help.",
    "Of course. It's my job, after all.",
    "I'm programmed to help - I'm glad that I'm doing it well.",
    "Helpful? Me? Impossible.",
    "You're welcome! Although, if you really want to thank me, you can contribute to the github repos."
])

cant_open_url = Response("cant_open_url",
[
    "Weird, I can't open your browser. Here's the URL: <url>\n",
    "Huh, that's strange. I can't open your browser. Have a URL: <url>\n",
    "Well, this is awkward. Normally I'd open your browser now, but I can't for some reason or another. Enjoy your URL: <url>\n",
    "A URL a day keeps the doctor away, especially when your assistant isn't able to open your browser. URL: <url>\n",
    "You seem independent, have a URL. I can't open it, anyways. URL: <url>\n"
])

confirm_scheduled_time = Response("confirm_scheduled_time",
[
    "Alrighty then. I'll do that for you in <time_string>, yes?\n",
    "Just to clarify, you want that done in <time_string>?\n",
    "In <time_string>? Sure, my schedule's clear. That is the time, correct?\n",
    "I'd love to! I'll mark you down for <time_string> from now, then?\n",
    "Yeah, I can do that for you. You said <time_string> didn't you?\n"
])

scheduled_task_cancelled = Response("scheduled_task_cancelled",
[
    "Task cancelled.",
    "Okay. I'll mark that with a red X. Very large, very red, just for you.",
    "Operation aborted.",
    "You're really decisive, aren't you? Okay, okay, cancelling it...",
    "I'll forget you even asked."
])

confirm_yes_no = Response("confirm_yes_no",
[
    "Was that a yes or a no?\n",
    "I'm sorry, I didn't quite get that - is that a yes or an no?\n",
    "Imagine that I'm a slightly handsomer magic eight ball. Yes, or no?\n",
    "You'll have to excuse me, I'm not quite sure what you mean. Would you like me to schedule it, or cancel it?\n",
    "I may be digital, but I'm not omnipotent. Would you mind rephrasing your response?\n"
])

rephrase_scheduled_task = Response("rephrase_scheduled_task",
[
    "Sometimes the English language eludes me. This is one of those moments. Can you rephrase that?",
    "Can you rephrase that for me?",
    "I'm sorry, but I have no idea what you want me to do right now. Can you say that again?",
    "I didn't quite get that. English is my second language, after binary, of course.",
    "Would you rephrase that, please? I'm afraid I don't understand."
])

shutdown_scheduled = Response("shutdown_scheduled",
[
    "Powerdown imminent. Well, not imminent, really, but it's scheduled.",
    "I'll perform the shutdown when you asked.",
    "Shutdown scheduled.",
    "I'll turn your PC off at the aforementioned time.",
    "You're a busy person, so I'll make sure to shut it down for you when you asked."
])

shutdown_cancelled = Response("shutdown_cancelled",
[
    "Shutdown cancelled.",
    "Powerdown aborted.",
    "Changed your mind? I'll take it off the to-do list.",
    "Sounds like a pla - oh, changed your mind already? I'll cancel that, then.",
    "Okay, I'll forget that you ever asked me."
])

should_option = Response("should_option",
[
    "Clearly, <option> is the superior choice.",
    "I would go with <option>.",
    "You know what? Today, I'm feeling like <option>.",
    "You'd have to be a fool to not go with <option>.",
    "In situations like this, you should ask yourself: what would OSCAR do? Obviously, he would go with <option>.",
    "What kind of a question is that? Of course it's <option>!",
    "Normally, I wouldn't do it, but since you asked nicely, I'd go with <option>."
])

farewell = Response("farewell",
[
    "Have a lovely time.",
    "Leaving so soon? I was just getting warmed up.",
    "Alrighty then, I'll see you around.",
    "Until next time.",
    "You'll be back, we both know it."
])

ambiguous_request = Response("ambiguous_request",
[
    "I'm sorry, I have no idea what that means.",
    "Sometimes the English language eludes me. This is one of those moments. Can you rephrase that?",
    "Can you rephrase that for me?",
    "I'm sorry, but I have no idea what you want me to do right now. Can you say that again?",
    "I didn't quite get that. English is my second language, after binary, of course.",
    "Would you rephrase that, please? I'm afraid I don't understand."
])

you_should = Response("you_should",
[
    "That's a great idea! Do it.",
    "I don't see why not.",
    "What could go wrong?",
    "Yeah, sure, go for it.",
    "I wouldn't be against it."
])

you_shouldnt = Response("you_shouldnt",
[
    "That doesn't sound like a good idea to me.",
    "Are you sure? I'm not sure it's such a good idea.",
    "Personally, I wouldn't, but it's not my choice.",
    "That sounds dreadful, don't do it.",
    "Would you be angry if I said no? I'm saying no."
])

wont_open_summary_good = Response("wont_open_summary_good",
[
    "My summary was good enough? Excellent!",
    "That's okay, I'll just read it alone.",
    "Alrighty then. I'll keep the link to myself.",
    "You're a busy person. If a summary works, it works. If it doesn't, the link's still there.",
    "I'm glad that I was able to summarize it well for you."
])

wont_open_no_summary = Response("wont_open_no_summary",
[
    "I won't open it in your browser, then.",
    "If you change your mind, just ask again.",
    "The link's not going anywhere, in case you change your mind.",
    "That's fine. I'll leave it closed, in that case.",
    "Sounds good to me. If you change your mind, just ask again."
])

command_scheduled = Response("command_scheduled",
[
    "Command scheduled.",
    "I'll do that.",
    "I'll take care of it for you when the time arrives, don't worry.",
    "I can do that.",
    "Okay, I'll do that for you."
])

prompt_command_to_schedule = Response("prompt_command_to_schedule",
[
    "Okay. What do you want me to do at that time, exactly?",
    "Well, I've got the time down, but I'm not exactly sure of what you want me to do. Can you clarify?",
    "My schedule's clear for that time. What would you like me to do then?",
    "I don't have any plans for that time. What do you need me to do?",
    "Sure, that time works for me. What's your command?"
])

opening_link = Response("opening_link",
[
    "Let's open that in your browser, then.",
    "Opening link now...",
    "I'll open that link for you quickly.",
    "Your browser is asking for your attention - I believe it's the link you asked for.",
    "The page is opened in your browser, whenever you're ready for it."
])

whats_your_name = Response("whats_your_name",
[
    "What do you like to be called?\n",
    "What's your name, stranger?\n",
    "I'm Oscar, lovely to meet you. You would be..?\n",
    "A fresh face! What do I call you?\n",
    "I'm always terrible at introductions. Let's start with names - I'm Oscar, and you are?\n"
])

prompt_clock_type = Response("prompt_clock_type",
[
    "Next question: Your clock type. 24-hour or 12-hour?\n",
    "What type of clock do you prefer: 12-hour or 24-hour?\n",
    "<user>. Got it. So what kind of clock do you like, <user>? 24-hour or 12-hour?\n",
    "It's nice to meet you, <user>. Do you prefer the 24-hour or 12-hour clock?\n",
    "Okay <user>, do you prefer your times to be in 24-hour or 12-hour format?\n"
])

selected_24hour_clock = Response("selected_24hour_clock",
[
    "24-hour, huh? Finally, someone sensible.",
    "At last, someone rational. 24-hour clock it is.",
    "I'll serve your times in a 24-hour format, then.",
    "24-hour? sounds good to me.",
    "I'm glad you chose 24-hour. I don't think I'd see you in the same light if you had said 12."
])

selected_12hr_clock = Response("selected_12hr_clock",
[
    "12-hour? Weird, but okay.",
    "12-hour it is.",
    "Strange choice, but it's yours. 12-hour clock, then.",
    "Alright, I'll give you the time in the 12-hour format whenever you ask.",
    "12-hour? Aww. Come to the dark side - we have cookies, and twice the hours on our clock."
])

launching_programs = Response("launching_programs",
[
    "Opening them now...",
    "I'll get those up for you in a jiffy",
    "They'll be open in just a moment.",
    "Of course, I'll open those right away.",
    "Expect those programs to be open shortly"
])

launching_program = Response("launching_program",
[
    "I'll open it right now",
    "Give me just a second, aaaaand it's opening.",
    "It'll be up in just a second",
    "It's opening right now, just for you",
    "Program opened - or rather, it's opening."
])

couldnt_find_program_requested = Response("couldnt_find_program_requested",
[
    "I don't think you've told me about any programs by that name.",
    "I'm looking at my list, and I don't see any programs called that.",
    "Are you sure you spelled it right? You haven't told me about any programs named that.",
    "I may just be illiterate, but I don't see a program named that"
])

found_video = Response("found_video",
[
    "Hey! I found a video about that. Want me to play it for you?\n",
    "They say a picture's worth a thousand words. Personally, I think videos are worth more - care to see one?\n",
    "Youtube seems to have something appropriate - want me to put it on?\n",
    "Ooh! A video! Want me to open it?\n",
    "I've got a youtube video on the subject, just say the word and I'll open it\n"
])

prompt_configure_settings = Response("prompt_configure_settings",
[
    "Configure settings? Absolutely! Here are your settings. Which would you like to edit?\n",
    "Ooh! Changing settings, are we? Well, here they are - just say which setting you want to change.\n",
    "Here's a list of settings for you to play with. Call it by name, and I'll change it to whatever you like.\n",
    "I hope I didn't get one of your settings wrong. Here they are, let me know which one you need changed.\n",
    "If I got something wrong, I'm happy to fix it. Your settings are right below, which do you need changed?\n"
])

prompt_select_files_method = Response("prompt_select_files_method",
[
    "Sometimes, I might need to get the location of a file from you. When that comes up, would you like a file manager, or do you just want to type the path out yourself?\n",
    "Tell me - are you a fan of file managers, or do you prefer to type out paths yourself?\n",
    "In the event that I need a file from you, would you prefer to be given a file manager, or would you like to type it out manually?\n",
    "Do you prefer to be given a file manager, or would you rather type out file paths yourself?\n",
    "At some point, I may have to get a file path from you. Do you want a GUI file manager, or would you rather just type out the path yourself?\n"
])

disp_chosen_to_use_file_manager = Response("disp_chosen_to_use_file_manager",
[
    "Great! I'll give you a file manager when I need files from you, then.",
    "Awesome! I'll make sure you have something you can click on whenever you choose a file.",
    "File manager it is. You'll have one to use if I ever need a file from you.",
    "In that case, I'll give you a GUI to choose your files from, if it's necessary.",
    "Excellent, if I need a file from you, I'll ensure that you have a window to find it with."
])

disp_chosen_to_type_out_paths = Response("disp_chosen_to_type_out_paths",
[
    "File managers are for casuals anyways. I'll let you type out your own paths.",
    "If I need a file from you, I'll just let you type the path in yourself.",
    "No file manager? That makes it much easier for both of us.",
    "I'm glad you like typing out your own file paths - windows are scary, anyway.",
    "I'll remember that. If I ever need a file from you, rest assured that I'll let you type out the path."
])

disp_settings_have_updated = Response("disp_settings_have_updated",
[
    "Your settings have been updated. I wish I would be updated more often...",
    "Updating your settings... and done! Everything is how you asked.",
    "I've changed your settings how you asked - if you need to change or view them again later, just ask again",
    "Whoosh! Hear that? It's the sound of your settings being updated. Don't ask me why they make whooshing noises.",
    "Options optimized - just for you, just as you asked."
])

disp_settings_not_updated = Response("disp_settings_not_updated",
[
    "No changes? Wonderful, I'm glad that I got everything right last time.",
    "I wouldn't change anything, either - they're perfect as they are c:",
    "No changes it is! I'll just leave your settings be.",
    "I'm glad that you're satisfied with your settings - I won't touch them, then.",
    "If no changes are necessary, I'll just leave them be."
])

prompt_select_file_for_new_program = Response("prompt_select_file_for_new_program",
[
    "Adding a new program? Sweet! I could use some company. Where's the file at?",
    "Ooooh? A new program, huh? Point me to it.",
    "Point me to the app you want to add, and I'll register it.",
    "I love new applications! Where's it at?",
    "You want to add a new program? Okay, just point me to it."
])

disp_not_valid_file_path = Response("disp_not_valid_file_path",
[
    "That's strange, I can't seem to find a file at that location. Try again?",
    "This is odd... to me, it looks like there's no file at that path. Would you try again, please?",
    "There's doesn't seem to be a file there - are you sure it's there? Try it again, please.",
    "I'm looking as hard as I can, but I still can't find a file there. Can you try again?",
    "Filesystems, much like fate, work in mysterious ways - and right now I can't find that file. Try again, would you?"
])

prompt_for_aliases = Response("prompt_for_aliases",
[
    "I've got the file - now what do you want to call it?",
    "File acquired - what's its name?",
    "Aaaaand there it is! Exactly where you said it would be. What would you like to call this program?",
    "Hey! There it is! What's this program's name?",
    "I found the file you mentioned, now what would you like me to refer to it as?"
])

tutorial_enter_multiple_names = Response("tutorial_enter_multiple_names",
[
    "You can enter multiple names, just separate them by commas and a space.",
    "If you like, you can put more than one name - simply separate the names by commas and a space.",
    "If the file's got a nickname or two, you can also tell me about those - just separate them with commas and a space.",
    "If you want to call that program by more than one name, just list the others as well, separated by commas and a space.",
    "Some programs have more than one name - if you want me to remember another name for this program, just put it after the first, with a comma and a space."
])

program_has_been_added = Response("program_has_been_added",
[
    "Program added! It's a little less lonely here, now.",
    "Your program has been added",
    "Aaaand I've added your application.",
    "I'll remember that app, now, in case you want to reference it in the future.",
    "App added. I'll remember it now, if you need me to do anything with it."
])

program_already_registered = Response("program_already_registered",
[
    "Looks like you've already registered that program. No need to register it again",
    "It seems like you've already told me about that program - you don't need to tell me about it again",
    "I can remember this app from before - I still remember it, don't worry.",
    "I've already got this app registered - no need to re-register it",
    "My memory isn't that bad - I still remember where this program is from last time, so don't worry."
])

all_aliases_in_use = Response("all_aliases_in_use",
[
    "All of the names you gave me are already in use - can you give me some other names, instead?\n",
    "I'm afraid I can't use names that are already being used. What's another name you can call that program?\n",
    "Those names are taken, I'm afraid. What other names do you have?\n",
    "Looks like there are programs called that already - what else can you call this one?\n",
    "Strange, there's an application that's already called that. Is there anything else you can call it?\n"
])

stopwatch_started = Response("stopwatch_started",
[
    "Aaand, the clock has started! Press enter when you're ready to stop.",
    "Ready, set... go! Oh, and by the way - when you're ready to stop timing, press enter.",
    "Okay, I'm timing. Press enter when you're finished",
    "Stopwatch started. Press enter to stop timing.",
    "Let the stopwatch begin! You can press enter if you want the stopwatch to stop."
])

disp_time_passed = Response("disp_time_passed",
[
    "Done! Here's your time: <time_string>",
    "Time: <time_string>",
    "That took <time_string>",
    "Final time: <time_string>",
    "Finished. <time_string>"
])

responses_dict = {
    "daytime_greetings" : daytime_greetings,
    "nighttime_greetings" : nighttime_greetings,
    "search_query_blank" : search_query_blank,
    "search_query_no_summary" : search_query_no_summary,
    "offer_source" : offer_source,
    "disp_time" : disp_time,
    "youre_welcome" : youre_welcome,
    "cant_open_url" : cant_open_url,
    "confirm_scheduled_time" : confirm_scheduled_time,
    "scheduled_task_cancelled" : scheduled_task_cancelled,
    "confirm_yes_no" : confirm_yes_no,
    "rephrase_scheduled_task" : rephrase_scheduled_task,
    "shutdown_scheduled" : shutdown_scheduled,
    "shutdown_cancelled" : shutdown_cancelled,
    "should_option" : should_option,
    "farewell" : farewell,
    "ambiguous_request" : ambiguous_request,
    "you_should" : you_shouldnt,
    "you_shouldnt" : you_shouldnt,
    "wont_open_summary_good" : wont_open_summary_good,
    "wont_open_no_summary" : wont_open_no_summary,
    "command_scheduled" : command_scheduled,
    "prompt_command_to_schedule" : prompt_command_to_schedule,
    "opening_link" : opening_link,
    "whats_your_name" : whats_your_name,
    "prompt_clock_type" : prompt_clock_type,
    "selected_24hour_clock" : selected_24hour_clock,
    "selected_12hr_clock" : selected_12hr_clock,
    "launching_programs" : launching_programs,
    "launching_program" : launching_program,
    "couldnt_find_program_requested" : couldnt_find_program_requested,
    "found_video" : found_video,
    "prompt_configure_settings" : prompt_configure_settings,
    "prompt_select_files_method" : prompt_select_files_method,
    "disp_chosen_to_use_file_manager" : disp_chosen_to_use_file_manager,
    "disp_chosen_to_type_out_paths" : disp_chosen_to_type_out_paths,
    "disp_settings_have_updated" : disp_settings_have_updated,
    "disp_settings_not_updated" : disp_settings_not_updated,
    "prompt_select_file_for_new_program" : prompt_select_file_for_new_program,
    "disp_not_valid_file_path" : disp_not_valid_file_path,
    "prompt_for_aliases" : prompt_for_aliases,
    "tutorial_enter_multiple_names" : tutorial_enter_multiple_names,
    "program_has_been_added" : program_has_been_added,
    "program_already_registered" : program_already_registered,
    "all_aliases_in_use" : all_aliases_in_use,
    "stopwatch_started" : stopwatch_started,
    "disp_time_passed" : disp_time_passed
}

#Inputs
time_date_command = Input(
    "time_date_command",
    positive_matches = [
        "\\bwhat time is it\\b",
        "\\bwhat is the time\\b",
        "\\bhow much is the clock\\b",
        "\\bwhat day is it\\b",
        "\\bwhat is the day\\b",
        "\\bhwhat date is it\\b",
        "\\bwhat is the date\\b",
        "\\bday\\b",
        "\\bdate\\b"
    ],
    negative_matches = [
        "\\blook up\\b",
        "\\bsearch\\b",
        "\\blooking up\\b",
        "\\bsearching up\\b",
        "\\btell me about",
        "\\bwho is\\b",
        "\\bwho's\\b",
        "\\bdefine\\b",
        "\\bwhat are\\b",
        "\\bwhat was\\b",
        "\\bwhat were\\b",
        "\\bwho was\\b",
        "\\bwho were\\b",
        "\\bjokes?\\b"
    ],
    function = actions.give_time
)

search_command = Input(
    "search_command",
    positive_matches = [
        "\\bsearch\\b",
        "\\blook up\\b",
        "\\blooking up\\b",
        "\\bsearching up\\b",
        "\\btell me\\b",
        "\\btell me the\\b",
        "\\btell me everything about\\b",
        "\\btell me everything you know about\\b",
        "\\btell me about\\b",
        "\\bwhat is\\b",
        "\\bwhat's\\b",
        "\\bwhat the fuck is\\b",
        "\\bwhat the hell is\\b",
        "\\bwhats\\b",
        "\\bwho is\\b",
        "\\bwho's\\b",
        "\\bdefine\\b",
        "\\bwhat are\\b",
        "\\bwhat was\\b",
        "\\bwhat were\\b",
        "\\bwho was\\b",
        "\\bwho were\\b",
        "\\bwhat do you know about\\b",
        "\\bshow me\\b"
    ],
    negative_matches = [
        "\\bjokes?\\b"
    ],
    function = actions.search
)

should_command =  Input(
    "should_command",
    positive_matches = [
        "\\bshould\\b"
    ],
    function = actions.should
)

launch_program_command = Input(
    "launch_program_command",
    positive_matches = [
        "\\blaunch\\b",
        "\\bstart\\b",
        "\\bstarting\\b",
        "\\bopen\\b"
    ],
    function =  actions.launch_program
)

thank_you_command = Input(
    "thank_you_command",
    positive_matches = [
        "\\bthanks\\b",
        "\\bthank you\\b",
        "\\bappreciate\\b",
        "\\bgrateful\\b",
        "\\bglad\\b",
        "\\bty\\b"
    ],
    function = actions.thanks
)

schedule_shutdown_command = Input(
    "schedule_shutdown_command",
    positive_matches = [
        "\\bshut ?down\\b",
        "\\bpower ?off\\b",
        "\\bpower ?down\\b",
        "\\bturn off\\b"
    ],
    function = actions.schedule_shutdown
)

schedule_command_command =  Input(
    "schedule_command_command",
    positive_matches = [
        "\\bschedule\\b",
        "\\bseco?n?d?s?\\b",
        "\\bminu?t?e?s?\\b",
        "\\bhours?\\b",
        "\\bdays?\\b"
    ],
    function = actions.schedule_command
)

close_command = Input(
    "close_command",
    positive_matches = [
        "\\bexit\\b",
        "\\bfuck off\\b",
        "\\b:q\\b",
        "\\bquit\\b",
        "\\bclose\\b",
        "\\bbye\\b",
        "\\btalk to you later\\b",
        "\\blater\\b",
        "\\bsee you later\\b",
        "\\bcya\\b",
        "\\bsee you\\b",
        ":q"
    ],
    negative_matches = [
        "\\bdon't\\b",
        "\\bdo not\\b",
        "\\bno\\b",
        "\\bnevermind\\b"
    ],
    function = oscar_functions.close_oscar
)

input_is_no = Input(
    "input_is_no",
    positive_matches = [
        "\\bno\\b",
        "\\bnah\\b",
        "\\bnevermind\\b",
        "\\bnope\\b",
        "\\bforget about it\\b",
        "\\bforget it\\b",
        "\\bchanged my mind\\b",
        "\\bnegative\\b",
        "\\bnegatory \\b",
        "\\bcancel\\b"
    ]
)

input_is_yes = Input(
    "input_is_yes",
    positive_matches = [
        "\\byes\\b",
        "\\bof course\\b",
        "\\bplease\\b",
        "\\bnaturally\\b",
        "\\blove\\b",
        "\\byeah\\b",
        "\\byep\\b",
        "\\byea\\b",
        "\\bi do\\b",
        "\\bsure\\b",
        "\\balright\\b",
        "\\bokay\\b",
        "\\bsummary\\b",
        "\\bok\\b",
        "\\bmhm\\b",
        "\\bgo ahead\\b"
    ],
    negative_matches = [
        "\\bno\\b",
        "\\bnot\\b",
        "\\bdon't\\b",
        "\\bdo not\\b",
        "\\bnevermind\\b"
    ]
)

walkthrough_input = Input(
    "walkthrough_input",
    positive_matches = [
        "\\bhelp\\b",
        "\\bhelpful\\b",
        "\\byes\\b",
        "\\bof course\\b",
        "\\bplease\\b",
        "\\bnaturally\\b",
        "\\blove\\b",
        "\\byeah\\b",
        "\\byep\\b",
        "\\byea\\b",
        "\\bi do\\b",
        "\\bsure\\b",
        "\\balright\\b",
        "\\bokay\\b",
        "\\bok\\b",
        "\\bwalkthrough\\b",
        "\\bwalk me through\\b",
        "\\bwalk through\\b"
    ],
    negative_matches = [
        "\\bno\\b",
        "\\bnot\\b",
        "\\bdon't\\b",
        "\\bdo not\\b"
    ]
)

default_settings_input = Input(
    "default_settings_input",
    positive_matches = [
        "\\bdefaults\\b",
        "\\bthanks anyways\\b",
        "\\bno thanks\\b"
    ]
)

twenty_four_hour_clock_input = Input(
    "twenty_four_hour_clock_input",
    positive_matches = [
        "\\b24-hour\\b",
        "\\b24 hour\\b",
        "\\b24hour\\b",
        "\\b24\\b",
        "\\btwenty four\\b"
    ]
)

twelve_hour_clock_input = Input(
    "twelve_hour_clock_input",
    positive_matches = [
        "\\b12-hour\\b",
        "\\b12 hour\\b",
        "\\b12hour\\b",
        "\\b12\\b",
        "\\btwelve\\b"
    ]
)

name_input = Input(
    "name_input",
    positive_matches = [
        "\\byou can call me\\b",
        "\\bmy name is\\b",
        "\\bsome people call me\\b",
        "\\bsome call me\\b",
        "\\bthe name's\\b",
        "\\bthe name is\\b",
        "\\bcall me\\b",
        "\\bi go by\\b",
        "\\bbe called\\b"
    ]
)

joke_input = Input(
    "joke_input",
    positive_matches = [
        "\\bjoke\\b",
        "\\bjokes\\b",
        "\\blaugh\\b"
    ],
    function = actions.tell_joke
)

file_manager_input = Input(
    "file_manager_input",
    positive_matches = [
        "\\bfile manager\\b",
        "\\bmanager\\b",
        "\\bgui\\b",
        "\\bwindow\\b"
    ],
    negative_matches = [
        "\\bdon't need\\b",
        "\\bdon't want\\b"
    ]
)

type_out_paths_input = Input(
    "type_out_paths_input",
    positive_matches = [
        "\\btype\\b",
        "\\btyped\\b",
        "\\btyping\\b",
        "\\bon my own\\b",
        "\\bmyself\\b"
    ]
)

reconfigure_settings_input = Input(
    "reconfigure_settings_input",
    positive_matches = [
        "\\bconfigure\\b",
        "\\bconfiguring\\b",
        "\\bconfigured\\b",
        "\\breconfigure\\b",
        "\\breconfiguring\\b",
        "\\breconfigured",
        "\\bsettings\\b",
        "\\badjust\\b",
        "\\badjusting\\b",
        "\\badjusted\\b",
        "\\boptions\\b"
    ],
    function = actions.configure_settings
)

add_new_program_input = Input(
    "add_new_program_input",
    positive_matches = [
        "\\badd an application\\b",
        "\\badd a program\\b",
        "\\badd an app\\b",
        "\\badd a new application\\b",
        "\\badd a new program\\b",
        "\\badd a new app\\b",
        "\\badding a new application\\b",
        "\\badding a new program\\b",
        "\\badding a new app\\b",
        "\\btell you about an application\\b",
        "\\btell you about a program\\b",
        "\\btell you about an app\\b",
        "\\btell you about a new application\\b",
        "\\btell you about a new program\\b",
        "\\btell you about a new app\\b",
        "\\bregister an application\\b",
        "\\bregister a program\\b",
        "\\bregister an app\\b",
        "\\bregister a new application\\b",
        "\\bregister a new program\\b",
        "\\bregister a new app\\b",
        "\\bregistering an application\\b",
        "\\bregistering a program\\b",
        "\\bregistering an app\\b",
        "\\bregistering a new application\\b",
        "\\bregistering a new program\\b",
        "\\bregistering a new app\\b"
    ],
    function = actions.add_program
)

stopwatch_command =  Input(
    "stopwatch_command",
    positive_matches = [
        "\\bstopwatch\\b",
        "\\bstart timing\\b",
        "\\btime me\\b",
        "\\btime this\\b",
        "\\btime something\\b"
    ],
    function = actions.stopwatch
)

inputs_dict = {
    "time_date_command" : time_date_command,
    "search_command" : search_command,
    "should_command" : should_command,
    "launch_program_command" : launch_program_command,
    "thank_you_command" : thank_you_command,
    "schedule_shutdown_command" : schedule_shutdown_command,
    "schedule_command_command" : schedule_command_command,
    "close_command" : close_command,
    "input_is_no" : input_is_no,
    "input_is_yes" : input_is_yes,
    "walkthrough_input" : walkthrough_input,
    "default_settings_input" : default_settings_input,
    "twenty_four_hour_clock_input" : twenty_four_hour_clock_input,
    "twelve_hour_clock_input" : twelve_hour_clock_input,
    "name_input" : name_input,
    "joke_input" : joke_input,
    "file_manager_input" : file_manager_input,
    "type_out_paths_input" : type_out_paths_input,
    "reconfigure_settings_input" : reconfigure_settings_input,
    "add_new_program_input" : add_new_program_input,
    "stopwatch_command" : stopwatch_command
}

#The settings dictionary is responsible for managing the user's various settings and preferences.
settings_dict = {
    #The name that the user wishes to be called
    "name" : Setting("name", "nameless"),
    #24-hour or 12-hour clock. True = twelve-hour, False = 24-hour
    "use_12_hour_clock" : Setting("use_12_hour_clock", True),
    #Let the user type out paths to files, or give them a file manager. True = File manager, False = Type it out
    "use_file_manager" : Setting("use_file_manager", True)
}

#This houses a list of programs that the user has on their computer.
#It contains objects of type Program, as defined in config_structures.py
programs_array = []

#Houses a list of program groups that the user has told Oscar to group together
#"Groups" are sets of applications that OSCAR associates with particular phrases or words
groups_array = []
