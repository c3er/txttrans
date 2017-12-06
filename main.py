#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.ttk as ttk

import gui
import message


MAINWINDOW_SIZE = "800x700"


_root = None


# GUI initialization ###########################################################

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


def close_app():
    message.info("Quitting")
    cleanup()


def main():
    global _root
    _root = root = gui.MainWindow()
    root.update_transformers()

    root.wm_title("Text Transformer")
    root.geometry(MAINWINDOW_SIZE)
    root.bind("<Alt-F4>", lambda event: close_app())
    root.protocol('WM_DELETE_WINDOW', close_app)

    pw = ttk.PanedWindow(root, orient="vertical")
    pw.pack(fill="both", expand=True)
    pw.add(main_area(pw), weight=100)
    pw.add(message_area(pw), weight=1)

    message.debug("Initialized")
    message.info("Initialized")
    message.warn("Initialized")
    message.error("Initialized")

    root.mainloop()


if __name__ == "__main__":
    main()
