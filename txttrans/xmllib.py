#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""If no wheel fits your requirements, invent an own one!
A try to make an XML library that is able to pretty print an XML.
"""


import sys
import os
import html.parser


class XMLNodeBase:
    def __init__(self):
        pass


class XMLReader(html.parser.HTMLParser):
    def handle_decl(self, decl):
        print("Doctype: " + decl, type(decl), sep='\t')

    def unknown_decl(self, data):
        print("Decl: " + data, type(data), sep='\t')

    def handle_pi(self, data):
        print("PI: " + data, type(data), sep='\t')

    def handle_comment(self, data):
        print("Comment: " + data, type(data), sep='\t')

    def handle_starttag(self, tag, attrs):
        print('Starttag: ' + tag, attrs, sep='\t')

    def handle_startendtag(self, tag, attrs):
        print('Startendtag: ' + tag, attrs, sep='\t')

    def handle_endtag(self, tag):
        print('Endtag: ' + tag)

    def handle_data (self, data):
        print('Data: ' + data, type(data), sep='\t')

    def handle_charref(self, name):
        print('Charrref: ' + name, type(name), sep='\t')

    def handle_entityref(self, name):
        print('Entityref: ' + name, type(name), sep='\t')


def main(args):
    xmlfile = args[1]
    with open(xmlfile) as f:
        content = f.read()
    parser = XMLReader()
    parser.feed(content)


if __name__ == "__main__":
    main(sys.argv)