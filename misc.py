#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import collections


class curry:
    """Handles arguments for callback functions."""
    def __init__(self, callback, *args, **kw):
        self.callback = callback
        self.args = args
        self.kw = kw

    def __call__(self):
        return self.callback(*self.args, **self.kw)


def islistlike(listobj):
    return isinstance(listobj, (list, tuple, collections.UserList))


def getstarterdir():
    return getscriptpath(sys.argv[0])


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def obj2str(obj):
    """For debugging
    Get a string, containing the attributes and their values of the
    given object.
    """
    return "\n".join("{}\t{}".format(attr, getattr(obj, attr)) for attr in dir(obj))
