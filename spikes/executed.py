#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string


global_var = "This is global inside the executed code"


@decorator  # Intended access to executor's namespace
def foo():
    pass


@decorator  # Intended access to executor's namespace
def bar():
    print("something")


@decorator  # Intended access to executor's namespace
def test_func():
    print("test")


@decorator  # Intended access to executor's namespace
def something():
    print(global_var)


print("blub")
print("Hallo")
print()
print("foobar")
print(sys.argv)  # Unintended access to executor's namespace
