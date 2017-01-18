#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import enum

import tkinter

import guilib


_handler = None


class MessageHandler:
    def __init__(self, parent):
        self.textbox = tkinter.Text(parent)
        guilib.setup_scrollbars(parent, self.textbox)

    def write(self, msg):
        self.textbox.insert("end", str(msg) + "\n")


class MessageLevel(enum.Enum):
    invalid = 0
    debug   = 1
    info    = 2
    warning = 3
    error   = 4


class Message:
    def __init__(self, msgtype, *args, sep=" "):
        self.type = msgtype
        self.parts = args
        self.separator = sep

    def __str__(self):
        return self.separator.join(self.parts)


def init(parent):
    global _handler
    _handler = MessageHandler(parent)


def info(*args, sep=" "):
    _handler.write(Message(MessageLevel.info, *args, sep=sep))


def warn(*args, sep=" "):
    _handler.write(Message(MessageLevel.warning, *args, sep=sep))


def error(*args, sep=" "):
    _handler.write(Message(MessageLevel.error, *args, sep=sep))
