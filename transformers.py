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


# Source: https://de.wikipedia.org/w/index.php?title=VCard&oldid=166969059#vCard_4.0
_vcard_template = """\
BEGIN:VCARD
VERSION:4.0
N:{{FAMILY_NAME}};{{GIVEN_NAME}};{{ADDITIONAL_NAMES}};{{PREFIXES}};{{SUFFIXES}}
FN:{{PREFIXES}} {{GIVEN_NAME}} {{ADDITIONAL_NAMES}} {{FAMILY_NAME}} {{SUFFIXES}}
ORG:{{ORGANIZATION}}
TEL;TYPE=home,voice;VALUE=uri:tel{{TELEFON_NUMBER}}
ADR;TYPE=home;LABEL="{{STREET}} {{STREET_NUMBER}}\n{{POSTAL_CODE}} {{CITY}}\nDeutschland"
 :;;{{STREET}} {{STREET_NUMBER}};{{CITY}};;{{POSTAL_CODE}};Germany
EMAIL:{{EMAIL_ADDRESS}}
END:VCARD
"""


@api.transformer("Generate vCard")
def t(text):
    PREFIXES_LABEL = "Prefixes"
    GIVEN_NAME_LABEL = "Given name"
    ADDITIONAL_NAMES_LABEL = "Additional names"
    FAMILY_NAME_LABEL = "Family name"
    SUFFIXES_LABEL = "Suffixes"
    ORGANIZATION_LABEL ="Organization"
    TELEFON_NUMBER_LABEL = "Telefon number"
    STREET_LABEL = "Street"
    STREEL_NUMBER_LABEL = "Street number"
    CITY_LABEL = "City"
    POSTAL_CODE_LABEL = "Postal code"
    EMAIL_ADDRESS_LABEL = "E-Mail address"

    entries = [
        api.DataEntry(PREFIXES_LABEL),
        api.DataEntry(GIVEN_NAME_LABEL, validator=bool),
        api.DataEntry(ADDITIONAL_NAMES_LABEL),
        api.DataEntry(FAMILY_NAME_LABEL, validator=bool),
        api.DataEntry(SUFFIXES_LABEL),
        api.DataEntry(ORGANIZATION_LABEL, "Privat"),
        api.DataEntry(TELEFON_NUMBER_LABEL, "+49 "),
        api.DataEntry(STREET_LABEL),
        api.DataEntry(STREEL_NUMBER_LABEL),
        api.DataEntry(CITY_LABEL),
        api.DataEntry(POSTAL_CODE_LABEL),
        api.DataEntry(EMAIL_ADDRESS_LABEL),
    ]

    sdd = api.SimpleDataDialog("Visiting Card", entries)
    if not sdd.canceled:
        result = sdd.result
        return (_vcard_template
            .replace("{{PREFIXES}}", result[PREFIXES_LABEL])
            .replace("{{GIVEN_NAME}}", result[GIVEN_NAME_LABEL])
            .replace("{{ADDITIONAL_NAMES}}", result[ADDITIONAL_NAMES_LABEL])
            .replace("{{FAMILY_NAME}}", result[FAMILY_NAME_LABEL])
            .replace("{{SUFFIXES}}", result[SUFFIXES_LABEL])
            .replace("{{ORGANIZATION}}", result[ORGANIZATION_LABEL])
            .replace("{{TELEFON_NUMBER}}", result[TELEFON_NUMBER_LABEL])
            .replace("{{STREET}}", result[STREET_LABEL])
            .replace("{{STREET_NUMBER}}", result[STREEL_NUMBER_LABEL])
            .replace("{{CITY}}", result[CITY_LABEL])
            .replace("{{POSTAL_CODE}}", result[POSTAL_CODE_LABEL])
            .replace("{{EMAIL_ADDRESS}}", result[EMAIL_ADDRESS_LABEL])
        )


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


@api.transformer("Raise exception")
def t(text):
    raise Exception(":-P")


api.transformer("Return None")(lambda text: None)
