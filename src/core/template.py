'''
'  pnbp - pnbp is not a blogging platform
'  template.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''

import re, json, yaml
from helper.functions import *

# Adds in variables defined in pages.json
#
# t = raw template, var = "pagevar" variables in pages.json (<pagename> -> "pagevar")
def generate(t,var,page):
	if page == "index":
		page = ""

	t = t.replace("%page%",page)
	t = run(t,page)
	
	for search,replace in var.items():
		if search[0] == ":":
			try:
				t.index("%"+search+"%")
				exists = True

			except:
				exists = False

			if exists:
				inc = file(replace).read()
				inc = generate(inc,var,page)
				print("Building include: '"+search+"'")
				t = t.replace("%"+search+"%",inc)

		else:
			t = t.replace("%"+search+"%",replace)

	return t

#Takes all code blocks in templates ("{:print("Hi"):}") and executes it, and replaces the block with the "returns" variable
def run(template,page):
	for script in re.findall("{:(.*?):}",template, re.DOTALL):
		returns = ""
		exec(script)
		template = template.replace("{:"+script+":}",returns)
	
	return template
