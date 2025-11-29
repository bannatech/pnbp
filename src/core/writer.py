'''
'  pnbp - pnbp is not a blogging platform
'  writer.py
'  Paul Longtine <paul@banna.tech>
'''
import os
import shutil
import hashlib

static_dir = "data/static/"
index_file = "index.html"

# Handles directories
def handlePages(pageName, loc):
    if pageName == "index":
        return loc[:-1] if loc[-1] == "/" else loc
    else:
        return os.path.join(loc, pageName)

# Builds the site off of a dictionary.
# site = dict of site directory tree/pages, loc = root of site
def writeOut(site, loc, dry_run):
    if not os.path.exists(loc):
        os.mkdir(loc)

    for page, subpages in site.items():
        currentDir = handlePages(page, loc)

        if not os.path.exists(currentDir):
            os.mkdir(currentDir)

        writePages(subpages, currentDir, dry_run)

    loc += "/" if loc[-1] != "/" else ""
    copy_tree(static_dir, loc, dry_run)

def copy_tree(src_dir, dest_dir, dry_run):
    copystring = "HAS  " if not dry_run else "DRY-RUN-COPY"
    for i in os.scandir(src_dir):
        src = os.path.join(src_dir, i.name)
        dest = os.path.join(dest_dir, i.name)
        if i.is_dir():
            if not os.path.exists(dest):
                os.mkdir(dest)
            copy_tree(src, dest, dry_run)
        elif i.is_file():
            srcSize = 0
            s = hashlib.sha256()
            with open(src, 'rb') as f:
                sfile = f.read()
                srcSize = len(sfile)
                s.update(sfile)

            srchash = s.digest()
            if os.path.exists(dest) and os.path.isdir(dest) == False:
                s = hashlib.sha256()
                with open(dest, 'rb') as f:
                    s.update(f.read())
                desthash = s.digest()
            else:
                desthash = 0

            if not dry_run and srchash != desthash:
                copystring = "COPY "
                shutil.copy(src, dest)

            print(f"{copystring} {s.hexdigest()} {dest} {srcSize}")


# Format subpage name to filename used in filesystem
# name = name of subpage
def toFS(name, cur):
    fsplit = name.split(".")
    fname = ""
    dirname = None

    # Determine what kind of filename this will have
    if len(fsplit) < 2:
        if fsplit[0] != "index":
            fname = index_file
            dirname = name
        else:
            fname = index_file
    else:
        fname = name

    if dirname is not None:
        dirname = os.path.join(cur, dirname)
    else:
        dirname = cur

    return fname, dirname


# Recursive loop through all subpages
# d = dict of all subpages, cur = Current directory
def writePages(d, cur, dry_run):
    writestring = "DRY  "
    for k, v in d.items():
        fname, dirname = toFS(k, cur)
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        if isinstance(v, dict):
            writePages(v, dirname, dry_run)
        else:
            fullpath = os.path.join(dirname, fname)
            s = hashlib.sha256()
            s.update(v.encode())
            curhash = s.digest()
            if not dry_run:
                if os.path.exists(fullpath):
                    s = hashlib.sha256()
                    with open(fullpath, "rb") as f:
                        s.update(f.read())
                    fhash = s.digest()
                    fhx = s.hexdigest()
                else:
                    fhx = "N/A"
                    fhash = 0

                if fhash != curhash:
                    writestring = "WRITE"
                    open(fullpath, "w").write(v)
                else:
                    writestring = "HAS  "

            print(f"{writestring} {s.hexdigest()} {fullpath} {len(v)}")


# Recursive loop to determine the file paths + directories of the resutling site
# d = dict of all subpages, cur = Current directory
def getCurrentPages(d, cur):
    dirs = set()
    files = set()
    for k, v in d.items():
        fname, dirname = toFS(k, cur)

        if dirname not in dirs:
            dirs.add(dirname)

        if isinstance(v, dict):
            d, f = getCurrentPages(v, dirname)
            dirs |= d
            files |= f

        else:
            fullpath = os.path.join(dirname, fname)
            if fullpath not in files:
                files.add(fullpath)

    return dirs, files


# Recursive loop to determine the static directories and files of the site
# base = base directory to scan through
def getCurrentStaticFiles(base, cur):
    dirs = set()
    files = set()
    for i in os.scandir(base):
        destpath = i.path.replace(static_dir, "", 1)
        destpath = os.path.join(cur, destpath)
        if i.is_file():
            if destpath not in files:
                files.add(destpath)
        else:
            dirs.add(destpath)
            d, f = getCurrentStaticFiles(i.path, cur)
            dirs |= d
            files |= f

    return dirs, files


# Removes all files and directories that are not part of the current site
# d = dict of all subpages, cur = Current directory
def removeDeadPages(d, cur, dry_run):
    dirs, files = getCurrentPages(d, cur)
    d, f = getCurrentStaticFiles(static_dir, cur)
    dirs |= d
    files |= f
    removeDeadTreesAndLeafs(dirs, files, cur, dry_run)


# Recursive loop to determine which files and directories are not current
# d = dict of all subpages, cur = Current directory
def removeDeadTreesAndLeafs(dirs, files, cur, dry_run):
    deletestring = "DELETE" if not dry_run else "DRY-RUN-DELETE"
    active_dirs = os.scandir(cur)
    for i in active_dirs:
        if i.is_dir() and i.path not in dirs:
            print(f"{deletestring} DIR {i.path}")
            if not dry_run:
                shutil.rmtree(i.path)
        elif i.is_dir():
            removeDeadTreesAndLeafs(dirs, files, i.path, dry_run)

    active_files = os.scandir(cur)
    for i in active_files:
        if i.is_dir() is False and i.path not in files:
            print(f"{deletestring} FILE {i.path}")
            if not dry_run:
                os.remove(i.path)
