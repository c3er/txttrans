#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import collections
import html
import json
import re
import uuid

import api

import xmllib

try:
    api.message.debug("Importing external modules...")
    import loremipsum  # pip install loremipsum
except ImportError:
    api.message.warn("Failed to import one or more modules. Some transform handlers may not work.")
else:
    api.message.debug("External modules imported")


HTML_LINKLIST_TEMPLATE = '''\
<html>
    <head>
        <title>Links</title>
    </head>
    <body>
        {{LINKS}}
    </body>
</html>
'''


class DefaultValueDict(collections.UserDict):
    def __init__(self, default):
        super().__init__()
        self.default = default

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            return self.default


def isnumber(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def first_index(iterable):
    for i, element in enumerate(iterable):
        if element:
            return i
    return None


def extract_markdown_headers(content):
    incode = False
    lines = []
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("```"):
            incode = not incode
        if not incode and line.startswith("#"):
            lines.append(line)
    return "\n".join(lines)


@api.transformer("Beatify JSON")
def t(text):
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


api.transformer("Beautify XML")(lambda text: str(xmllib.str2xml(text)))


api.transformer('"\\" to "/"')(lambda text: text.replace("\\", "/"))


api.transformer('"/" to "\\"')(lambda text: text.replace("/", "\\"))


api.transformer("Unescape backslashes")(lambda text: text.replace(r"\\", "\\"))


api.transformer("Decode Base64")(lambda text: base64.decodebytes(text.encode()).decode(errors="replace"))


api.transformer("Extract Markdown headers")(extract_markdown_headers)


@api.transformer("Align Markdown table")
def t(text):
    # Regard literal pipe "\|"
    # Example: https://github.com/mity/md4c/wiki/Markdown-Syntax:-Tables
    text = text.replace("\\|", "{{LITERAL_PIPE}}")

    table = [
        [
            cell
                .strip()
                .replace("{{LITERAL_PIPE}}", "\\|")
            for cell in line.strip().split("|")
            if cell
        ]
        for line in text.splitlines()
    ]

    column_lengths = DefaultValueDict(0)
    for line in table:
        for i, cell in enumerate(line):
            cellsize = len(cell)
            if column_lengths[i] < cellsize:
                column_lengths[i] = cellsize

    normalized_table = [
        [" " + cell.ljust(column_lengths[i] + 1) for i, cell in enumerate(line)]
        for line in table
    ]

    return "\n".join("|" + "|".join(line) + "|" for line in normalized_table)


@api.transformer("Generate Markdown table of content")
def t(text):
    LINK_PATTERN = r"\[|\]|<.*>|\(.*\)"

    lines = [line.strip() for line in extract_markdown_headers(text).splitlines()]
    levels = [first_index(char != "#" for char in line) for line in lines]
    headers = [re.sub(LINK_PATTERN, "", line.lstrip("# ")) for line in lines]

    targets = []
    for header in headers:
        header = re.sub(LINK_PATTERN + r"|\.|`|\{|\}", "", header).strip()
        targets.append("#" + re.sub(r"\s", "-", header).lower())

    return "\n".join(
        "  " * (level - 1) + f"- [{header}]({target})"
        for level, header, target in zip(levels, headers, targets))


@api.transformer("Links to HTML")
def t(text):
    return HTML_LINKLIST_TEMPLATE.replace(
        "{{LINKS}}",
        "\n".join('<p><a href="{0}">{0}</a></p>'.format(link) for link in text.splitlines()))


api.transformer("Unescape HTML characters")(lambda text: html.unescape(text))


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


@api.transformer("Filter lines")
def t(text):
    label = "Pattern"
    dialog = api.SimpleDataDialog(
        "Filter lines",
        api.DataEntry(label, validator=bool))
    if not dialog.canceled:
        return "\n".join(
            line
            for line in text.splitlines()
            if re.match(dialog.result[label], line))


api.transformer("Break lines at column 120")(
    lambda text: re.sub(r"(.{60,120})\s", r"\1\n", text, flags=re.MULTILINE))


api.transformer("Reverse lines")(lambda text: "\n".join(reversed(text.splitlines())))


api.transformer("Generate GUID")(lambda _: str(uuid.uuid4()))
