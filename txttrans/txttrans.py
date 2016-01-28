#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tkinter
import tkinter.ttk as ttk


def toolbar(parent):
    pass


def main_area(parent):
    pass


def init_gui():
    root = tkinter.Tk()
    root.wm_title("Text Transformator")
    return root


def main(args):
    root = init_gui()
    root.mainloop()

if __name__ == "__main__":
    main(sys.argv)
