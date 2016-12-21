#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.ttk as ttk

import gui
import message
import transformers

from misc import curry


WINDOW_SIZE = "800x700"


# GUI initialization ###########################################################

def toolbar(parent):
    frame = ttk.Frame(parent)
    for i, t in enumerate(gui.transformers):
        fkey_str = "F" + str(i + 1)
        label = "[{}] {}".format(fkey_str, t.label)
        parent.bind("<{}>".format(fkey_str), t.handler)
        gui.create_button(frame, label, t.handler)
    return frame


def main_area(parent):
    global _textbox
    frame = ttk.Frame(parent)
    _textbox = gui.init_textbox(frame)
    return frame

################################################################################


def appclose_callback(root):
    message.info("Quitting")
    root.destroy()


def main():
    root = gui.App()
    root.wm_title("Text Transformator")
    root.geometry(WINDOW_SIZE)
    root.bind("<Alt-F4>", lambda event: appclose_callback(root))
    root.protocol('WM_DELETE_WINDOW', curry(appclose_callback, root))

    toolbar(root).pack(anchor="n", fill="x")
    main_area(root).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()
