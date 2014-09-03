'''
'  pnbp - pnbp is not a blogging platform
'  builder.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import os, shutil

import core.template
import core.module

#Builds the site off of a filestructure dictionary.
#site = dict of site directory tree/pages, loc = root of site
def makeSite(site,loc):
	try:
		shutil.rmtree(loc)

	except:
		print("No directory {}, ignoring".format(loc))

	os.mkdir(loc)
	for page, subpages in site.items():
		currentDir = handleDirectory(page,loc)

		subpageLoop(subpages,currentDir)

	if loc[-1] != "/":
		loc = loc + "/"
	try:
		for i in os.listdir("data/static/"):
			try:
				shutil.copytree("data/static/"+i,loc+i)
				
			except:
				shutil.copy2("data/static/"+i,loc+i)

	except:
		print("No directory data/static, ignoring")

# Handles directories
#p = name of page, l = location
def handleDirectory(p,l):
	if p == "index":
		if l[-1] == "/":
			r = l[0:-1]

		else:
			r = l

	else:
		if l[-1] == "/":
			r = l+p

		else:
			r = l+"/"+p

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
			subpageLoop(v,cur + "/" + k)
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
