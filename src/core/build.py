'''
'  pnbp - pnbp is not a blogging platform
'  build.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import os, shutil, module

# Builds the site off of a filestructure dictionary.
#site = dict of site directory tree/pages, loc = root of site
def write(site,loc):
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
			f = "index.html"

			if k == "default":
				k = ""

			elif k[0:4] == "php:":
				f = "{}.php".format(k[4:])
				k = ""

			else:
				k = k + "/"

			try:
				file("{}/{}{}".format(cur,k,f), "w").write(v)

			except:
				try:
					os.mkdir("{}".format(cur))

				except:
					pass

				try:
					os.mkdir("{}/{}".format(cur,k))
				except:
					pass

				file("{}/{}{}".format(cur,k,f), "w").write(v)
