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
            font=(config.messagefont, config.messagefontsize, 'normal')
        )
        self.textbox.config(state="disabled")
        gui.lib.setup_scrollbars(parent, self.textbox)

    def write(self, msg):
        self.textbox.config(state="normal")
        self.textbox.insert("end", str(msg) + "\n")
        self.textbox.config(state="disabled")
        self.textbox.yview("end")


class Level(enum.Enum):
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
    _handler.write(Message(Level.info, *args, sep=sep))


def warn(*args, sep=" "):
    _handler.write(Message(Level.warning, *args, sep=sep))


def error(*args, sep=" "):
    _handler.write(Message(Level.error, *args, sep=sep))
