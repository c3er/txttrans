#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import pickle
import tkinter

import misc


DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600

STATE_PATH = os.path.join(misc.getstarterdir(), "state.dat")


class State:
    def __init__(self, **kw):
        for attr, val in kw.items():
            setattr(self, attr, val)

    def save(self):
        with open(STATE_PATH, "wb") as f:
            pickle.dump(self, f)


_dummy = tkinter.Tk()
_dummy.attributes("-alpha", 0)

_x = _dummy.winfo_screenwidth() // 2 - DEFAULT_WIDTH // 2
_y = _dummy.winfo_screenheight() // 2 - DEFAULT_HEIGHT // 2

_dummy.destroy()

_default_state = State(window_geometry=f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}+{_x}+{_y}")


def load():
    try:
        with open(STATE_PATH, "rb") as f:
            return pickle.load(f)
    except (OSError, pickle.UnpicklingError):
        return _default_state
