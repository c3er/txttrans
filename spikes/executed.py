#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string


global_var = "This is global inside the executed code"


@decorator  # Intended access to executor's namespace
def foo(x):
    raise Exception("Test exception")


@decorator  # Intended access to executor's namespace
def return_value(x):
    return "this value was returned directly"


@decorator  # Intended access to executor's namespace
def return_global(x):
    return global_var


@decorator  # Intended access to executor's namespace
def bar(x):
    print("something")
    return "muhaha"


@decorator  # Intended access to executor's namespace
def test_func(x):
    print(x)


@decorator  # Intended access to executor's namespace
def something(x):
    print(global_var)


print("blub")
print("Hallo")
print()
print("foobar")
print(sys.argv)  # Unintended access to executor's namespace
