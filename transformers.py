#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import collections
import base64
import re
import string

import api

import xmllib

try:
    api.message.debug("Importing external modules...")
    import loremipsum  # pip install loremipsum
except ImportError:
    api.message.warn("Failed to import one or more modules. Some transform handlers may not work.")
else:
    api.message.debug("External modules imported")


@api.transformer("Help")
def t(text):
    readmepath = os.path.join(api.execdir, "README.md")
    with open(readmepath, encoding="utf8") as f:
        return f.read()


@api.transformer("Beatify JSON")
def t(text):
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


api.transformer("Beautify XML")(lambda text: str(xmllib.str2xml(text)))


api.transformer('"\\" to "/"')(lambda text: text.replace("\\", "/"))


api.transformer("Decode Base64")(lambda text: base64.decodebytes(text.encode()).decode())


@api.transformer("Extract Markdown headers")
def t(text):
    incode = False
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("```"):
            incode = not incode
        if not incode and line.startswith("#"):
            lines.append(line)
    return "\n".join(lines)


class DefaultValueDict(collections.UserDict):
    def __init__(self, default):
        super().__init__()
        self.default = default

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return self.default


@api.transformer("Align Markdown table")
def t(text):
    table = []
    for line in text.splitlines():
        table.append([cell.strip() for cell in line.strip().split("|") if cell])

    column_lengths = DefaultValueDict(0)
    for line in table:
        for i, cell in enumerate(line):
            cellsize = len(cell)
            if column_lengths[i] < cellsize:
                column_lengths[i] = cellsize

    normalized_table = []
    for line in table:
        normalized_table.append([" " + cell.ljust(column_lengths[i] + 1) for i, cell in enumerate(line)])

    output_lines = []
    for line in normalized_table:
        output_lines.append("|" + "|".join(line) + "|")

    return "\n".join(output_lines)


_html_template = '''\
<html>
    <head>
        <title>Links</title>
    </head>
    <body>
        {{LINKS}}
    </body>
</html>
'''


@api.transformer("Links to HTML")
def t(text):
    return _html_template.replace(
        "{{LINKS}}",
        "\n".join('<p><a href="{0}">{0}</a></p>'.format(link) for link in text.splitlines()))


@api.transformer('Generate "Hello" transformers')
def t(text):
    label = "Count"
    template = 'api.transformer("Hello {{index}}")(lambda text: "Hello {{index}}")'
    sdd = api.SimpleDataDialog(
        'Generate "Hello" tranformers',
        api.DataEntry(label, validator=lambda value: all(char in string.digits for char in value)))
    if not sdd.canceled:
        count = int(sdd.result[label])
        return "\n\n\n".join(
            template.replace("{{index}}", str(i))
            for i in range(1, count + 1))


def isnumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


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


@api.transformer("Say Hello")
def t(text):
    entries = [
        api.DataEntry("Forename", validator=lambda value: value == "Tom"),
        api.DataEntry("Surname", "Jones", validator=bool),
        api.DataEntry("No meaning"),
    ]
    sdd = api.SimpleDataDialog("Hello", entries)
    result = sdd.result
    if result:
        return "Hello {} {}".format(result["Forename"], result["Surname"])
    return text


@api.transformer("Raise exception")
def t(text):
    raise Exception(":-P")


api.transformer("Return None")(lambda text: None)
