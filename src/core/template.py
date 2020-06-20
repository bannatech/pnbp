'''
'  pnbp - pnbp is not a blogging platform
'  template.py
'  Paul Longtine <paul@nanner.co>
'''

import re
import core.env


# Adds in variables defined in pages.json
#
def generate(rawTemplate, pagevar, pageName):
    if pageName == "index":
        page = ""

    t = rawTemplate.replace("%page%", pageName)
    t = run(t, pageName)

    for search, replace in pagevar.items():
        key = f"%{search}%"
        if search[0] == "$":
            try:
                t.index(key)
                exists = True

            except Exception:
                exists = False

            if exists:
                inc = open(replace).read()
                inc = generate(inc, pagevar, pageName)
                print(f"Building include: '{search}'")
                t = t.replace(key, inc)

        else:
            t = t.replace(key, replace)

    return t


# Finds all code blocks in templates (e.g. "{:print("Hi"):}") and executes it,
# replaces the block with the "returns" variable
def run(template, pageName):
    for script in re.findall("{:(.*?):}", template, re.DOTALL):
        returns = core.env.run(script, pageName)
        template = template.replace(f"{{:{script}:}}", returns)

    return template
