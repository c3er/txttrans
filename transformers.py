#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import collections

import gui
import info

import xmllib


@gui.transform_handler("Help")
def help(text):
    readmepath = os.path.join(info.execdir, "README.md")
    with open(readmepath, encoding="utf8") as f:
        return f.read()


@gui.transform_handler("Beatify JSON")
def beautify_json(text):
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


@gui.transform_handler("Beautify XML")
def beautify_xml(text):
    return str(xmllib.str2xml(text))


@gui.transform_handler("Say Hello")
def say_hello(text):
    entries = [
        gui.DataEntry("Forename", validator=lambda value: value == "Tom"),
        gui.DataEntry("Surname", "Jones", validator=lambda value: bool(value)),
        gui.DataEntry("No meaning"),
    ]
    sdd = gui.SimpleDataDialog("Hello", entries)
    result = sdd.result
    if sdd.result:
        return "Hello {} {}".format(result["Forename"], result["Surname"])
    return text


@gui.transform_handler("Raise exception")
def raise_exception(text):
    raise Exception(":-P")
