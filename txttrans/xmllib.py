#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""If no wheel fits your requirements, invent an own one!
A try to make an XML library that is able to pretty print an XML.
"""


import sys
import html.parser


class XMLNode:
    def __init__(self):
        pass


class XMLReader(html.parser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('Starttag: ' + tag, attrs, sep='\t')

    def handle_endtag(self, tag):
        print('Endtag: ' + tag)

    def handle_data (self, data):
        print('Data: ' + data, type(data), sep='\t')

    def handle_charref(self, name):
        print('Charrref: ' + name, type(name), sep='\t')

    def handle_entityref(self, name):
        print('Entityref: ' + name, type(name), sep='\t')


def main(args):
    print(args)


if __name__ == "__main__":
    main(sys.argv)