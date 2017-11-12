#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import time
import traceback

import msvcrt


FILE = "executed.py"


data = []


def decorator(func):
    """A decorator with side effect to a data structure"""
    data.append(func.__name__)
    return func


def getstarterdir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def main():
    global data
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

                # the data list needs to be initialized right before executing
                data = []

                # Execute the file with the global namespace...
                exec(code)
                for d in data:
                    print(d)
        except:
            print(traceback.format_exc(), file=sys.stderr)
        finally:
            time.sleep(1)
    msvcrt.getch()


if __name__ == "__main__":
    main()
