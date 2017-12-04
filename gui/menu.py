#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter

from misc import curry


class Menu:
    """Wrapper class over the tkinter.Menu class to add features.
    These features are:
    - A nice tree structure to navigate through.
    - The possibility to get every item as variable.
    """
    def __init__(self, tkparent):
        self.children = []
        
        # XXX...
        if not isinstance(self, SubMenu):
            tkparent.option_add('*tearOff', False)
            
        self.tkmenu = tkinter.Menu(tkparent)
        
        # ... not pretty
        if not isinstance(self, SubMenu):
            tkparent.config(menu=self.tkmenu)
            
        self.tkparent = tkparent
        self.label = None
    
    def add_submenu(self, label):
        submenu = SubMenu(label, self, self.tkmenu)
        self.tkmenu.add_cascade(label=label, menu=submenu.tkmenu)
        self.children.append(submenu)
        return submenu
    
    def add_item(self, label, command, *args, **kw):
        item = MenuItem(self, label, command)
        self.tkmenu.add_command(*args, label=label, command=command, **kw)
        self.children.append(item)
        return item
    
    def add_seperator(self):
        self.tkmenu.add_separator()
    

class SubMenu(Menu):
    def __init__(self, label, parent, *args, **kw):
        super().__init__(*args, **kw)
        self.parent = parent
        self.label = label

    def destroy(self):
        self.parent.tkmenu.delete(self.label)
    

class MenuItem:
    def __init__(self, parent, label, command):
        self.parent = parent
        self.label = label
        self.command = command

        
class Popup:
    """Also called "context menu". A menu that shall appear at the location of
    the mouse pointer.
    """
    def __init__(self, frame):
        self.menu = tkinter.Menu(frame, tearoff=0)
        self.lastevent = None
        self.handlers = {}
        
    def dispatch(self, label):
        """Calls the handler.
        The event that is given to the handler is the appearance of the menu
        and not the actual call of the menu item.
        """
        self.handlers[label](self.lastevent)
    
    def display(self, event):
        """The handler, which shall be bound to the right mouse button.
        (TK name: <Button-3>)
        """
        event.widget.focus_set()
        try:
            self.menu.post(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
        self.lastevent = event
    
    def add_entry(self, label, handler, accelerator=None):
        self.handlers[label] = handler
        self.menu.add_command(
            label=label,
            command=curry(self.dispatch, label),
            accelerator=accelerator
        )
    
    def add_seperator(self):
        self.menu.add_separator()

    def destroy(self):
        self.menu.destroy()
