#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter


class Menu:
    """Wrapper class over the tkinter.Menu class to add needed features
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
        
        # ... ugly!
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
    

class MenuItem:
    def __init__(self, parent, label, command):
        self.parent = parent
        self.label = label
        self.command = command
