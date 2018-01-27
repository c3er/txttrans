#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = [
    "transformer",
    "message",
    "SimpleDataDialog",
    "DataEntry",
    "execdir",
]


import gui
import message
import misc


transformer = gui.transformer
SimpleDataDialog = gui.SimpleDataDialog
DataEntry = gui.DataEntry

# Directory where the tool (txttrans.pyw) is.
# Useful e.g. to put some files there that can be used by a transform handler.
execdir = misc.getstarterdir()
