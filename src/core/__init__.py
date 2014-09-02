'''
'  pnbp - pnbp is not a blogging platform
'  __init__.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''

import os, sys, yaml

import core.helper.cmd
import core.builder

def init(arg):
	bd = cli(arg)

	#Try to get the config
	try:
		pages = file("pages.yml")

	except:
		print("Can't open file 'pages.yml'")
		sys.exit()

	pagedata = yaml.load(pages)

	core.builder.build(pagedata,bd)

#CLI Interface function
#args = list of command line arguementsn
def cli(args):
	bd = "site/"
	for i in args:
		if i[0] != "-" and args.index(i) != 0:
			bd = i

		elif i == "-d":
			os.chdir(args.pop(args.index(i)+1))
		
		elif i == "--help":
			core.helper.cmd.phelp()
		elif i == "--init" or i == "-i":
			core.helper.cmd.init()

		elif 0 != args.index(i):
			print("Unknown option: {}".format(i))

	return bd
