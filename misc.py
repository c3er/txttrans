#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
