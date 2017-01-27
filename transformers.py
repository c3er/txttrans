#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import collections

import gui
import info

import xmllib


@gui.transform_handler("Help")
def t(text):
    readmepath = os.path.join(info.execdir, "README.md")
    with open(readmepath, encoding="utf8") as f:
        return f.read()


@gui.transform_handler("Beatify JSON")
def t(text):
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


@gui.transform_handler("Beautify XML")
def t(text):
    return str(xmllib.str2xml(text))


@gui.transform_handler("Say Hello")
def t(text):
    entries = [
        gui.DataEntry("Forename", validator=lambda value: value == "Tom"),
        gui.DataEntry("Surname", "Jones", validator=lambda value: bool(value)),
        gui.DataEntry("No meaning"),
    ]
    sdd = gui.SimpleDataDialog("Hello", entries)
    result = sdd.result
    if result:
        return "Hello {} {}".format(result["Forename"], result["Surname"])
    return text


@gui.transform_handler("Raise exception")
def t(text):
    raise Exception(":-P")


@gui.transform_handler("Return None")
def t(text):
    return None
