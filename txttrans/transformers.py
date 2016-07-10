#!/usr/bin/env python
# -*- coding: utf-8 -*-


import gui

import json
import collections

import xmllib


@gui.transform_handler("Help")
def help(text):
    return "XXX Write help text."


@gui.transform_handler("Beatify JSON")
def beautify_json(text):
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


@gui.transform_handler("Beautify XML")
def beautify_xml(text):
    return str(xmllib.str2xml(text))