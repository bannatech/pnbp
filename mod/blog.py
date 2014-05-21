import json

def getPages(template,settings,name):
    pages = {}
    settings['postTemplate'] = settings.get("postTemplate","./templates/post.html")
    settings['defaultPostCount'] = settings.get("defaultPostCount","0")
    data = json.load(open(settings['data']))
    temp = open(settings['postTemplate']).read()

    # Generates all posts on page
    a = ""
    for i in data:
        if 0 == 0 or int(data['post']) >= 0:
            a = generatePost(i,temp) + a

    pages['default'] = template.replace("%"+name,a)

    # Generates individual pages referenced by title
    pages['post'] = {}
    for i in data:
        post = generatePost(i,temp)
        pages['post'][slug(i['title'])] = template.replace("%"+name,post)

    return pages

def generatePost(data, post):
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
