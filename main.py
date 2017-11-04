#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
import tkinter.ttk as ttk

import gui
import gui.base
import gui.menu

import message
import transformers

from misc import curry


MAINWINDOW_SIZE = "800x700"
FKEY_COUNT = 12


_root = None


# GUI initialization ###########################################################

def create_menus(parent):
    menubar = gui.menu.Menu(parent)
    mainmenu = menubar.add_submenu("Transform handlers")

    popup = gui.menu.Popup(parent)

    for i, t in enumerate(gui.transformers):
        label = t.label
        handler = t.handler

        if i < FKEY_COUNT:
            keystring = "F" + str(i + 1)
        elif i < FKEY_COUNT * 2:
            keystring = "Control-F" + str((i % FKEY_COUNT) + 1)
        elif i < FKEY_COUNT * 3:
            keystring = "Shift-F" + str((i % FKEY_COUNT) + 1)
        elif i < FKEY_COUNT * 4:
            keystring = "Control-Shift-F" + str((i % FKEY_COUNT) + 1)
        else:
            keystring = None

        if keystring:
            parent.bind("<{}>".format(keystring), handler)
        mainmenu.add_item(label, handler, accelerator=keystring)
        popup.add_entry(label, handler, keystring)
        
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

    root.wm_title("Text Transformer")
    root.geometry(MAINWINDOW_SIZE)
    root.bind("<Alt-F4>", lambda event: close_app(root))
    root.protocol('WM_DELETE_WINDOW', curry(close_app, root))

    create_menus(root)

    pw = tkinter.PanedWindow(root, orient="vertical")
    pw.pack(fill="both", expand=True)
    pw.add(main_area(root), minsize=500)
    pw.add(message_area(root), minsize=100)

    message.debug("Initialized")
    message.info("Initialized")
    message.warn("Initialized")
    message.error("Initialized")

    root.mainloop()


if __name__ == "__main__":
    main()
