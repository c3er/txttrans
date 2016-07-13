"""A parser for XML style files."""

# This file is based on the Python module html.parser of Python 3.5
# This version is cut off the conversions of the element values.

# XXX There should be a way to distinguish between PCDATA (parsed
# character data -- the normal case), RCDATA (replaceable character
# data -- only char and entity references and end tags are special)
# and CDATA (character data -- only end tags are special).


import re
import warnings
import _markupbase


__all__ = ['HTMLParser']

# Regular expressions used for parsing

interesting_normal = re.compile('<')
incomplete = re.compile('&[a-zA-Z#]')

starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile(r'--\s*>')

# Note:
#  1) if you change tagfind/attrfind remember to update locatestarttagend too;
#  2) if you change tagfind/attrfind and/or locatestarttagend the parser will
#     explode, so don't do it.
# see http://www.w3.org/TR/html5/tokenization.html#tag-open-state
# and http://www.w3.org/TR/html5/tokenization.html#tag-name-state

tagfind_tolerant = re.compile('([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*')

attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')

locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][^\t\n\r\f />\x00]*       # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
         (?:\s*,)*                   # possibly followed by a comma
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)

endtag_end = re.compile('>')

# the HTML 5 spec, section 8.1.2.2, doesn't allow spaces between
# </ and the tag name, so maybe this should be fixed
endtagfind = re.compile('</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>')



