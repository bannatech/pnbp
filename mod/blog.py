import json

def getPages(template,settings,name,page):
    pages = {}
    settings['postTemplate'] = settings.get("postTemplate","./templates/post.html")
    settings['defaultPostCount'] = settings.get("defaultPostCount","0")
    data = json.load(open(settings['data']))
    temp = open(settings['postTemplate']).read()

    # Generates all posts on page (/all
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
        if int(settings['defaultPostCount']) == 0 or int(i['post']) >= posts-int(settings['defaultPostCount']) :
            a = generatePost(i,temp,page) + a

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
                page = ""
            else:
                page = page + "/"

            post = post.replace("%titlelink%","/"+page+"post/"+slug(x))

        post = post.replace("%"+name+"%", x)

    return post
                

# Helper functions

# slug("hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
def slug(string):
    invalidChars = ["<",">","#","%","{","}","|","\\","^","[","]","`","'",";","/","?",":","@","&","+",",","."]
    for x in invalidChars:
        string = string.replace(x, "")

    string = string.replace(" ","_")
    return string.lower()
