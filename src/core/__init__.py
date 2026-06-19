'''
'  pnbp - pnbp is not a blogging platform
'  __init__.py - the core entrypoint to pnbp
'  Paul Longtine <paul@banna.tech>
'''

import os
import sys

import core.cmd
import core.conf
import core.builder
import core.writer


# arg = parsed arguments from core.cmd.parsearg
def execute(arg):
    if os.path.exists(arg.dir):
        print(f"using directory '{arg.dir}'")
        os.chdir(arg.dir)
    else:
        raise Exception(f"'{arg.dir}' does not exist")

    if arg.module_dir != "":
        if os.path.isdir(arg.module_dir):
            print(f"using module directory '{arg.module_dir}'")
            core.module.module_path = arg.module_dir
        else:
            raise Exception(f"'{arg.module_dir}' does not exist")

    if arg.static_dir != "":
        if os.path.isdir(arg.static_dir):
            print(f"using static directory '{arg.static_dir}'")
            core.writer.static_dir = arg.static_dir
        else:
            raise Exception(f"'{arg.static_dir}' does not exist")

    if arg.index_file != "":
        print(f"using index filename '{arg.index_file}'")
        core.writer.index_file = arg.index_file

    if arg.init:
        core.cmd.writeBasicConfig()

    conf = core.conf.base()
    conf.fname = arg.pagesname
    conf.ftype = arg.pagestype
    pagedata = conf.load()
    if pagedata is None:
        raise Exception("pagedata is empty")

    site = core.builder.build(pagedata)
    return core.writer.writeOut(site, arg.out, arg.dry_run, arg.scrub)
