#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  init.py
'  Paul Longtine <paul@nanner.co>
'
'  For documentation, please visit http://pnbp.nanner.co
'''

import core, shtml, stagit

from time import time
from optparse import OptionParser

def parsearg():
	parser = OptionParser()

	parser.add_option("-d", dest="dir", default=".",
	                  help="set site project root directory", metavar="<dir>")
	parser.add_option("-o", dest="out", default="site",
	                  help="where to output", metavar="<out>")
	return parser.parse_args()

if __name__ == "__main__":
	#Save the time for the caluation
	start = time()

	#Parse arguements
	options, args = parsearg()

	#Tries to run the jobs
	core.init(options)

	#Do the thing after
	stagit.init(options)

	#Print the time it took to build the site
	print("Finished in {} ms.".format((time()-start)*1000))


