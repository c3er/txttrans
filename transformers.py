#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import json
import collections
import base64

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


@api.transformer("Beautify XML")
def t(text):
    return str(xmllib.str2xml(text))


@api.transformer('"\\" to "/"')
def t(text):
    return text.replace("\\", "/")


@api.transformer("Decode Base64")
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
        api.DataEntry(label, 100, validator=isnumber)
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


@api.transformer("Return None")
def t(text):
    return None


# @api.transformer("Hello 1")
# def t(text):
#     return "Hello 1"
