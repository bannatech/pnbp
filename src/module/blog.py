import json,time

def getPages(template,settings,name,page):
    pages = {}
    settings['postTemplate'] = settings.get("postTemplate","./templates/post.html")
    settings['defaultPostCount'] = settings.get("defaultPostCount","0")
    settings['description'] = settings.get("description","0")
    data = json.load(file(settings['data']))
    temp = file(settings['postTemplate']).read()

    # Generates all posts on page (/all)
    a = ""
    posts = 0
    for i in data:
        a = generatePost(i,temp,page) + a
        posts += 1

    pages['all']= {}
    pages['all']['default'] = template.replace("%"+name+"%",a)
    
    # Generates index
    a = ""
    for i in data:
        if int(settings['defaultPostCount']) == 0 or int(i['post']) >= posts-int(settings['defaultPostCount']):
            back = i['content']
            if settings['description'] != "0":
                i['content'] = i['description']
            a = generatePost(i,temp,page) + a
            i['content'] = back

    pages['default'] = template.replace("%"+name+"%",a)

    # Generates individual pages referenced by title (/post/<title>)
    pages['post'] = {}
    for i in data:
        post = generatePost(i,temp,page)
        pages['post'][slug(i['title'])] = template.replace("%"+name+"%",post)    

    return pages


#Generates post out of given template, data and page name, returns string
def generatePost(data, post, page):
    for name,x in data.items():
        if name == 'title':
            if page == "index":
                linkpage = ""

            else:
                linkpage = page + "/"

            post = post.replace("%titlelink%","/"+linkpage+"post/"+slug(x))
            post = post.replace("%"+name+"%", x)

        elif name == 'date':
            config = getConfig("%date:",post)
            if config == "none":
                post = post.replace("%date:none%",x)
            elif config == "-1":
                post = post.replace("%date%",x)
            else:
                post = post.replace(
                    "%date:"+config+"%",
                    time.strftime(config.replace("&","%"),time.strptime(x,"%Y-%m-%d")))
        elif name == 'description':
            pass

        else:
            post = post.replace("%"+name+"%", x)

    return post
                

# Helper functions

# slug(string -> "hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
def slug(string):
    invalidChars = [
        "<",">","#","%","{","}",
        "|","\\","^","[","]","`",
        "'",";","/","?",":","@",
        "&","+",",","."
        ]
    for x in invalidChars:
        string = string.replace(x, "")

    string = string.replace(" ","_")
    return string.lower()

# getConfig(string -> index, string -> data) -> gets "config" data ex. (%blah:<config>%)
def getConfig(index,data):
    retVal = ""
    try:
        pointer = data.index(index)+len(index)
    except:
        retVal = "-1"
    if retVal != "-1":
        while data[pointer] != "%" and retVal != "-1":
            retVal = retVal + data[pointer]
            pointer += 1
    return retVal
