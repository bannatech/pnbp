#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  init.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import sys
import core
from time import time

if __name__ == "__main__":
	#Save the time for the caluation
	start = time()
	
	#Try to build the site
	core.init(sys.argv)

	#Print the time it took to build the site
	print("Finished in {} ms.".format((time()-start)*1000))


