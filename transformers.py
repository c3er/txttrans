#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import api

try:
    api.message.debug("Importing external modules...")
    import loremipsum  # pip install loremipsum
except ImportError:
    api.message.warn("Failed to import one or more modules. Some transform handlers may not work.")
else:
    api.message.debug("External modules imported")


def isnumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


@api.transformer("Help")
def t(text):
    readmepath = os.path.join(api.execdir, "README.md")
    with open(readmepath, encoding="utf8") as f:
        return f.read()


@api.transformer("Lorem Ipsum Generator")
def t(text):
    label = "Count of sentences"
    sdd = api.SimpleDataDialog(
        "Lorem Ipsum Generator",
        api.DataEntry(label, 100, validator=isnumber))

    if not sdd.canceled:
        count = int(sdd.result[label])
        return " ".join(
            data[2]
                # Workaround for a bug in the loremipsum library
                .replace("b'", "")
                .replace("'", "")
            for data in loremipsum.generate_sentences(count, start_with_lorem=True))


@api.transformer('Generate "Hello" transformers')
def t(text):
    label = "Count"
    template = 'api.transformer("Hello {{index}}")(lambda text: "Hello {{index}}")'
    sdd = api.SimpleDataDialog('Generate "Hello" tranformers', api.DataEntry(label, validator=isnumber))
    if not sdd.canceled:
        count = int(sdd.result[label])
        return "\n\n\n".join(
            template.replace("{{index}}", str(i))
            for i in range(1, count + 1))


@api.transformer("Say Hello")
def t(text):
    entries = [
        api.DataEntry("Forename", validator=lambda value: value == "Tom"),
        api.DataEntry("Surname", "Jones", validator=bool),
        api.DataEntry("No meaning"),
    ]
    sdd = api.SimpleDataDialog("Hello", entries)
    if not sdd.canceled:
        result = sdd.result
        return f"Hello {result['Forename']} {result['Surname']}"


@api.transformer("Raise exception")
def t(text):
    raise Exception(":-P")


api.transformer("Return None")(lambda text: None)
