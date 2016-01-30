#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk


_textbox = None
_transformers = []


# Helpers #####################################################################

class Transformer:
    def __init__(self, label, handler):
        self.label = label
        self.handler = handler


class transform_handler:
    def __init__(self, label):
        """If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.label = label

    def __call__(self, func):
        """If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give it
        a single argument, which is the function object.
        """
        def wrapper(event=None):
            text = get_text()
            text = func(text)
            set_text(text)
        t = Transformer(self.label, wrapper)
        _transformers.append(t)
        return wrapper


def get_text():
    return _textbox.get("1.0", "end")


def set_text(text):
    _textbox.delete("1.0", "end")
    _textbox.insert("1.0", text)


def create_button(parent, label, command):
    button = ttk.Button(parent, text=label, command=command)
    button.pack(side='left')
    return button

###############################################################################


# Handlers ####################################################################

@transform_handler("Hello")
def say_hello(text):
    return "Hello, world!"

###############################################################################


# GUI initialization ##########################################################

def toolbar(parent):
    frame = ttk.Frame(parent)
    for t in _transformers:
        create_button(frame, t.label, t.handler)
    return frame


def main_area(parent):
    global _textbox

    frame = ttk.Frame(parent)

    _textbox = tkinter.Text(frame)
    _textbox.pack(fill="both")

    return frame


def init_gui():
    root = tkinter.Tk()
    root.wm_title("Text Transformator")

    toolbar(root).pack(anchor="n", fill="x")
    main_area(root).pack(fill="both")

    return root

###############################################################################


def main(args):
    root = init_gui()
    root.mainloop()

if __name__ == "__main__":
    main(sys.argv)
