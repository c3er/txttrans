#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import time
import traceback

import msvcrt


FILE = "executed.py"


functions = []


def decorator(func):
    """A decorator with side effect to a data structure"""
    functions.append(func)
    return func


def getstarterdir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


def main():
    global functions
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

                # the function list needs to be initialized right before executing
                functions = []

                # Use global namespace and make sure that it does not mess with our namespace
                namespace = globals().copy()
                exec(code, namespace)
                for f in functions:
                    # The trick: the namespace object contains the globals of the executed code
                    exec(f.__code__, namespace)
        except:
            print(traceback.format_exc(), file=sys.stderr)
        finally:
            time.sleep(1)
    msvcrt.getch()


if __name__ == "__main__":
    main()
