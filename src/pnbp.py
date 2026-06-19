#!/usr/bin/env python3
'''
'  pnbp - pnbp is not a blogging platform
'  pnbp.py
'  Paul Longtine <paul@banna.tech>
'''

import os
import sys
import traceback
from time import monotonic

import core

if __name__ == "__main__":
    # Reference start time for calculating approximate elapsed time
    start = monotonic()

    args, _ = core.cmd.parsearg()

    # Attempt to build the site with the options provided
    try:
        files, dirs = core.execute(args)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

    duration = (monotonic() - start) * 1000
    # Show the elapsed time for assembling the site and the number of files/dirs
    print(f"generated {len(files)} files across {len(dirs)} dirs in {duration} ms")