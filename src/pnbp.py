#!/usr/bin/env python3
'''
'  pnbp - pnbp is not a blogging platform
'  pnbp.py
'  Paul Longtine <paul@nanner.co>
'''

import os
import sys
import traceback
from time import monotonic

import core

if __name__ == "__main__":
    # Reference start time for calculating approximate elapsed time
    start = monotonic()

    options, args = core.cmd.parsearg()

    # Attempt to build the site with the options provided
    try:
        core.execute(options)
    except Exception as e:
        print("Error: {}".format(e))
        if options.verbose:
            traceback.print_exc()

        sys.exit(1)

    # Show the elapsed time for assembling the site
    print("Finished in {} ms.".format((monotonic()-start)*1000))
