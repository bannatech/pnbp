#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'''
import os, shutil, mod, json

def main():
    print("Going through pages...")

    site = {}

    for name,v in pagedata.items():
        template = open(v['template']).read()

        template = generateTemplate(template,v['pagevar'])

        print("page '{}' using template '{}'...".format(name,v['template']))

        site[name] = runMod(template,v['pagemod'])
    
    buildSite(site)

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generateTemplate(t,var):
    for search,replace in var.items():
        if search[0] == ":":
            try:
                inc = open(replace).read()
                t = t.replace("%"+search+"%",inc)
            except:
                print("Can't open file '{}'".format(replace))
        else:
            t = t.replace("%"+search+"%",replace)

    return t

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var):
    subpage = {}
    for name, mdata in var.items():
        subpage.update(getattr(mod,mdata['mod']).getPages(t,mdata['settings'],name))

    return subpage

# Builds the site off of a filestructure dictionary.

def buildSite(site):
    try:
        shutil.rmtree("./site/")
    except:
        print("No directory site/, ignoring")

    os.mkdir("./site/")
    for page, subpages in site.items():
        if page == "index":
            currentDir = "./site"
        else:
            currentDir = "./site/"+page
            os.mkdir(currentDir)

        open(currentDir+"/index.html", "w").write(subpages['default'])

        for subdir, data in subpages.items():
            if subdir != "default":
                os.mkdir(currentDir+"/"+subdir)
                for page, content in data.items():
                    os.mkdir(currentDir+"/"+subdir+"/"+page)
                    open(currentDir+"/"+subdir+"/"+page+"/index.html","w").write(content)
                

if __name__ == "__main__":
    pages = open("pages.json")
    pagedata = json.load(pages)
    pages.close()
    main()
    print("Finished.")
