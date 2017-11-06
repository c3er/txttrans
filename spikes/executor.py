#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import time
import traceback

import msvcrt


FILE = "executed.py"


def getstarterdir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


data = []
oldcode = None
file = os.path.join(getstarterdir(), FILE)
while not msvcrt.kbhit():
    try:
        with open(file, encoding="utf8") as f:
            codestr = f.read()
        if codestr != oldcode:
            print("Execute", file)
            oldcode = codestr
            code = compile(codestr, file, "exec")

            # Needed trick: Give data object defined here to the code to execute
            exec(code, { "data": data })
            for d in data:
                print(d)
    except:
        print(traceback.format_exc(), file=sys.stderr)
    finally:
        time.sleep(1)
msvcrt.getch()
