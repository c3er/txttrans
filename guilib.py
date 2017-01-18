#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.ttk as ttk


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


def setup_scrollbars(container, widget):
    vsb = AutoScrollbar(container, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)

    widget.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns')

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)