'''
'  pnbp - pnbp is not a blogging platform
'  __init__.py - the core entrypoint to pnbp
'  Paul Longtine <paul@nanner.co>
'''

import os
import sys
import core.cmd
import core.conf
import core.builder
import core.writer


def execute(arg):
    if os.path.exists(arg.dir):
        print(f"using directory '{arg.dir}'")
        os.chdir(arg.dir)
    else:
        raise Exception(f"'{arg.dir}' does not exist")

    if arg.module_dir != "":
        if os.path.exists(arg.module_dir):
            print(f"using module directory '{arg.module_dir}'")
            core.module.module_path = arg.module_dir
        else:
            raise Exception(f"'{arg.module_dir}' does not exist")

    if arg.init:
        core.cmd.writeBasicConfig()

    conf = core.conf.base()
    conf.fname = arg.pagesname
    conf.ftype = arg.pagestype
    pagedata = conf.load()

    if pagedata is None:
        raise Exception("Did not find pages file")

    site = core.builder.build(pagedata)
    if arg.removedir and os.path.exists(arg.out):
        core.writer.removeOut(arg.out)

    core.writer.writeOut(site, arg.out)
