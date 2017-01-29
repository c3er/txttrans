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


def event2str(event):
    """For debugging
    Tool should not react to the F10 key if there are not as many transformers defined
    """
    return "\n".join("{}\t{}".format(attr, getattr(event, attr)) for attr in dir(event))
