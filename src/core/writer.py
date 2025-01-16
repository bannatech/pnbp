'''
'  pnbp - pnbp is not a blogging platform
'  writer.py
'  Paul Longtine <paul@nanner.co>
'''
import os
import shutil

static_dir = "data/static/"


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

    for i in os.scandir(static_dir):
        src = os.path.join(static_dir, i.name)
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

        if not os.path.exists(dirname):
            os.mkdir(dirname)

        if isinstance(v, dict):
            writePages(v, dirname)
        else:
            fullpath = os.path.join(dirname, fname)
            print(f"WRITE {fullpath}")
            open(fullpath, "w").write(v)


# Recursive loop to determine the file paths + directories of the resutling site
# d = dict of all subpages, cur = Current directory
def getCurrentPages(d, cur):
    dirs = []
    files = []
    for k, v in d.items():
        fname, dirname = toFS(k, cur)

        if dirname not in dirs:
            dirs.append(dirname)

        if isinstance(v, dict):
            sd, sf = getCurrentPages(v, dirname)
            dirs.extend([d for d in sd if d not in dirs])
            files.extend([f for f in sf if f not in files])

        else:
            fullpath = os.path.join(dirname, fname)
            if fullpath not in files:
                files.append(fullpath)

    return dirs, files


# Recursive loop to determine the static directories and files of the site
# base = base directory to scan through
def getCurrentStaticFiles(base, cur):
    dirs = []
    files = []
    for i in os.scandir(base):
        destpath = i.path.replace(static_dir, "", 1)
        destpath = os.path.join(cur, destpath)
        if i.is_file():
            if destpath not in files:
                files.append(destpath)
        else:
            dirs.append(destpath)
            sd, sf = getCurrentStaticFiles(destpath, cur)
            dirs.extend([d for d in sd if d not in dirs])
            files.extend([f for f in sf if f not in files])

    return dirs, files


# Recursive loop to determine the file paths + directories of the resutling site
# d = dict of all subpages, cur = Current directory
def removeDeadPages(d, cur):
    dirs, files = getCurrentPages(d, cur)
    sd, sf = getCurrentStaticFiles(static_dir, cur)
    dirs.extend([d for d in sd if d not in dirs])
    files.extend([f for f in sf if f not in files])

    active_dirs = os.scandir(cur)
    for i in active_dirs:
        if i.is_dir() and i.path not in dirs:
            print(f"DELETE DIR {i.path}")
            shutil.rmtree(i.path)

    active_files = os.scandir(cur)
    for i in active_files:
        if i.is_dir() is False and i.path not in files:
            print(f"DELETE FILE {i.path}")
            os.remove(i.path)
