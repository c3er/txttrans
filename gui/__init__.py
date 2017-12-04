#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import traceback

import tkinter
import tkinter.ttk as ttk

import gui.base
import message
import misc

import config


TRANSFORMER_FILE = "transformers.py"
FKEY_COUNT = 12


_root = None
_maintext = None


transformers = []


# Stolen from some demos #######################################################

class _DialogBase(tkinter.Toplevel):
    def __init__(self, parent, title = None):
        """Must be called after initialization of inheriting classes."""

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


class TransformData:
    def __init__(self, label, handler):
        self.label = label
        self.handler = handler


class transformer:
    def __init__(self, label):
        self.label = label

    def __call__(self, func):
        transformers.append(TransformData(self.label, func))
        return func


# Helpers ######################################################################

class MainWindow(tkinter.Tk):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.unbind_all("<F10>")

        self.transfomer_file = os.path.join(misc.getstarterdir(), TRANSFORMER_FILE)
        self.oldcode = None
        self.menubar = None
        self.mainmenu = None
        self.popup = None
        self.update_transformers()

    def report_callback_exception(self, exc, val, tb):
        msg = traceback.format_exception(exc, val, tb)
        message.error("Exception occured:", ''.join(msg))

    def update_transformers(self):
        global transformers
        try:
            with open(self.transfomer_file, encoding="utf8") as f:
                codestr = f.read()

            if codestr != self.oldcode:
                message.debug("Update transformers...")
                self.oldcode = codestr

                code = compile(codestr, self.transfomer_file, "exec")
                transformers = []
                self.namespace = globals().copy()
                exec(code, self.namespace)

                self._update_ui(transformers)
                message.debug("Transformers updated")
        finally:
            self.after(1000, self.update_transformers)

    def _update_ui(self, transformers):
        if self.mainmenu:
            self.mainmenu.destroy()
        if self.popup:
            self.popup.destroy()

        if not self.menubar:
            self.menubar = gui.menu.Menu(self)
        self.mainmenu = self.menubar.add_submenu("Transformers")
        self.popup = gui.menu.Popup(self)

        for i, t in enumerate(transformers):
            label = t.label
            handler = lambda event=None, t=t, n=self.namespace: self._handle_transformer(t, n)
            keystring = self._get_keystring(i)
            if keystring:
                self.bind("<{}>".format(keystring), handler)
            self.mainmenu.add_item(label, handler, accelerator=keystring)
            self.popup.add_entry(label, handler, keystring)
            
        self.bind('<Button-3>', self.popup.display)

    @staticmethod
    def _handle_transformer(t, namespace):
        try:
            message.info(f'Call transfomer "{t.label}"')
            handler = t.handler
            def wrapper():
                return handler(_maintext.get())
            namespace[wrapper.__name__] = wrapper
            text = eval(f"{wrapper.__name__}()", namespace)
            if text:
                _maintext.clipboard = text
                _maintext.set(text)
        finally:
            _maintext.set_focus()

    @staticmethod
    def _get_keystring(i):
        if i < FKEY_COUNT:
            return "F" + str(i + 1)
        elif i < FKEY_COUNT * 2:
            return "Control-F" + str((i % FKEY_COUNT) + 1)
        elif i < FKEY_COUNT * 3:
            return "Shift-F" + str((i % FKEY_COUNT) + 1)
        elif i < FKEY_COUNT * 4:
            return "Control-Shift-F" + str((i % FKEY_COUNT) + 1)
        else:
            return None


class MainText:
    MAX_CHARACTERS = 100000

    def __init__(self, parent):
        self.textbox = tkinter.Text(
            parent,
            font=(config.font, config.fontsize, 'normal')
        )
        gui.base.setup_scrollbars(parent, self.textbox)
        self.textbox.focus_set()

        self.text_is_too_big = False
        self.too_big_text = ""

    @property
    def clipboard(self):
        return self.textbox.selection_get(selection='CLIPBOARD')

    @clipboard.setter
    def clipboard(self, text):
        self.textbox.clipboard_clear()
        self.textbox.clipboard_append(text)

    def get(self):
        if self.text_is_too_big:
            return self.too_big_text.strip()
        return self.textbox.get("1.0", "end").strip()

    def set(self, text):
        self.textbox.delete("1.0", "end")
        if len(text) < self.MAX_CHARACTERS:
            self.textbox.insert("1.0", text)
            self.text_is_too_big = False
        else:
            self.too_big_text = text
            self.text_is_too_big = True
            msg = "Desired text is too big to display. But it is remembered and in the clipboard."
            self.textbox.insert("1.0", msg)

    def set_focus(self):
        self.textbox.focus_set()


class DataEntry:
    def __init__(self, label, default="", validator=lambda value: True):
        self.label = label
        self.default = default
        self.validator = validator
        self.widget = None

    @property
    def value(self):
        return self.widget.get()

    def validate(self):
        return self.validator(self.value)


class SimpleDataDialog(_DialogBase):
    ENTRYWIDTH = 80

    def __init__(self, title, *entries):
        firstentry = entries[0]
        self.entries = firstentry if len(entries) == 1 and misc.islistlike(firstentry) else entries
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
                message.warn('Validation failed on entry "{}"'.format(entry.label))
            succeeded = succeeded and entrysuccess
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


def init_maintext(parent):
    global _maintext
    global _root
    _root = parent
    _maintext = MainText(parent)

################################################################################
