#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import enum
import tkinter

import gui.lib

import config


_handler = None


class MessageHandler:
    def __init__(self, parent):
        self.textbox = tkinter.Text(
            parent,
            font=(config.messagefont, config.messagefontsize, 'normal'),
            background="black"
        )
        self.textbox.config(state="disabled")
        gui.lib.setup_scrollbars(parent, self.textbox)
        self._configcolors()

    def write(self, msg):
        self.textbox.config(state="normal")
        self.textbox.insert("end", str(msg) + "\n", str(msg.level))
        self.textbox.config(state="disabled")
        self.textbox.yview("end")

    def _configcolors(self):
        self.textbox.tag_config(str(Level.debug), foreground="grey")
        self.textbox.tag_config(str(Level.info), foreground="lightgrey")
        self.textbox.tag_config(str(Level.warning), foreground="orange")
        self.textbox.tag_config(str(Level.error), foreground="orangered")


class Level(enum.Enum):
    invalid = 0
    debug   = 1
    info    = 2
    warning = 3
    error   = 4


class Message:
    def __init__(self, msglevel, *args, sep=" "):
        self.level = msglevel
        self.parts = args
        self.separator = sep

    def __str__(self):
        return self.separator.join(self.parts)


def init(parent):
    global _handler
    _handler = MessageHandler(parent)


def debug(*args, sep=" "):
    if config.debug:
        _handler.write(Message(Level.debug, *args, sep=sep))


def info(*args, sep=" "):
    _handler.write(Message(Level.info, *args, sep=sep))


def warn(*args, sep=" "):
    _handler.write(Message(Level.warning, *args, sep=sep))


def error(*args, sep=" "):
    _handler.write(Message(Level.error, *args, sep=sep))
