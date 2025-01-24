import markdown
import json
import time


def getPages(template, settings, modName, pageName):
    pages = {}
    backend = settings.get("backend", "json")
    contentType = settings.get("contentType", "markdown")

    postTemplate = settings.get("postTemplate", "templates/post.html")
    genAll = settings.get("genAll", "0")
    genPosts = settings.get("genPosts", "1")
    postsPage = settings.get("postsPage", "post")
    description = settings.get("description", "0")
    defaultPostCount = settings.get("defaultPostCount", "0")

    data = getDB(settings['data'], backend, contentType)
    temp = open(postTemplate).read()

    namekey = f"%{modName}%"
    subjkey = f"%{modName}title%"
    desckey = f"%{modName}desc%"
    posts = len(data)
    if genAll != "0":
        allContent = ""
        posts = 0
        for i in data:
            allContent = generatePost(i, temp, pageName, postsPage) + allContent
            posts += 1

        # Generates all posts on page (/all)
        pages['all'] = {}
        indexpage = template.replace(namekey, allContent)
        indexpage = indexpage.replace(subjkey, "all posts")
        indexpage = indexpage.replace(desckey, "all posts")

        pages['all']['index'] = indexpage

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
            postpage = template.replace(namekey, post)
            postpage = postpage.replace(subjkey, f"{i['title']} - ")
            if 'description' in i:
                postpage = postpage.replace(desckey, f"{i['description']} - ")
            else:
                postpage = postpage.replace(desckey, f"{i['title']} - ")

            pageKey = slug(i['title'])
            posts[pageKey] = postpage

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
            md = markdown.Markdown(
                extensions=[
                    'footnotes',
                    'tables',
                    'def_list',
                    'fenced_code'
                ]
            )
            for post in dbdata:
                post['content'] = md.convert(post['content'])
                md.reset()

    return dbdata
