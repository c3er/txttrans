#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.ttk as ttk


_maintext = None


transformers = []

        
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


class Transformer:
    def __init__(self, label, handler):
        self.label = label
        self.handler = handler


class transform_handler:
    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        def wrapper(event=None):
            try:
                text = func(_maintext.get())
                if text is None:
                    raise Exception("Transform handler '{}' returned 'None'.".format(func.__name__))
                _maintext.clipboard = text
                _maintext.set(text)
            finally:
                _maintext.set_focus()
        transformers.append(Transformer(self.label, wrapper))
        return wrapper
    

# Helpers ######################################################################

class MainText:
    def __init__(self, parent):
        self.textbox = tkinter.Text(parent)
        setup_scrollbars(parent, self.textbox)
        self.textbox.focus_set()

    @property
    def clipboard(self):
        raise NotImplementedError()

    @clipboard.setter
    def clipboard(self, text):
        self.textbox.clipboard_clear()
        self.textbox.clipboard_append(text)

    def get(self):
        return self.textbox.get("1.0", "end").strip()

    def set(self, text):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)

    def set_focus(self):
        self.textbox.focus_set()


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
    global _maintext
    _maintext = MainText(parent)

################################################################################


