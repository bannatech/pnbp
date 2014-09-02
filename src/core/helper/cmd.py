'''
'  pnbp - pnbp is not a blogging platform
'  cmd.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''

basicConfig = "index:\n  template: \"template.html\"\n  pagevar:\n    title: \"I'm basic\"\n  pagemod:\n    page:\n      mod: \"page\""
basicTemplate = "<html>\n <body>\n  <h1>%title%</h1>\n  </body>\n</html>"

def init():
	file("pages.yml","w").write(basicConfig)
	file("template.html","w").write(basicTemplate)

def phelp():
	print(
		"Usage: build [OPTION(s)]... [DIR]...\n"
		"Build site in DIR using configuration in pwd\n"
		"\n"
		"  -d DIR  Use configuration in DIR, when not specified DIR is 'site/'\n"
		"  -i, --init  Make a new site using the bare minimium config and build it in DIR\n"
		"  --help  Display this help and exit\n"
	)
