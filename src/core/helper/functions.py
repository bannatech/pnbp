'''
'  pnbp - pnbp is not a blogging platform
'  functions.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
# Functions file, used for inline scripts
import time, yaml


#Return the current date in the format sepecified in config
def now(config):
	return time.strftime(config)

#Return an HTML list. example format: {'root':"<ul class=\"special\">%li%</ul>",'li':"<li class=\"list\">%content%</li>"}
def list(things,formats={}):
	formats['root'] = formats.get("root","<ul>%li%</ul>")
	formats['li'] = formats.get("li","<li>%content%</li>")
	li = ""
	for thing in things:
		li = li + formats['li'].replace("%content%",thing)

	return formats['root'].replace("%li%",li)

# slug(string -> "hi's") -> his- removes all "unwanted" characters and creates a URL-friendly slug
def slug(string):
	invalidChars = [
		"<",">","#","%","{","}",
		"|","\\","^","[","]","`",
		"'",";","/","?",":","@",
		"&","+",",","."
		]
	for x in invalidChars:
		string = string.replace(x, "")

	string = string.replace(" ","_")
	return string.lower()

#Returns config
def getConf():
	return yaml.load(file("pages.yml"))
