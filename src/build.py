#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  build.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
#Core imports
import os, sys, shutil, json, yaml, time, traceback

#Helper imports
import module
from buildsite import *
from functions import *
from initbasic import *

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
    for name, mdata in var['pagemod'].items():
        if mdata['mod'] != "page":
            try:
                #Runs module specified in settings
                subpage.update(getattr(module,mdata['mod']).getPages(t,mdata['settings'],name,page))

            except Exception,e:
                print("Error occured at {} using module {}:".format(page,mdata['mod']))
                if type(e) == KeyError:
                    print("Missing attribute {}".format(e))
                    sys.exit()

                else:
                    print(e)

        elif mdata['mod'] == "page":
            #Built-in module page, takes configuration settings and builds a page at a location
            if 'settings' in mdata:
                try:
                    if 'template' in mdata['settings']:
                        template = file(mdata['settings']['template']).read()

                except:
                    print("Error occured at {} using module page".format(page))
                    print("Cannot open file {}".format(mdata['settings']['template']))
                    sys.exit()
            else:
                template = t

            if 'pagevar' in var:
                pv = var['pagevar']
                if 'settings' in mdata:
                    if 'pagevar' in mdata['settings']:
                        pv.update(mdata['settings']['pagevar'])

                template = generateTemplate(template,pv,name)

            else:
                template = runInlineScript(template,name)
            
            if not 'settings' == mdata:
                t = {'default':template}

            else:
                if 'location' in mdata:
                    t = {mdata['settings']['location']:{'default':template}}

            subpage.update(t)

    return subpage

def build(bd):
    site = {}
    
    #Loops through defined "sites"
    for name,v in pagedata.items():
        try:
            template = file(v['template']).read()

        except:
            print("{}: Can't open file '{}'".format(name,v['template']))
            sys.exit()

        if 'pagevar' in v:
            template = generateTemplate(template,v['pagevar'],name)
        else:
            template = runInlineScript(template,name)

        site[name] = runMod(template,v,name)

    buildSite(site,bd)

if __name__ == "__main__":
    buildDir = "site/"
    init = False

    if len(sys.argv) > 1:
        for i in sys.argv:
            if i[0] != "-" and i != sys.argv[0]:
                buildDir = i

            elif i == "--init" or i == "-i":
                init = True

            elif i == "-d":
                os.chdir(sys.argv.pop(sys.argv.index(i)+1))

            elif i == "--help":
                print("Usage: build [OPTION(s)]... [DIR]...\n"
                      "Build site in DIR using configuration in pwd\n"
                      "\n"
                      "  -d DIR      Use configuration in DIR, when not specified DIR is 'site/'\n"
                      "  -i, --init  Make a new site using the bare minimium config and build it in DIR\n"
                      "      --help  Display this help and exit\n"
                      "\n")

                sys.exit()

            elif i != sys.argv[0]:
                print("Unknown option: {}".format(i))

    if init:
        init()

    print("Going through pages...")
    start = time.time()
    try:
        pages = open("pages.yml")

    except:
        print("Can't open file 'pages.yml'")
        sys.exit()

    pagedata = yaml.load(pages)
    pages.close()

    try: build(buildDir)
    except Exception,e:
        if type(e) == KeyError:
            print("Missing or mistyped value: {}".format(e))

        else:
            print("Something went wrong...")
            print(e)
        
        traceback.print_exc(file=sys.stdout)
        sys.exit()

    print("Finished in {} ms.".format((time.time()-start)*1000))
