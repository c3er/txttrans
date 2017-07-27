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
    message.warn("Failed to import one or more modules. Some transform handlers may not work.")
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


@gui.transform_handler("Generate vCard")
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
        gui.DataEntry(PREFIXES_LABEL),
        gui.DataEntry(GIVEN_NAME_LABEL, validator=bool),
        gui.DataEntry(ADDITIONAL_NAMES_LABEL),
        gui.DataEntry(FAMILY_NAME_LABEL, validator=bool),
        gui.DataEntry(SUFFIXES_LABEL),
        gui.DataEntry(ORGANIZATION_LABEL, "Privat"),
        gui.DataEntry(TELEFON_NUMBER_LABEL, "+49 "),
        gui.DataEntry(STREET_LABEL),
        gui.DataEntry(STREEL_NUMBER_LABEL),
        gui.DataEntry(CITY_LABEL),
        gui.DataEntry(POSTAL_CODE_LABEL),
        gui.DataEntry(EMAIL_ADDRESS_LABEL),
    ]

    sdd = gui.SimpleDataDialog("Visiting Card", entries)
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


@gui.transform_handler("Lorem Ipsum Generator")
def t(text):
    label = "Count of sentences"
    sdd = gui.SimpleDataDialog(
        "Lorem Ipsum Generator",
        gui.DataEntry(label, 100, validator=isnumber)
    )

    if not sdd.canceled:
        count = int(sdd.result[label])
        sentences = [
            data[2]
                # Workaround for a bug in the loremipsum library
                .replace("b'", "")
                .replace("'", "")
            for data in loremipsum.generate_sentences(count, start_with_lorem=True)
        ]
        return " ".join(sentences)


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


@gui.transform_handler("Raise exception")
def t(text):
    raise Exception(":-P")


@gui.transform_handler("Return None")
def t(text):
    return None


# @gui.transform_handler("Hello 1")
# def t(text):
#     return "Hello 1"
