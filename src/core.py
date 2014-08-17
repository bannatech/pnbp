'''
'  pnbp - pnbp is not a blogging platform
'  core.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
#Core imports
import os, sys, json, yaml

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
                t = t.replace("%"+search+"%",inc)

        else:
            t = t.replace("%"+search+"%",replace)

    return t

#Takes all code blocks in templates ("{:print("Hi"):}") and executes it, and replaces the block with the "returns" variable
def runInlineScript(template,page):
    exists = True
    while exists:
        try:
            index = template.index("{:")+2
            findex = index
            exists = True
            
        except:
            exists = False

        if exists:
            script = ""
            while template[index:index+2] != ":}":
                script = script + template[index]
                index += 1

            returns = ""
            exec(script)
            template = template.replace(template[findex-2:index+2],returns)
    
    return template

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
    subpage = {}
    for name, meta in var['pagemod'].items():
        if meta['mod'] != "page":
            if not "settings" in meta: meta['settings'] = {}
            try:
                #Runs module specified in settings
                subpage.update(
                    getattr(module, meta['mod']).getPages(
                        t, meta['settings'], name, page
                    )
                )

            except Exception,e:
                print("Error occured at {} using module {}:".format(page,meta['mod']))
                if type(e) == KeyError:
                    print("Missing attribute {}".format(e))
                    sys.exit()

                else:
                    print(e)

        elif meta['mod'] == "page":
            #Built-in module page, takes configuration settings and builds a page at a location
            if 'settings' in meta:
                try:
                    if 'template' in meta['settings']: template = file(meta['settings']['template']).read()

                except:
                    print("Error occured at {} using module page".format(page))
                    print("Cannot open file {}".format(meta['settings']['template']))
                    sys.exit()
            else:
                template = t

            if 'pagevar' in var:
                if 'settings' in meta:
                    if 'pagevar' in meta['settings']:
                        var['pagevar'].update(meta['settings']['pagevar'])

                template = generateTemplate(template,var['pagevar'],name)

            else:
                template = runInlineScript(template,name)
            
            if not 'settings' == meta:
                t = {'default':template}

            else:
                if 'location' in meta: t = {meta['settings']['location']:{'default':template}}

            subpage.update(t)

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

        site[name] = runMod(template,v,name)

    buildSite(site,bd)
