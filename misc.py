#!/usr/bin/env python
# -*- coding: utf-8 -*-


import collections


def islistlike(listobj):
    return isinstance(listobj, (list, tuple, collections.UserList))
