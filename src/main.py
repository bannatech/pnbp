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

#CLI Interface function
#args = list of command line arguementsn
def cli(args):
    bd = "site/"
    if len(args) > 1:
        for i in args:
            if i[0] != "-" and args.index(i) != 0:
                bd = i
            
            elif i == "-d":
                os.chdir(args.pop(args.index(i)+1))
            
            elif i == "--help":
                print("Usage: build [OPTION(s)]... [DIR]...\n"
                      "Build site in DIR using configuration in pwd\n"
                      "\n"
                      "  -d DIR      Use configuration in DIR, when not specified DIR is 'site/'\n"
                      "  -i, --init  Make a new site using the bare minimium config and build it in DIR\n"
                      "      --help  Display this help and exit\n")
                
                sys.exit()
            
            elif 0 != args.index(i):
                print("Unknown option: {}".format(i))
            
    if "--init" in args or "-i" in args:
        init()

    return bd

if __name__ == "__main__":
    #Save the time for the caluation
    start = time.time()
    
    #Try to build the site
    try: core.build(cli(sys.argv))
    except:
        print("Something went wrong...")

        traceback.print_exc(file=sys.stdout)
        sys.exit()
    #Print the time it took for the calculation
    print("Finished in {} ms.".format((time.time()-start)*1000))


