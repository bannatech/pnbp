#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'''
import os, shutil, mod, json

def main():
    site = {}
    
    #Loops through defined "sites"
    for name,v in pagedata.items():
        try:
            template = open(v['template']).read()
        except:
            print("Can't open file '{}'".format(v['template']))

        template = generateTemplate(template,v['pagevar'],name)

        site[name] = runMod(template,v['pagemod'],name)
    
    buildSite(site)

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generateTemplate(t,var,page):
    if page == "index":
        page = ""

    t = t.replace("%page%",page)
    for search,replace in var.items():
        if search[0] == ":":
            try:
                inc = open(replace).read()
                inc = inc.replace("%page%", page)
                for subsearch,subreplace in var.items():
                    inc = inc.replace("%"+subsearch+"%",subreplace)

                t = t.replace("%"+search+"%",inc)

            except:
                print("Can't open file '{}'".format(replace))

        else:
            t = t.replace("%"+search+"%",replace)

    return t

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
    subpage = {}
    for name, mdata in var.items():
        subpage.update(getattr(mod,mdata['mod']).getPages(t,mdata['settings'],name,page))

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
                    if page != "default":
                        os.mkdir(currentDir+"/"+subdir+"/"+page)
                        open(currentDir+"/"+subdir+"/"+page+"/index.html","w").write(content)
                    else:
                        open(currentDir+"/"+subdir+"/index.html", "w").write(data['default'])
                

if __name__ == "__main__":
    print("Going through pages...")
    try:
        pages = open("pages.json")
    except:
        print("Can't open file 'pages.json'")        
    pagedata = json.load(pages)
    pages.close()
    main()
    print("Finished.")
