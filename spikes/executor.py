#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os


FILE = "executed.py"


data = []


def getstarterdir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


file = os.path.join(getstarterdir(), FILE)
with open(file, encoding="utf8") as f:
    codestr = f.read()
code = compile(codestr, file, "exec")
exec(code, { "data": data })
for d in data:
    print(d)
