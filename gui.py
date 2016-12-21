#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter
import tkinter.ttk as ttk

import misc


_root = None
_maintext = None


transformers = []


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


class _DialogBase(tkinter.Toplevel):
    def __init__(self, parent, title = None):
        'Must be called after initialization of inheriting classes.'

        super().__init__(parent)

        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.canceled = False
        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+{}+{}".format(
            parent.winfo_rootx() + 50,
            parent.winfo_rooty() + 50)
        )
        self.initial_focus.focus_set()
        self.wait_window(self)

    def close(self, event = None):
        """Give focus back to the parent window and close the dialog."""
        self.parent.focus_set()
        self.destroy()

    # Methods to overwrite #####################################################
    def body(self, master):
        """Create dialog
        Returns a widget, which should have the focus immediatly. This method
        should be overwritten.
        """
        pass

    def buttonbox(self):
        """Add standard button box
        Overwrite, if there are no standard buttons wanted.
        """
        box = ttk.Frame(self)

        ttk.Button(
            box,
            text="Cancel",
            width=10,
            command=self.cancel
        ).pack(side='right', padx=5, pady=5)

        ttk.Button(
            box,
            text="OK",
            width=10,
            command=self.ok,
            default=tkinter.ACTIVE
        ).pack(side='right', padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)
        box.pack(fill='x')

    # Standard button behavior ###
    def ok(self, event = None):
        """Execute the validate function and if it returns False, it will just
        set the focus right and return.
        If validate returns True, then the apply function will be called and the
        dialog will be closed.
        """
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.close()

    def cancel(self, event = None):
        """Performs an Abortion of the dialog."""
        self.canceled = True
        self.close(event)
    ###

    # Command hooks ###
    def validate(self):
        """Overwrite.
        Validate the input. If the function returns false, the dialog will stay
        open.
        """
        return True

    def apply(self):
        """Overwrite.
        Process the input. This function will be called, after the dialog was
        closed.
        """
        pass
    ###
    ############################################################################

################################################################################


class Transformer:
    def __init__(self, label, handler):
        self.label = label
        self.handler = handler


class transform_handler:
    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        def wrapper(event=None):
            try:
                text = func(_maintext.get())
                if text is None:
                    raise Exception("Transform handler '{}' returned 'None'.".format(func.__name__))
                _maintext.clipboard = text
                _maintext.set(text)
            finally:
                _maintext.set_focus()
        transformers.append(Transformer(self.label, wrapper))
        return wrapper


# Helpers ######################################################################

class MainText:
    def __init__(self, parent):
        self.textbox = tkinter.Text(parent)
        setup_scrollbars(parent, self.textbox)
        self.textbox.focus_set()

    @property
    def clipboard(self):
        raise NotImplementedError()

    @clipboard.setter
    def clipboard(self, text):
        self.textbox.clipboard_clear()
        self.textbox.clipboard_append(text)

    def get(self):
        return self.textbox.get("1.0", "end").strip()

    def set(self, text):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)

    def set_focus(self):
        self.textbox.focus_set()


def create_button(parent, label, command):
    button = ttk.Button(parent, text=label, command=command)
    button.pack(side='left')
    return button


def setup_scrollbars(container, widget):
    vsb = AutoScrollbar(container, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)

    widget.grid(column=0, row=0, sticky='nsew', in_=container)
    vsb.grid(column=1, row=0, sticky='ns')

    container.grid_columnconfigure(0, weight=1)
    container.grid_rowconfigure(0, weight=1)


class DataEntry:
    def __init__(self, label, default="", validator=None):
        def dummy_validator(value):
            return True
        self.label = label
        self.validator = validator if validator else dummy_validator
        self.widget = None
        self.default = default

    @property
    def value(self):
        return self.widget.get()

    def validate(self):
        return self.validator(self.value)


class SimpleDataDialog(_DialogBase):
    ENTRYWIDTH = 80

    def __init__(self, title, entries):
        self.entries = entries
        super().__init__(_root, title)

    def body(self, master):
        frame = ttk.Frame(self)
        entrywidgets = [self._labeled_entry(frame, entry.label, entry.default) for entry in self.entries]
        for entry, widget in zip(self.entries, entrywidgets):
            entry.widget = widget
        frame.pack(side='top', padx=2, pady=2, fill='x')
        return entrywidgets[0]

    def validate(self):
        succeeded = True
        for entry in self.entries:
            entrysuccess = entry.validate()
            if not entrysuccess:
                print('Validation failed on entry "{}"'.format(entry.label))
            succeeded = entrysuccess and succeeded
        return succeeded

    def apply(self):
        self.result = {}
        for entry in self.entries:
            self.result[entry.label] = entry.value

    def _labeled_entry(self, parent, label, default):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text=label).pack(side='top', anchor='w')
        entry = ttk.Entry(frame, width=self.ENTRYWIDTH)
        entry.pack(side='top', fill='x')
        frame.pack(side='top', padx=2, pady=2, fill='x')
        self._setentry(entry, default)
        return entry

    @staticmethod
    def _setentry(entry, text):
        entry.delete(0, 'end')
        entry.insert(0, text)


def init_textbox(parent):
    global _maintext
    global _root
    _root = parent
    _maintext = MainText(parent)

################################################################################
