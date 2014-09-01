'''
'  pnbp - pnbp is not a blogging platform
'  main.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''

import os, sys, yaml

#Helper imports
import core

def build(arg):
	bd = cli(arg)

	#Try to get the config
	try: pages = file("pages.yml")
	except:
		print("Can't open file 'pages.yml'")
		sys.exit()

	pagedata = yaml.load(pages)

	site = {}
	#Loops through defined "sites"
	for name,v in pagedata.items():
		#Read the template
		if 'template' in v:
			try: temp = file(v['template']).read()
			except:
				print("{}: Can't open file '{}'".format(name,v['template']))
				sys.exit()
		else:
			temp = ""

		#Check if pagevar is defined, skip the variable replacement step
		if 'pagevar' in v:
			temp = core.template.generate(temp,v['pagevar'],name)

		else:
			temp = core.template.run(temp,name)
		
		print("Running modules for page: '"+name+"'")

		site[name] = core.modtool.runMod(temp,v,name)

		print("Built page: '"+ name +"'\n")

	core.build.write(site,bd)

#CLI Interface function
#args = list of command line arguementsn
def cli(args):
	bd = "site/"
	for i in args:
		if i[0] != "-" and args.index(i) != 0:
			bd = i
		
		elif i == "-d":
			try:
				os.chdir(args.pop(args.index(i)+1))
			except:
				pass
		
		elif i == "--help":
			print("Usage: build [OPTION(s)]... [DIR]...\n"
				  "Build site in DIR using configuration in pwd\n"
				  "\n"
				  "  -d DIR	  Use configuration in DIR, when not specified DIR is 'site/'\n"
				  "  -i, --init  Make a new site using the bare minimium config and build it in DIR\n"
				  "	  --help  Display this help and exit\n")
			
			sys.exit()
		
		elif i == "--init" or i == "-i":
			core.initbasic.init()

		elif 0 != args.index(i):
			print("Unknown option: {}".format(i))
		
	return bd


