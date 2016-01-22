'''
'  pnbp - pnbp is not a blogging platform
'  builder.py
'  Paul Longtine <paul@nanner.co>
'''
import os, shutil

from datetime import date, datetime

import core.template
import core.module

#Builds the site off of a filestructure dictionary.
#site = dict of site directory tree/pages, loc = root of site
def makeSite(site,loc):
	if not (os.path.isdir("history")):
		os.mkdir("history")

	shutil.move(loc,
		os.path.join("history",
		              loc+date.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S")
		)
	)

	if (os.path.isdir(loc)):
		shutil.rmtree(loc)

	os.mkdir(loc)

	for page, subpages in site.items():
		currentDir = handleDirectory(page,loc)

		subpageLoop(subpages,currentDir)
	
	try:

		for i in os.listdir("data/static/"):
			try:
				shutil.copytree(
					os.path.join("data/static/", i),
					os.path.join(loc, i)
				)
			
			except:
				shutil.copy2(
					os.path.join("data/static/", i),
					os.path.join(loc, i)
				)

	except:
		print("No directory data/static, ignoring")

# Handles directories
#p = name of page, l = location
def handleDirectory(p,l):
	if p == "index":
		r = l[0:-1] if l[-1] == "/" else l

	else:
		r = l+p if l[-1] == "/" else l+"/"+p

		try:
			os.mkdir(r)

		except:
			pass

	return r
	
#Recursive loop through all subpages
#d = dict of all subpages, cd = Current directory
def subpageLoop(d,cur):
	for k, v in d.iteritems():
		if isinstance(v, dict):
			subpageLoop(v, os.path.join(cur, k))
		else:
			f = k.split(".")
			fl = ""

			if len(f) < 2:
				if f[0] != "default":
					fl = f[0] + "/index.html"

				else:
					fl = "index.html"
					k = ""

			else:
				if f[0] != "raw":
					fl = f[0] + "." + f[1]

				else:
					fl = f[0]

			try:
				file("{}/{}".format(cur,fl), "w").write(v)

			except:
				try: os.mkdir("{}".format(cur))
				except: pass

				try: os.mkdir("{}/{}".format(cur,k))
				except: pass

				file("{}/{}".format(cur,fl), "w").write(v)

def build(pd,directory):
	site = {}
	for name,v in pd.items():
		#Read the template
		if 'template' in v:
			try:
				temp = file(v['template']).read()

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

		site[name] = core.module.run(temp,v,name)

		print("Built page: '"+ name +"'\n")

	makeSite(site,directory)
