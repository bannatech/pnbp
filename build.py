#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'''
import os, sys, shutil, mod, json, time

def main():
    site = {}
    
    #Loops through defined "sites"
    for name,v in pagedata.items():
        try:
            template = file(v['template']).read()

        except:
            print("{}: Can't open file '{}'".format(name,v['template']))
            sys.exit()

        template = generateTemplate(template,v['pagevar'],name)

        site[name] = runMod(template,v,name)
    
    buildSite(site)

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

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
    subpage = {}
    for name, mdata in var['pagemod'].items():
        if mdata['mod'] != "page":
            try:
                subpage.update(getattr(mod,mdata['mod']).getPages(t,mdata['settings'],name,page))

            except Exception,e:
                print("Error occured at {} using module {}:".format(page,mdata['mod']))
                if type(e) == KeyError:
                    print("Missing attribute {}".format(e))
                    sys.exit()

                else:
                    print(e)

        elif mdata['mod'] == "page":
            try:
                template = file(mdata['settings']['template']).read()

            except:
                print("Error occured at {} using module page".format(page))
                print("Cannot open file {}".format(mdata['settings']['template']))
                sys.exit()

            pv = var['pagevar']
            pv.update(mdata['settings']['pagevar'])
            template = generateTemplate(template,pv,name)
            if mdata['settings']['location'] == "":
                t = {'default':template}
            else:
                t = {}
                temp = {}
                for i in mdata['settings']['location'].split("/"):
                    temp[i] = {}
                    

            subpage.update(t)
            
    return subpage

def runInlineScript(template,page):
    try:
        index = template.index("{:")+2
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
        template = template.replace(template[template.index("{:"):template.index(":}")+2],returns)
    
    return template

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
                        file(currentDir+"/"+subdir+"/"+page+"/index.html","w").write(content)

                    else:
                        file(currentDir+"/"+subdir+"/index.html", "w").write(data['default'])

    for i in os.listdir("data/static/"):
        shutil.copytree("data/static/"+i,"site/"+i)
        
if __name__ == "__main__":
    print("Going through pages...")
    start = time.time()
    try:
        pages = open("pages.json")

    except:
        print("Can't open file 'pages.json'")
        sys.exit()

    pagedata = json.load(pages)
    pages.close()
    main()
    print("Finished in {} ms.".format((time.time()-start)*1000))
