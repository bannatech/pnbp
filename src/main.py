#!/usr/bin/python
'''
'  pnbp - pnbp is not a blogging platform
'  main.py
'  Paul Longtine - paullongtine@gmail.com
'
'  For documentation, please visit http://static.nanner.co/pnbp
'''
import os, sys, traceback, time, core
from initbasic import *

if __name__ == "__main__":
    #Save the time for the caluation
    start = time.time()
    
    #Try to build the site
    try:
        core.build(sys.argv)

    except:
        print("Something went wrong...")

        traceback.print_exc(file=sys.stdout)

        sys.exit()

    #Print the time it took for the calculation
    print("Finished in {} ms.".format((time.time()-start)*1000))


