'''
'  pnbp - pnbp is not a blogging platform
'  __init__.py
'  Paul Longtine <paul@nanner.co>
'''

import os, sys, yaml

import core.helper.cmd
import core.builder

def init(arg):
	if arg.init:
		core.helper.cmd.init()
	if arg.dir != "":
		i = os.getcwd()
	else:
		if os.path.exists(arg.dir):
			i = arg.dir
		else:
			print("'{}' does not exist".format(arg.dir))
			sys.exit(1)

	#Try to get the config
	try:
		pages = file("pages.yml")

	except:
		print("Can't open file 'pages.yml'")
		sys.exit()

	pagedata = yaml.load(pages)

	core.builder.build(pagedata,arg.dir)

