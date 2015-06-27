import os, yaml

def getPages(template,settings,name,page):
	blogdb = getBlogDB(settings)
	if settings['root'][-1] != "/": settings['root'] = settings['root'] + "/"
	settings['pass'] = settings.get("pass",settings['root'] + "data/.htpasswd")

	d = os.path.dirname(__file__)
	index    = file(os.path.join(d, "data/admin/index.template")).read()
	edit     = file(os.path.join(d, "data/admin/edit.template")).read()
	post     = file(os.path.join(d, "data/admin/post.template")).read()
	htaccess = file(os.path.join(d, "data/admin/htaccess.template")).read()

	return {
		"index.php":index.replace("%db%",blogdb[0][:-1]).replace("%dbn%",blogdb[1][:-1]),
		"edit.php":edit,
		"post.php":post.replace("%root%",settings['root']).replace("%destination%",settings['dest']),
		".htaccess.raw":htaccess.replace("%pass%",settings['pass']).replace("%user%",settings['user'])
	}

def getBlogDB(s):
	dbs = ""
	dbn = ""
	data = yaml.load(file("pages.yml").read())

	for k,v in data.items():
		for m,md in v['pagemod'].items():
			if md['mod'] == "blog":
				if md['settings']['data'][0:2] == "./" or md['settings']['data'][0] != "/":
					if s['root'][-1] != "/": s['root'] = s['root'] + "/"
					dbs = dbs + "\""+s['root']+md['settings']['data'][2:]+"\","

				else:
					dbs = dbs + "\""+md['settings']['data']+"\","

				dbn = dbn + "\""+k+"\","

	return [dbs,dbn]

