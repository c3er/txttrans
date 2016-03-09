#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
#import xml.etree.ElementTree as et
#import xml.dom.minidom as minidom
import xml.dom
import xml.dom.xmlbuilder


def xml2str(xmldoc):
    return str(xmldoc)


def main(args):
    xmlfile = args[1]
    with open(xmlfile) as f:
        xmlstr = f.read()
    #xmldoc = et.fromstring(xmlstr)
    #xmldoc = minidom.parseString(xmlstr)
    input = xml.dom.xmlbuilder.DOMInputSource()
    input.stringData = xmlstr
    xmldoc = xml.dom.xmlbuilder.DOMBuilder()
    xmldoc.parse(input)
    print(xml2str(xmldoc))


if __name__ == "__main__":
    main(sys.argv)