#!/usr/bin/env python
# -*- coding: utf-8 -*-


import traceback
import tkinter
import tkinter.ttk as ttk


ERRORWINDOW_SIZE = "800x600"


class ErrorHandler:
    def __init__(self, parent, tb):
        self.textbox = tkinter.Text(parent)
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


def message_area(parent, tb):
    frame = ttk.Frame(parent)
    ErrorHandler(frame, tb)
    return frame


def main():
    try:
        import main
        main.main()
    except:
        tb = traceback.format_exc()
        root = tkinter.Tk()
        root.wm_title("Error")
        root.geometry(ERRORWINDOW_SIZE)
        message_area(root, tb).pack(fill="both", expand=True)
        root.mainloop()


if __name__ == "__main__":
    main()
