#!/usr/bin/env python
# -*- coding: utf-8 -*-


import types
import traceback
import tkinter
import tkinter.ttk as ttk


ERRORWINDOW_SIZE = "800x600"


class ErrorData:
    def __init__(self):
        self.errors = []

    def __str__(self):
        errors = []
        for stored_error in reversed(self.errors):
            if not any(
                    stored_error.strip() in error.strip() or error.strip() in stored_error.strip()
                    for error in errors):
                errors.insert(0, stored_error)
        return "\n\n".join(errors)

    def add(self):
        self.errors.append(traceback.format_exc())


class ErrorHandler:
    def __init__(self, parent, tb):
        self.textbox = tkinter.Text(
            parent,
            font=("Consolas", 10, 'normal'),
            background="black",
            foreground="orange"
        )
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
    errors = ErrorData()
    try:
        import main
        main.main()
    except:
        errors.add()
        
        try:
            import main
        except:
            pass
        else:
            if hasattr(main, "cleanup") and isinstance(main.cleanup, types.FunctionType):
                try:
                    main.cleanup()
                except:
                    errors.add()

        root = tkinter.Tk()
        root.wm_title("Error")
        root.geometry(ERRORWINDOW_SIZE)
        message_area(root, str(errors)).pack(fill="both", expand=True)
        root.mainloop()
        raise


if __name__ == "__main__":
    main()
