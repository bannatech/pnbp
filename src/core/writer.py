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

# Builds the site off of a dictionary.
# site = dict of site directory tree/pages, loc = root of site
def writeOut(site, loc, dry_run):
    dirs = set()
    files = set()
    if not dry_run and not os.path.exists(loc):
        os.mkdir(loc)

    for page, subpages in site.items():
        if page == "index":
            currentDir = loc.strip('/')
        else:
            currentDir = os.path.join(loc, page)

        if not dry_run and not os.path.exists(currentDir):
            os.mkdir(currentDir)

        d, f = writePages(subpages, currentDir, dry_run)
        dirs |= d
        files |= f

    loc += "/" if loc[-1] != "/" else ""
    d, f = copyTree(static_dir, loc, dry_run)
    dirs |= d
    files |= f

    return dirs, files

def copyTree(src_dir, dest_dir, dry_run):
    dirs = set()
    files = set()
    copystring = "HAS"
    for i in os.scandir(src_dir):
        src_path = os.path.join(src_dir, i.name)
        dest_path = os.path.join(dest_dir, i.name)
        if i.is_dir():
            dirs.add(dest_path)
            if not dry_run and not os.path.exists(dest_path):
                os.mkdir(dest_path)
            d, f = copyTree(src_path, dest_path, dry_run)
            dirs |= d
            files |= f
        elif i.is_file():
            if dest_path not in files:
                files.add(dest_path)
            with open(src_path, 'rb') as f:
                srcfile = f.read()
                srchash = hashlib.sha256(srcfile).digest()
                srcsize = len(srcfile)

            desthash = b''
            if os.path.exists(dest_path) and os.path.isdir(dest_path) == False:
                with open(dest_path, 'rb') as f:
                    desthash = hashlib.sha256(f.read()).digest()

            if srchash != desthash:
                if not dry_run:
                    copystring = "COPY"
                    shutil.copy(src_path, dest_path)
                else:
                    copystring = f"DIFF != {desthash.hex()}"

            print(f"{copystring} {srchash.hex()} {dest_path} {srcsize}")

    return dirs, files


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

    dirname = os.path.join(cur, dirname) if dirname is not None else cur


    return fname, dirname


# Recursive loop through all subpages
# d = dict of all subpages, cur = Current directory
def writePages(d, cur, dry_run):
    dirs = set()
    files = set()
    writestring = "DRY"
    for k, v in d.items():
        fname, dirname = toFS(k, cur)
        dirs.add(dirname)
        if not dry_run and not os.path.exists(dirname):
            os.mkdir(dirname)

        if isinstance(v, dict):
            d, f = writePages(v, dirname, dry_run)
            dirs |= d
            files |= f
        else:
            fullpath = os.path.join(dirname, fname)
            if fullpath not in files:
                files.add(fullpath)
            curhash = hashlib.sha256(v.encode()).digest()
            desthash = b''
            if os.path.exists(fullpath):
                with open(fullpath, "rb") as f:
                    desthash = hashlib.sha256(f.read()).digest()

            if desthash != curhash:
                if not dry_run:
                    writestring = "WRITE"
                    open(fullpath, "w").write(v)
                else:
                    writestring = f"DIFF != {desthash.hex()}"
            else:
                writestring = "HAS"

            print(f"{writestring} {curhash.hex()} {fullpath} {len(v)}")

    return dirs, files

# Removes all files and directories that are not part of the current site
# result = tuple of two sets (dirs, files), cur = Current directory
def removeDeadPages(result, cur, dry_run):
    dirs, files = result
    removeDeadTreesAndLeafs(dirs, files, cur, dry_run)


# Recursive loop to determine which files and directories are not current
# d = dict of all subpages, cur = Current directory
def removeDeadTreesAndLeafs(dirs, files, cur, dry_run):
    deletestring = "DELETE" if not dry_run else "DRY-DELETE"
    for i in os.scandir(cur):
        if i.is_dir() and i.path not in dirs:
            print(f"{deletestring} DIR {i.path}")
            if not dry_run:
                shutil.rmtree(i.path)

        elif i.is_dir():
            removeDeadTreesAndLeafs(dirs, files, i.path, dry_run)

        elif i.is_dir() is False and i.path not in files:
            print(f"{deletestring} FILE {i.path}")
            if not dry_run:
                os.remove(i.path)
