#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import collections
import base64

import gui
import info
import message

import xmllib

try:
    message.debug("Importing external modules...")
    import loremipsum  # pip install loremipsum
except ImportError:
    message.warn("Failed to import one or more modules")
    message.warn("Some transform handlers may not work")
else:
    message.debug("External modules imported")


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


@gui.transform_handler('"\\" to "/"')
def t(text):
    return text.replace("\\", "/")


@gui.transform_handler("Decode Base64")
def t(text):
    return base64.decodebytes(text.encode()).decode()


def isnumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


@gui.transform_handler("Lorem Ipsum Generator")
def t(text):
    label = "Count of sentences"
    sdd = gui.SimpleDataDialog(
        "Lorem Ipsum Generator",
        [gui.DataEntry(label, 100, validator=isnumber)]
    )

    if not sdd.canceled:
        count = int(sdd.result[label])
        sentences = [
            data[2]
                .replace("b'", "")
                .replace("'", "")
            for data in loremipsum.generate_sentences(count, start_with_lorem=True)
        ]
        return " ".join(sentences)
    return text


@gui.transform_handler("Say Hello")
def t(text):
    entries = [
        gui.DataEntry("Forename", validator=lambda value: value == "Tom"),
        gui.DataEntry("Surname", "Jones", validator=bool),
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


# @gui.transform_handler("Hello 1")
# def t(text):
#     return "Hello 1"
