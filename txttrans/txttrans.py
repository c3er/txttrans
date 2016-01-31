#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk


_textbox = None
_transformers = []
        
# Stolen from some demos #######################################################

class AutoScrollbar(ttk.Scrollbar):
    """A scrollbar that hides it self if it's not needed.
    Only works if you use the grid geometry manager.
    """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        super().set(lo, hi)
        
    def pack(self, **kw):
        raise tkinter.TclError("Can not use pack with this widget")
    
    def place(self, **kw):
        raise tkinter.TclError("Can not use place with this widget")

################################################################################


# Helpers ######################################################################

class Transformer:
    def __init__(self, label, handler):
        self.label = label
        self.handler = handler


class transform_handler:
    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        def wrapper(event=None):
            text = get_text()
            text = func(text)
            set_text(text)
            _textbox.focus_set()
        _transformers.append(Transformer(self.label, wrapper))
        return wrapper


def get_text():
    return _textbox.get("1.0", "end").strip()


def set_text(text):
    _textbox.delete("1.0", "end")
    _textbox.insert("1.0", text)


def create_button(parent, label, command):
    button = ttk.Button(parent, text=label, command=command)
    button.pack(side='left')
    return button

                
def setup_scrollbars(container, widget):
    vsb = AutoScrollbar(container, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)

    widget.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns')
    
    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)


def init_textbox(parent):
    textbox = tkinter.Text(parent)
    setup_scrollbars(parent, textbox)
    textbox.focus_set()
    return textbox

################################################################################


# Handlers #####################################################################

@transform_handler("Help")
def help(text):
    return "XXX Write help text."

@transform_handler("Hello")
def say_hello(text):
    return "Hello, world!"

@transform_handler("To upper")
def toupper(text):
    return text.upper()

################################################################################


# GUI initialization ###########################################################

def toolbar(parent):
    frame = ttk.Frame(parent)
    for t in _transformers:
        create_button(frame, t.label, t.handler)
    return frame


def main_area(parent):
    global _textbox
    frame = ttk.Frame(parent)
    _textbox = init_textbox(frame)
    return frame


def init_gui():
    root = tkinter.Tk()
    root.wm_title("Text Transformator")

    toolbar(root).pack(anchor="n", fill="x")
    main_area(root).pack(fill="both", expand=True)

    return root

################################################################################


def main(args):
    root = init_gui()
    root.mainloop()

if __name__ == "__main__":
    main(sys.argv)
