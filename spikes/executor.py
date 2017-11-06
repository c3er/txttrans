#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import time

import msvcrt


FILE = "executed.py"


def getstarterdir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


data = []
oldcode = None
file = os.path.join(getstarterdir(), FILE)
while not msvcrt.kbhit():
    with open(file, encoding="utf8") as f:
        codestr = f.read()
    if codestr != oldcode:
        oldcode = codestr
        code = compile(codestr, file, "exec")
        exec(code, { "data": data })
        for d in data:
            print(d)
    time.sleep(1)
