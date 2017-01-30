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


_root = None


# GUI initialization ###########################################################

def create_menus(parent):
    menubar = gui.menu.Menu(parent)
    mainmenu = menubar.add_submenu("Transform handlers")

    popup = gui.menu.Popup(parent)

    for i, t in enumerate(gui.transformers):
        fkey_str = "F" + str(i + 1)
        label = t.label
        handler = t.handler
        parent.bind("<{}>".format(fkey_str), handler)
        mainmenu.add_item(label, handler, accelerator=fkey_str)
        popup.add_entry(label, handler, fkey_str)
        
    parent.bind('<Button-3>', popup.display)

def main_area(parent):
    frame = ttk.Frame(parent)
    gui.init_maintext(frame)
    return frame


def message_area(parent):
    frame = ttk.Frame(parent)
    message.init(frame)
    return frame

################################################################################

def cleanup():
    if _root:
        _root.destroy()


def close_app(root):
    message.info("Quitting")
    cleanup()


def main():
    global _root
    _root = root = gui.MainWindow()

    root.wm_title("Text Transformator")
    root.geometry(MAINWINDOW_SIZE)
    root.bind("<Alt-F4>", lambda event: close_app(root))
    root.protocol('WM_DELETE_WINDOW', curry(close_app, root))

    create_menus(root)
    main_area(root).pack(fill="both", expand=True)
    message_area(root).pack(fill="both")

    message.debug("Initialized")
    message.info("Initialized")
    message.warn("Initialized")
    message.error("Initialized")

    root.mainloop()


if __name__ == "__main__":
    main()
