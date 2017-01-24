#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

import gui
import gui.lib
import gui.menu

import message
import transformers

from misc import curry


MAINWINDOW_SIZE = "800x700"


# GUI initialization #######################################################

def toolbar(parent):
    frame = ttk.Frame(parent)
    for i, t in enumerate(gui.transformers):
        fkey_str = "F" + str(i + 1)
        label = "[{}] {}".format(fkey_str, t.label)
        parent.bind("<{}>".format(fkey_str), t.handler)
        gui.create_button(frame, label, t.handler)
    return frame


def menubar(parent):
    mainmenu = gui.menu.Menu(parent)
    menu = mainmenu.add_submenu("Transform handlers")
    for i, t in enumerate(gui.transformers):
        fkey_str = "F" + str(i + 1)
        parent.bind("<{}>".format(fkey_str), t.handler)
        menu.add_item(t.label, t.handler, accelerator=fkey_str)


def main_area(parent):
    frame = ttk.Frame(parent)
    gui.init_maintext(frame)
    return frame


def message_area(parent):
    frame = ttk.Frame(parent)
    message.init(frame)
    return frame

############################################################################


def close_app(root):
    message.info("Quitting")
    root.destroy()


def main():
    root = gui.MainWindow()
    root.wm_title("Text Transformator")
    root.geometry(MAINWINDOW_SIZE)
    root.bind("<Alt-F4>", lambda event: close_app(root))
    root.protocol('WM_DELETE_WINDOW', curry(close_app, root))

    menubar(root)
    #toolbar(root).pack(anchor="n", fill="x")
    main_area(root).pack(fill="both", expand=True)
    message_area(root).pack(fill="both", expand=True)

    message.info("Initialized")

    root.mainloop()


if __name__ == "__main__":
    main()
