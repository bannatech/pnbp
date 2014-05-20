#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'''
import mod
import json

pages = open("pages.json")

pagedata = json.load(pages)

pages.close()

def main():
    print("Going through pages...")

    site = {}

    for name,v in pagedata.items():
        template = open(v['template']).read()

        template = generateTemplate(template,v['pagevar'])

        print("page '{}' using template '{}'...".format(name,v['template']))

        site[name] = runMod(template,v['pagemod'])
        
    print site

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generateTemplate(t,var):
    for search,replace in var.items():
        t = t.replace("%"+search,replace)

    return t

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var):
    subpage = {}
    for name, mdata in var.items():
        subpage.update(getattr(mod,mdata['mod']).getPages(t,mdata['settings'],name))

    return subpage

if __name__ == "__main__":
    main()
    print("Finished.")
