import markdown
import json
import time


def getPages(template, settings, modName, pageName):
    pages = {}
    postTemplate = settings.get("postTemplate", "templates/post.html")
    defaultPostCount = settings.get("defaultPostCount", "0")
    genAll = settings.get("genAll", "0")
    genPosts = settings.get("genPosts", "1")
    postsPage = settings.get("postsPage", "post")
    description = settings.get("description", "0")
    contentType = settings.get("contentType", "markdown")
    backend = settings.get("backend", "json")

    data = getDB(settings['data'], backend, contentType)

    temp = open(postTemplate).read()

    namekey = f"%{modName}%"
    posts = len(data)
    if genAll != "0":
        allContent = ""
        posts = 0
        for i in data:
            allContent = generatePost(i, temp, pageName, postsPage) + allContent
            posts += 1

        # Generates all posts on page (/all)
        pages['all'] = {}
        pages['all']['index'] = template.replace(namekey, allContent)

    # Generates index
    indexContent = ""
    for i in data:
        if int(defaultPostCount) == 0 or int(i['post']) >= posts-int(defaultPostCount):
            back = i['content']
            if description != "0":
                i['content'] = i['description']
            indexContent = generatePost(i, temp, pageName, postsPage) + indexContent
            i['content'] = back

    pages['index'] = template.replace(namekey, indexContent)

    # Generates individual pages referenced by title

    posts = {}
    if genPosts != "0":
        for i in data:
            post = generatePost(i, temp, pageName, postsPage)
            posts[slug(i['title'])] = template.replace(namekey, post)

    if postsPage == "":
        pages.update(posts)
    else:
        pages[postsPage] = posts

    return pages


# Generates post out of given template, data and page name, returns string
def generatePost(data, post, pageName, postsPage):
    linkpage = "" if pageName == "index" else pageName + "/"
    linkpost = "" if postsPage == "" else postsPage + "/"

    for name, x in data.items():
        if name == 'title':
            slugx = slug(x)
            post = post.replace("%titlelink%", f"/{linkpage}{linkpost}{slugx}")
            post = post.replace(f"%{name}%", x)
        elif name == 'date':
            config = parseConfig("%date:", post)
            if config is None:
                post = post.replace("%date%", x)
            elif config == "none":
                post = post.replace("%date:none%", x)
            else:
                post = post.replace(
                    f"%date:{config}%",
                    time.strftime(config.replace("&", "%"), time.strptime(x, "%Y-%m-%d")))
        elif name == 'description':
            pass
        else:
            post = post.replace(f"%{name}%", x)

    return post


# Helper functions

# slug(string -> "hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
def slug(string):
    invalidChars = [
        "<", ">", "#", "%", "{", "}",
        "|", "\\", "^", "[", "]", "`",
        "'", ";", "/", "?", ":", "@",
        "&", "+", ", ", "."
        ]
    for x in invalidChars:
        string = string.replace(x, "")

    string = string.replace(" ", "_")
    return string.lower()


# parseConfig(string -> index, string -> data) -> gets "config" data ex. (%blah:<config>%)
def parseConfig(index, data):
    retVal = ""
    try:
        pointer = data.index(index)+len(index)
    except Exception:
        retVal = None

    if retVal is not None:
        while data[pointer] != "%":
            retVal = retVal + data[pointer]
            pointer += 1
    return retVal


def getDB(db, backend, contentType):
    dbdata = {}
    if backend == "json":
        dbdata = json.load(open(db))
        if contentType == "markdown":
            for post in dbdata:
                post['content'] = markdown.markdown(post['content'])

    return dbdata
