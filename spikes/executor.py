#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import time
import traceback

import msvcrt


FILE = "executed.py"


# Function list must be global.
# Both, the decorator and the executing function have to be able to access it.
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

                # The function list needs to be initialized right before executing
                functions = []

                # Our namespace shall not be messed up by the executed code
                namespace = globals().copy()
                
                # Execute the file.
                # Because our namespace is given, the file knows the decorator.
                exec(code, namespace)

                # The decorator did its work and functions are registered now
                for f in functions:
                    try:
                        # A parameter that could come from elsewhere
                        param = "A function parameter"

                        # A parameterless wrapper is needed.
                        # Its name is needed too, therefore a lambda is not appropriated
                        def wrapper():
                            return f(param)

                        # Register wrapper's name in namespace
                        namespace[wrapper.__name__] = wrapper

                        # Execute!
                        result = eval(f"{wrapper.__name__}()", namespace)

                        print("Executor:", result)
                    except:
                        # Handle such things like syntax errors
                        print(traceback.format_exc(), file=sys.stderr)
        finally:
            time.sleep(1)
    msvcrt.getch()


if __name__ == "__main__":
    main()
