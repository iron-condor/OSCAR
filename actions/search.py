"""Module that allows OSCAR to look up things, summarize them, and display links for source webpages"""
import duckduckgo, re

def search(runtime):
    """Searches and interprets a given string. Can extract summaries from some sites and services. Uses duckduckgo"""
    identifier_string = None
    for string in runtime.inputs[1][0]:
        if re.search(string, runtime.command):
            identifier_string = string
            break
    index = re.search(identifier_string, runtime.command).end()
    query = runtime.command[index:]
    if query.endswith("?"):
        query = query[:-1]
    if query != "":
        answer = duckduckgo.get_zci(query)
        duck_query = duckduckgo.query(query)
        if answer != "":
            print(answer + "\n")
            if duck_query.type != "nothing":
                confirm = input(runtime.get_response(4)).lower()
                if runtime.get_yes_no(confirm):
                    runtime.open_in_browser(duck_query.related[0].url)
                else:
                    print(runtime.get_response(19))
            elif answer.startswith("http"):
                if answer.startswith("https://www.youtu.be") or answer.startswith("https://www.youtube.com"):
                    confirm = input(runtime.get_response(31))
                else:
                    confirm = input(runtime.get_response(3)).lower()
                if runtime.get_yes_no(confirm):
                    runtime.open_in_browser(answer)
                else:
                    print(runtime.get_response(20))

        else:
            confirm = input(runtime.get_response(3)).lower()
            if runtime.get_yes_no(confirm):
                for c in query:
                    if c == ' ':
                        c = '+'
                runtime.open_in_browser("https://www.duckduckgo.com/?q=" + query)
            else:
                print(runtime.get_response(20))
    else:
        print(runtime.get_response(2))
