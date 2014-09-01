'''
'  pnbp - pnbp is not a blogging platform
'  modtool.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''

import sys, module, template

# Built-in module, generates page as subpage
def modPage(t,var,data,name,page):
	if 'settings' in data:
		try:
			if 'template' in data['settings']:
				temp = file(data['settings']['template']).read()

		except:
			print("Error occured at {} using module page".format(page))
			print("Cannot open file {}".format(data['settings']['template']))
			sys.exit()

	else:
		temp = t

	if 'pagevar' in var:
		if 'settings' in data:
			if 'pagevar' in data['settings']:
				var['pagevar'].update(data['settings']['pagevar'])

		temp = template.generate(temp,var['pagevar'],name)

	else:
		temp = template.run(template,name)
	
	if not 'settings' == data:
		t = {'default':temp}

	else:
		if 'location' in meta:
			t = {data['settings']['location']:{'default':temp}}

	return t

# Gets subpages from module specified in data
def getSubpages(t,var,data,name,page):
	returns = {}
	if not "settings" in data:
		data['settings'] = {}

	try:
		returns = getattr(module, data['mod']).getPages(t, data['settings'], name, page)

	except Exception,e:
		print("Error occured at {} using module {}:".format(page,data['mod']))
		if type(e) == KeyError:
			print("Missing attribute {}".format(e))
			sys.exit()

		else:
			print(e)

	return returns

# Runs modules defined in pages.json
#
# t = raw template, var = "pagemod" variables in pages.json (<pagename> -> "pagemod")
def runMod(t,var,page):
	subpage = {}
	for name, meta in var['pagemod'].items():
		if meta['mod'] == "page":
			subpage.update(
				modPage(t,var,meta,name,page)
			)
		
		else:
			subpage.update(
				getSubpages(t,var,meta,name,page)
			)

	return subpage


