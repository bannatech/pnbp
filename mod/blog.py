import json

def getPages(template,settings,name):
    pages = {}
    settings['postTemplate'] = settings.get("postTemplate","./templates/post.html")
    settings['defaultPostCount'] = settings.get("defaultPostCount","0")
    data = json.load(open(settings['data']))
    temp = open(settings['postTemplate']).read()

    # Generates all posts on page
    a = ""
    pages['title'] = {}
    for i in data:
        post = generatePost(i, settings, temp, int(settings['defaultPostCount']))
        a = post + a
        pages['title'][slug(i['title'])] = template.replace("%"+name,post)

    pages['default'] = template.replace("%"+name,a)
    return pages

def generatePost(data, settings, post, defaultPostCount):
    if defaultPostCount == 0 or int(data['post']) >= defaultPostCount:
        for name,x in data.items():
            if name == 'title':
                post = post.replace("%titlelink",slug(x))

            post = post.replace("%"+name, x)

    return post
                

# Helper functions

# slug("hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
def slug(string):
    invalidChars = ["<",">","#","%","{","}","|","\\","^","[","]","`","'",";","/","?",":","@","&","+",",","."]
    for x in invalidChars:
        string = string.replace(x, "")

    string = string.replace(" ","_")
    return string.lower()
