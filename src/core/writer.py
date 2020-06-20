'''
'  pnbp - pnbp is not a blogging platform
'  writer.py
'  Paul Longtine <paul@nanner.co>
'''
import os
import shutil


def removeOut(loc):
    for i in os.scandir(loc):
        print(f"DELETE {i.path}")
        if i.is_dir():
            shutil.rmtree(i.path)
        else:
            os.remove(i.path)


# Builds the site off of a dictionary.
# site = dict of site directory tree/pages, loc = root of site
def writeOut(site, loc):
    if not os.path.exists(loc):
        os.mkdir(loc)

    for page, subpages in site.items():
        currentDir = handlePages(page, loc)

        if not os.path.exists(currentDir):
            os.mkdir(currentDir)

        writePages(subpages, currentDir)

    loc += "/" if loc[-1] != "/" else ""

    for i in os.scandir("data/static/"):
        src = os.path.join("data/static/", i.name)
        dest = os.path.join(loc, i.name)
        print(f"COPY {src} -> {dest}")
        if i.is_file():
            shutil.copy(src, dest)
        else:
            shutil.copytree(src, dest, dirs_exist_ok=True)


# Handles directories
def handlePages(pageName, loc):
    if pageName == "index":
        return loc[:-1] if loc[-1] == "/" else loc

    else:
        return os.path.join(loc, pageName)


# Format subpage name to filename used in filesystem
# name = name of subpage
def toFS(name, cur):
    fsplit = name.split(".")
    fname = ""
    dirname = None

    # Determine what kind of filename this will have
    if len(fsplit) < 2:
        if fsplit[0] != "index":
            fname = "index.html"
            dirname = name
        else:
            fname = "index.html"
    else:
        fname = name

    if dirname is not None:
        dirname = os.path.join(cur, dirname)
    else:
        dirname = cur

    return fname, dirname


# Recursive loop through all subpages
# d = dict of all subpages, cur = Current directory
def writePages(d, cur):
    for k, v in d.items():
        fname, dirname = toFS(k, cur)
        if dirname is not None and not os.path.exists(dirname):
            os.mkdir(dirname)

        if isinstance(v, dict):
            writePages(v, dirname)
        else:
            fullpath = os.path.join(dirname, fname)
            print(f"WRITE {fullpath}")
            open(fullpath, "w").write(v)
