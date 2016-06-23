#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.messagebox
import tkinter.ttk as ttk


WINDOW_SIZE = "800x700"


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
            try:
                text = func(get_text())
                if text is None:
                    raise Exception("Transform handler '{}' returned 'None'.".format(func.__name__))
                _textbox.clipboard_clear()
                _textbox.clipboard_append(text)
                set_text(text)
            finally:
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


@transform_handler("Beatify JSON")
def beautify_json(text):
    import json
    import collections
    obj = json.loads(text, object_pairs_hook=collections.OrderedDict)
    return json.dumps(obj, indent=4, separators=(",", ": "))


@transform_handler("Beautify XML")
def beautify_xml(text):
    import xmllib
    return str(xmllib.str2xml(text))

################################################################################


# GUI initialization ###########################################################
def toolbar(parent):
    frame = ttk.Frame(parent)
    for i, t in enumerate(_transformers):
        fkey_str = "F" + str(i + 1)
        label = "[{}] {}".format(fkey_str, t.label)
        parent.bind("<{}>".format(fkey_str), t.handler)
        create_button(frame, label, t.handler)
    return frame


def main_area(parent):
    global _textbox
    frame = ttk.Frame(parent)
    _textbox = init_textbox(frame)
    return frame


def init_gui():
    root = tkinter.Tk()
    root.wm_title("Text Transformator")
    root.geometry(WINDOW_SIZE)

    toolbar(root).pack(anchor="n", fill="x")
    main_area(root).pack(fill="both", expand=True)

    return root

################################################################################

def main():
    root = init_gui()
    root.mainloop()


if __name__ == "__main__":
    main()
