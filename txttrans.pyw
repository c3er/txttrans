#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import types
import traceback
import tkinter
import tkinter.ttk as ttk


ERRORWINDOW_SIZE = "800x600"


# Taken from the Python repository at https://github.com/python/cpython.git
# Commit ID 800415e3df69f494afe9f95a8563ce17609fe1da
if sys.platform == 'win32':
    import ctypes
    try:
        ctypes.OleDLL('shcore').SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


class ErrorHandler:
    def __init__(self, parent, tb):
        self.textbox = tkinter.Text(
            parent,
            font=("Consolas", 10, 'normal'),
            background="black",
            foreground="orange")
        setup_scrollbars(parent, self.textbox)

        self.textbox.insert("end", tb)

        self.textbox.config(state="disabled")
        self.textbox.yview("end")


def setup_scrollbars(container, widget):
    vsb = ttk.Scrollbar(container, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)

    widget.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns')

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)


def message_area(parent, msg):
    frame = ttk.Frame(parent)
    ErrorHandler(frame, msg)
    return frame


def main():
    try:
        import main
        main.main()
    except:
        error = traceback.format_exc()

        try:
            import main
        except:
            pass
        else:
            if hasattr(main, "cleanup") and isinstance(main.cleanup, types.FunctionType):
                try:
                    main.cleanup()
                except:
                    error = traceback.format_exc()

        root = tkinter.Tk()
        root.wm_title("Error")
        root.geometry(ERRORWINDOW_SIZE)
        message_area(root, error).pack(fill="both", expand=True)
        root.mainloop()
        raise


if __name__ == "__main__":
    main()