class HTMLParser(_markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

    Usage:
        p = HTMLParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  If convert_charrefs is
    True the character references are converted automatically to the
    corresponding Unicode character (and self.handle_data() is no
    longer split in chunks), otherwise they are passed by calling
    self.handle_entityref() or self.handle_charref() with the string
    containing respectively the named or numeric reference as the
    argument.
    """

    CDATA_CONTENT_ELEMENTS = ("script", "style")

    def __init__(self):
        """Initialize and reset this instance."""
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        self.cdata_elem = None
        _markupbase.ParserBase.reset(self)

    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

    def set_cdata_mode(self, elem):
        self.cdata_elem = elem
        self.interesting = re.compile(r'</\s*%s\s*>' % self.cdata_elem, re.I)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None

    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.  If 'end' is
    # true, force handling all data as if followed by EOF marker.
    def goahead(self, end):
        rawdata = self.rawdata
        startswith = rawdata.startswith  # Optimization
        curpos = 0
        endpos = len(rawdata)
        while curpos < endpos:
            match = self.interesting.search(rawdata, curpos)  # < or &
            if match:
                tmpendpos = match.start()
            else:
                if self.cdata_elem:
                    break
                tmpendpos = endpos
            if curpos < tmpendpos:
                self.handle_data(rawdata[curpos : tmpendpos])
            curpos = self.updatepos(curpos, tmpendpos)
            if curpos == endpos:
                break
            if startswith('<', curpos):
                if starttagopen.match(rawdata, curpos): # < + letter
                    elem_endpos = self.parse_starttag(curpos)
                elif startswith("</", curpos):
                    elem_endpos = self.parse_endtag(curpos)
                elif startswith("<!--", curpos):
                    elem_endpos = self.parse_comment(curpos)
                elif startswith("<?", curpos):
                    elem_endpos = self.parse_pi(curpos)
                elif startswith("<!", curpos):
                    elem_endpos = self.parse_html_declaration(curpos)
                elif (curpos + 1) < endpos:
                    self.handle_data("<")
                    elem_endpos = curpos + 1
                else:
                    break
                if elem_endpos < 0:
                    if not end:
                        break
                    elem_endpos = rawdata.find('>', curpos + 1)
                    if elem_endpos < 0:
                        elem_endpos = rawdata.find('<', curpos + 1)
                        if elem_endpos < 0:
                            elem_endpos = curpos + 1
                    else:
                        elem_endpos += 1
                    if self.convert_charrefs and not self.cdata_elem:
                        self.handle_data(unescape(rawdata[curpos : elem_endpos]))
                    else:
                        self.handle_data(rawdata[curpos : elem_endpos])
                curpos = self.updatepos(curpos, elem_endpos)
            else:
                assert 0, "interesting.search() lied"
        # end while

        if end and curpos < endpos and not self.cdata_elem:
            if self.convert_charrefs and not self.cdata_elem:
                self.handle_data(unescape(rawdata[curpos : endpos]))
            else:
                self.handle_data(rawdata[curpos : endpos])
            curpos = self.updatepos(curpos, endpos)
        self.rawdata = rawdata[curpos:]

    # Internal -- parse html declarations, return length or -1 if not terminated
    # See w3.org/TR/html5/tokenization.html#markup-declaration-open-state
    # See also parse_declaration in _markupbase
    def parse_html_declaration(self, startpos):
        rawdata = self.rawdata
        assert rawdata[startpos : startpos + 2] == '<!', ('unexpected call to '
                                        'parse_html_declaration()')
        if rawdata[startpos : startpos + 4] == '<!--':
            # this case is actually already handled in goahead()
            return self.parse_comment(startpos)
        elif rawdata[startpos : startpos + 3] == '<![':
            return self.parse_marked_section(startpos)
        elif rawdata[startpos : startpos + 9].lower() == '<!doctype':
            # find the closing >
            endpos = rawdata.find('>', startpos + 9)
            if endpos == -1:
                return -1
            self.handle_decl(rawdata[startpos + 2 : endpos])
            return endpos + 1
        else:
            return self.parse_bogus_comment(startpos)

    # Internal -- parse bogus comment, return length or -1 if not terminated
    # see http://www.w3.org/TR/html5/tokenization.html#bogus-comment-state
    def parse_bogus_comment(self, startpos, report=True):
        rawdata = self.rawdata
        assert rawdata[startpos : startpos + 2] in ('<!', '</'), ('unexpected call to '
                                                'parse_comment()')
        endpos = rawdata.find('>', startpos + 2)
        if endpos == -1:
            return -1
        if report:
            self.handle_comment(rawdata[startpos + 2 : endpos])
        return endpos + 1

    # Internal -- parse processing instr, return end or -1 if not terminated
    def parse_pi(self, startpos):
        rawdata = self.rawdata
        assert rawdata[startpos : startpos + 2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, startpos + 2) # >
        if not match:
            return -1
        endpos = match.start()
        self.handle_pi(rawdata[startpos + 2: endpos])
        endpos = match.end()
        return endpos

    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_starttag(self, startpos):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(startpos)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[startpos : endpos]

        # Now parse the data between the start position + 1 and the end position into a tag and its attributes
        attrs = []
        match = tagfind_tolerant.match(rawdata, startpos + 1)
        assert match, 'unexpected call to parse_starttag()'
        curpos = match.end()
        self.lasttag = tag = match.group(1)
        while curpos < endpos:
            attrmatch = attrfind_tolerant.match(rawdata, curpos)
            if not attrmatch:
                break
            attrname, rest, attrvalue = attrmatch.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1 : -1]
            attrs.append((attrname, attrvalue))
            curpos = attrmatch.end()

        end = rawdata[curpos : endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[startpos : endpos])
            return endpos
        if end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    # Internal -- check to see if we have a complete starttag; return end
    # or -1 if incomplete.
    def check_for_whole_start_tag(self, startpos):
        rawdata = self.rawdata
        starttagend_match = locatestarttagend_tolerant.match(rawdata, startpos)
        if starttagend_match:
            endpos = starttagend_match.end()
            next = rawdata[endpos : endpos + 1]
            if next == ">":
                return endpos + 1
            if next == "/":
                if rawdata.startswith("/>", endpos):
                    return endpos + 2
                if rawdata.startswith("/", endpos):
                    # buffer boundary
                    return -1
                # else bogus input
                if endpos > startpos:
                    return endpos
                else:
                    return startpos + 1
            if next == "":
                # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if endpos > startpos:
                return endpos
            else:
                return startpos + 1
        raise AssertionError("we should not get here!")

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_endtag(self, startpos):
        rawdata = self.rawdata
        assert rawdata[startpos : startpos + 2] == "</", "unexpected call to parse_endtag"
        match = endtag_end.search(rawdata, startpos + 1) # >
        if not match:
            return -1
        endpos = match.end()
        match = endtagfind.match(rawdata, startpos) # </ + tag + >
        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[startpos : endpos])
                return endpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, startpos + 2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[startpos : startpos + 3] == '</>':
                    return startpos + 3
                else:
                    return self.parse_bogus_comment(startpos)
            tagname = namematch.group(1)
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after tha name should cover
            # most of the cases and is much simpler
            endpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return endpos + 1

        elem = match.group(1) # script or style
        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[startpos : endpos])
                return endpos

        self.handle_endtag(elem)
        self.clear_cdata_mode()
        return endpos

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        pass

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        pass

    # Obsolete
    def handle_charref(self, name):
        raise NotImplementedError("charref: " + str(name))
    
    # Obsolete
    def handle_entityref(self, name):
        raise NotImplementedError("entityref: " + str(name))

    # Overridable -- handle data
    def handle_data(self, data):
        pass

    # Overridable -- handle comment
    def handle_comment(self, data):
        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass
