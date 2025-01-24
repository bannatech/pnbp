'''
'  pnbp - pnbp is not a blogging platform
'  env.py - maintain the scripting environment for templates
'  Paul Longtine -Paul Longtine <paul@banna.tech>
'''

import time
import json
import core.conf


class Tools:
    def __init__(self):
        self.conf = None

    # Return the current date in the format sepecified in config
    def now(self, config):
        return time.strftime(config)

    # Return an HTML list. example format:
    # {'root':"<ul class=\"special\">%li%</ul>",'li':"<li class=\"list\">%content%</li>"}
    def list(self, things, formats={}):
        formats['root'] = formats.get("root", "<ul>%li%</ul>")
        formats['li'] = formats.get("li", "<li>%content%</li>")
        li = ""
        for thing in things:
            li += formats['li'].replace("%content%", thing)

        return formats['root'].replace("%li%", li)

    # slug(string -> "hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
    def slug(self, string):
        invalidChars = [
            "<", ">", "#", "%", "{", "}",
            "|", "\\", "^", "[", "]", "`",
            "'", ";", "/", "?", ":", "@",
            "&", "+", ", ", "."
            ]
        for x in invalidChars:
            string = string.replace(x, "")

        string = string.replace(" ", "_")
        return string.lower()

    # Returns config
    def getConf(self):
        if self.conf is None:
            self.conf = core.conf.base().load()
        return self.conf

    def json_load(self, file):
        return json.load(file)


env = {"tools": Tools(), "page": "", "returns": ""}


def run(script, pageName):
    env["page"] = pageName
    exec(script, env)
    return str(env["returns"])
