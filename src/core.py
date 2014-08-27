'''
'  pnbp - pnbp is not a blogging platform
'  core.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
#Core imports
import os, sys, json, yaml, re

#Helper imports
import module
from buildsite import *
from functions import *

#Global variables

pages = ""
pagedata = {}

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generateTemplate(t,var,page):
    if page == "index":
        page = ""

    t = t.replace("%page%",page)
    t = runInlineScript(t,page)
    
    for search,replace in var.items():
        if search[0] == ":":
            try:
                t.index("%"+search+"%")
                exists = True

            except:
                exists = False

            if exists:
                inc = file(replace).read()
                inc = generateTemplate(inc,var,page)
                print("Building include: '"+search+"'")
                t = t.replace("%"+search+"%",inc)

        else:
            t = t.replace("%"+search+"%",replace)

    return t

#Takes all code blocks in templates ("{:print("Hi"):}") and executes it, and replaces the block with the "returns" variable
def runInlineScript(template,page):
    for script in re.findall("{:(.*?):}",template, re.DOTALL):
        returns = ""
        exec(script)
        template = template.replace("{:"+script+":}",returns)
    
    return template

# Built-in module, generates page as subpage
def genPage(t,var,data,name,page):
    if 'settings' in data:
        try:
            if 'template' in data['settings']:
                template = file(data['settings']['template']).read()

        except:
            print("Error occured at {} using module page".format(page))
            print("Cannot open file {}".format(data['settings']['template']))
            sys.exit()

    else:
        template = t

    if 'pagevar' in var:
        if 'settings' in data:
            if 'pagevar' in data['settings']:
                var['pagevar'].update(data['settings']['pagevar'])

        template = generateTemplate(template,var['pagevar'],name)

    else:
        template = runInlineScript(template,name)
    
    if not 'settings' == data:
        t = {'default':template}

    else:
        if 'location' in meta:
            t = {data['settings']['location']:{'default':template}}

    return t

# Gets subpages from module specified in data
def getSubpages(t,var,data,name,page):
    returns = {}
    if not "settings" in data:
        data['settings'] = {}

    try:
        returns = getattr(module, data['mod']).getPages(t, data['settings'], name, page)

    except Exception,e:
        print("Error occured at {} using module {}:".format(page,data['mod']))
        if type(e) == KeyError:
            print("Missing attribute {}".format(e))
            sys.exit()

        else:
            print(e)
    
    return returns

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
    subpage = {}
    for name, meta in var['pagemod'].items():
        if meta['mod'] != "page":
            subpage.update(
                getSubpages(t,var,meta,name,page)
            )

        elif meta['mod'] == "page":
            subpage.update(
                genPage(t,var,meta,name,page)
            )

    return subpage

def build(bd):
    global pages, pagedata

    #Try to get the config
    try: pages = file("pages.yml")
    except:
        print("Can't open file 'pages.yml'")
        sys.exit()

    pagedata = yaml.load(pages)

    site = {}
    #Loops through defined "sites"
    for name,v in pagedata.items():
        #Read the template
        try: template = file(v['template']).read()
        except:
            print("{}: Can't open file '{}'".format(name,v['template']))
            sys.exit()
        
        #Check if pagevar is defined, skip the variable replacement step
        if 'pagevar' in v:
            template = generateTemplate(template,v['pagevar'],name)

        else:
            template = runInlineScript(template,name)
        
        print("Running modules for page: '"+name+"'")
        site[name] = runMod(template,v,name)
        print("Built page: '"+ name +"'\n")

    buildSite(site,bd)
