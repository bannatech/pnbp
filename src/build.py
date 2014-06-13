#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import os, sys, shutil, module, json, yaml, time

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
                t = {mdata['settings']['location']:{'default':template}}

            subpage.update(t)
            
    return subpage

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
            try:
                os.mkdir(currentDir)
            except:
                pass
        
        subpageLoop(subpages,currentDir)

    for i in os.listdir("data/static/"):
        try:
            shutil.copytree("data/static/"+i,"site/"+i)
        except:
            shutil.copy2("data/static/"+i,"site/"+i)
        
#Recursive loop through all subpages
#d = dict of all subpages, cd = Current directory
def subpageLoop(d,currentDir):
    for k, v in d.iteritems():
        if isinstance(v, dict):
            subpageLoop(v,currentDir + "/" + k)
        else:
            if k == "default":
                k = ""

            else:
                k = k + "/"

            try:
                file("{}/{}index.html".format(currentDir,k), "w").write(v)

            except:
                try:
                    os.mkdir("{}".format(currentDir))

                except:
                    pass

                try:
                    os.mkdir("{}/{}".format(currentDir,k))
                except:
                    pass

                file("{}/{}index.html".format(currentDir,k), "w").write(v)

if __name__ == "__main__":
    print("Going through pages...")
    start = time.time()
    try:
        pages = open("pages")

    except:
        print("Can't open file 'pages'")
        sys.exit()

    pagedata = yaml.load(pages)
    pages.close()
    try:
        main()
    except Exception,e:
        if type(e) == KeyError:
            print("Missing or mistyped value: {}".format(e))
        else:
            print("Something went wrong...")
            print(e)
        sys.exit()
    print("Finished in {} ms.".format((time.time()-start)*1000))
