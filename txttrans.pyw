#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    import tkinter
    import tkinter.ttk as ttk

    import gui
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

        toolbar(root).pack(anchor="n", fill="x")
        main_area(root).pack(fill="both", expand=True)
        message_area(root).pack(fill="both", expand=True)

        message.info("Initialized")
        
        root.mainloop()


    if __name__ == "__main__":
        main()


except:
    # XXX Not all errors are catched by this, e.g. IndentationError.
    # If errors are not catched by this, it will just not start and does not display any messages.

    if __name__ != "__main__":
        raise

    import tkinter
    import traceback

    # XXX Errors in this module my lead the message window to be not displayed
    # (starting will fail silently)
    import message

    ERRORWINDOW_SIZE = "800x600"

    def message_area(parent):
        frame = ttk.Frame(parent)
        message.init(frame)
        return frame

    def errorwindow():
        root = tkinter.Tk()
        root.wm_title("Error")
        root.geometry(ERRORWINDOW_SIZE)
        message_area(root).pack(fill="both", expand=True)
        message.error(traceback.format_exc())
        root.mainloop()

    errorwindow()
    raise
