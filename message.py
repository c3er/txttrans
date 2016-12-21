#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import traceback


def info(*args, sep=" "):
    print(*args, sep=sep)


def warn(*args, sep=" "):
    print(*args, sep=sep, file=sys.stderr)


def error(*args, sep=" "):
    print(*args, sep=sep, file=sys.stderr)
