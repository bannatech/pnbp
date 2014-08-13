# Functions file, used for inline scripts
import time


#Return the current date in the format sepecified in config
def now(config):
    return time.strftime(config)

#Return an HTML list. example format: {'root':"<ul class=\"special\">%li%</ul>",'li':"<li class=\"list\">%content%</li>"}
def list(things,formats={}):
    formats['root'] = formats.get("root","<ul>%li%</ul>")
    formats['li'] = formats.get("li","<li>%content%</li>")
    li = ""
    for thing in things:
        li = li + formats['li'].replace("%content%",thing)

    return formats['root'].replace("%li%",li)

