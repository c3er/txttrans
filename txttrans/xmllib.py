#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""If no wheel fits your requirements, invent an own one!
A try to make an XML library that is able to pretty print an XML.
"""


import sys
import os
import collections
import html.parser


class XMLError(Exception):
    pass


class XMLDocument:
    def __init__(self, doctype=None, nodes=[]):
        assert isinstance(nodes, (list, collections.UserList))
        self.nodes = nodes
        self.doctype = doctype

    def __str__(self):
        nodestrings = [str(node) for node in self.nodes]
        if self.doctype:
            nodestrings = [self.doctype] + nodestrings
        return "\n".join(nodestrings)

    def add_node(self, node):
        self.nodes.append(node)

    @staticmethod
    def fromstring(string):
        with XMLReader() as parser:
            parser.feed(string)
            return parser.xml


class XMLChildList(collections.UserList):
    def __init__(self, node):
        super().__init__()
        self.node = node

    def append(self, item):
        assert isinstance(item, XMLNodeBase)
        item.parent = item
        super().append(item)

class XMLAttribute:
    def __init__(self, attr, val):
        self.attr = attr
        self.val = val

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.attr == other.attr and self.val == other.val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '{}="{}"'.format(self.attr, self.val)


class XMLAttributeList(collections.UserList):
    def __init__(self, attrs=[]):
        super().__init__()
        for attr in attrs:
            self.add(attr[0], attr[1])

    def __str__(self):
        return " ".join(str(item) for item in self.data)

    def __contains__(self, item):
        if isinstance(item, XMLAttribute):
            return item in self.data
        elif isinstance(item, str):
            for attr in self.data:
                if attr.attr == item:
                    return True
            return False
        else:
            raise TypeError("Item must be of type 'XMLAttribute' or 'str' (actual: '{}').".format(type(item).__name__))

    def add(self, attr, val):
        assert isinstance(attr, str)
        assert attr not in self
        super().append(XMLAttribute(attr, val))


class XMLNodeBase:
    def __init__(self, parent=None):
        self.parent = None
        if parent:
            parent.add_child(self)

    def __str__(self):
        return self.tostring(0, " " * 4)

    def tostring(self, indentlevel, indentchar):
        raise NotImplementedError()


class XMLNode(XMLNodeBase):
    def __init__(self, name="", attrs=[], parent=None):
        super().__init__(parent)
        self.name = name
        self.attributes = XMLAttributeList(attrs)
        self.children = XMLChildList(self)

    def add_child(self, child):
        self.children.append(child)

    def tostring(self, indentlevel, indentchar):
        indentation = indentchar * indentlevel
        headline = indentation + "<" + self.name
        if self.attributes:
            headline += " " + str(self.attributes)
        if self.children:
            headline += ">"
            footline = "</" + self.name + ">"
            childstrings = [child.tostring(indentlevel + 1, indentchar) for child in self.children]

            separator = self._get_separator()
            if separator == "":
                childstrings = [child.strip() for child in childstrings]
            elif separator == "\n":
                footline = indentation + footline

            text = separator.join([headline] + childstrings + [footline])
        else:
            text = headline + "/>"
        return text

    def _get_separator(self):
        if not self.children:
            return ""
        if len(self.children) > 1:
            return "\n"
        child = self.children[0]
        if not isinstance(child, XMLTextNode):
            return "\n"
        if "\n" not in child.text:
            return ""
        return "\n"


class XMLTextNode(XMLNodeBase):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text.strip()

    def tostring(self, indentlevel, indentchar):
        lines = (line.strip() for line in self.text.split("\n"))
        lines = ((indentchar * indentlevel) + line for line in lines)
        text = "\n".join(lines)
        return text


class XMLCommentNode(XMLNodeBase):
    def __init__(self, content, parent=None):
        super().__init__(parent)
        self.content = content.strip()

    def tostring(self, indentlevel, indentchar):
        indentation = indentchar * indentlevel
        lines = self.content.split("\n")
        if len(lines) > 1:
            # Put the comment marks to their own lines and indent the content one level deeper.
            textlines = (indentation + indentchar + line for line in lines)
            text = "\n".join([indentation + "<!-- "] + textlines + [indentation + " -->"])
            return text
        else:
            text = indentation + "<!-- " + self.content + " -->"
            return text


class XMLReader(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.xml = XMLDocument()
        self.parent = None
        self._stack = []

    # Needed to use it with a "with" statement #################################
    def __enter__(self):
        return self.__class__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    ############################################################################
    
    # Helpers ##################################################################
    def set_doctype(self, decl, firstchar):
        self.xml.doctype = "".join(("<", firstchar, decl, ">"))

    def add_simple_node(self, cls, *args):
        node = cls(*args)
        if not self.parent:
            self.xml.add_node(node)

    def push(self):
        self._stack.append(self.parent)

    def pop(self):
        self.parent = self._stack.pop()
    ############################################################################
    
    # Inherited from html.parser.HTMLParser ####################################
    def handle_decl(self, decl):
        self.set_doctype(decl, "!")

    def unknown_decl(self, data):
        self.set_doctype(data, "!")

    def handle_pi(self, data):
        self.set_doctype(data, "?")

    def handle_comment(self, data):
        self.add_simple_node(XMLCommentNode, data, self.parent)

    def handle_data (self, data):
        if data.strip():
            self.add_simple_node(XMLTextNode, data, self.parent)

    def handle_startendtag(self, tag, attrs):
        self.add_simple_node(XMLNode, tag, attrs, self.parent)

    def handle_starttag(self, tag, attrs):
        self.push()
        node = XMLNode(tag, attrs, self.parent)
        parent = self.parent
        self.parent = node
        if not parent:
            self.xml.add_node(node)

    def handle_endtag(self, tag):
        if self.parent.name != tag:
            raise XMLError("Error at parsing (maybe a start tag without closing tag).")
        self.pop()

    def handle_charref(self, name):
        print("handle_charref:", name)
        super().handle_charref(name)

    def handle_entityref(self, name):
        print("handle_entityref:", name)
        super().handle_entityref(name)
    ############################################################################


def main(args):
    xmlfile = args[1]
    with open(xmlfile) as f:
        content = f.read()
    xmldoc = XMLDocument.fromstring(content)
    print(str(xmldoc))

if __name__ == "__main__":
    main(sys.argv)