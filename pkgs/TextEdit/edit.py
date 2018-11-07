"""
TextEdit
Eric Diskin
2018
"""

"""Requires:
    pynput - pip install pynput"""

import json
import os
import sys
import tkinter as tk
from tkinter import filedialog


VERSION = '0.2.5.0'


class Editor(object):

    def __init__(self, root, path=None):
        self.root = root
        self.ALL = {
            'open_file': self.open_file,
            'save_file': self.save_file,
            'exit': self.root.destroy,
            'font_size_add': self.size_add,
            'font_size_sub': self.size_sub
        }

        if path != None:
            self.path = path
            if self.txtArea == None:
                self.loadUI()
            self.txtArea.insert('1.0', self.get_text())
        else:
            self.open_file()

        self.loadMenu(json.loads(open(PATH + 'menus.json').read()))

    txtArea = None
    fontsize = 11

    def get_text(self, evt=None):
        with open(self.path) as file:
            text = file.read()
            return text

    def set_word_wrap(self, val):
        self.txtArea.config(wrap=val)

    def size_add(self, evt=None):
        self.fontsize += 2
        self.txtArea.config(font=("Courier", self.fontsize))

    def size_sub(self, evt=None):
        self.fontsize -= 2
        self.txtArea.config(font=("Courier", self.fontsize))

    def loadUI(self):
            self.title = 'TextEdit - ' + os.path.split(self.path)[1]
            self.root.title()
            self.txtArea = tk.Text(self.root)
            self.txtArea.insert(tk.END, self.get_text())
            self.txtArea.pack(expand=1, fill='both')
            self.txtArea.focus_force()

    def open_file(self, types=(('All Files', '*.*'))):
        """Open a file dialog and select a file.
        returns the file path."""
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        root.destroy()
        self.path = path
        if self.txtArea == None:
            self.loadUI()

        self.txtArea.insert('1.0', self.get_text())

    def save_file(self, evt=None):
        with open(self.path, 'w') as file:
            file.write(self.txtArea.get('1.0', tk.END))
            self.root.title(self.title)

    def loadMenu(self, arr, root=False):
        if root == False:
            menu = tk.Menu(root)
            root = self.root
            root.config(menu=menu)

        else:
            menu = tk.Menu(root)

        for obj in arr:
            if obj['type'] == 'seperator':
                menu.add_separator()
                continue
            elif obj['type'] == 'comment':
                continue

            name = obj['name']

            if obj['type'] == 'cmd':
                func = self.ALL[obj['cmd']]
                if 'keys' in obj:
                    keys = obj['keys']
                    self.root.bind(keys, func)

                else:
                    keys = None

                menu.add_command(label=name, command=func, accelerator=keys)

            elif obj['type'] == 'dropdown':
                    nmen = self.loadMenu(obj['drop'], menu)
                    menu.add_cascade(label=obj['name'], menu=nmen)

        return menu

    def __str__(self):
        return self.txtArea.get('1.0', tk.END)


def main():

    root = tk.Tk()
    path = None

    if len(command.split()) > 1:
        path = command[9:]

    with open(PATH + 'menus.json') as JSON:
        tedit = Editor(root, path)
        tedit.loadMenu(json.loads(JSON.read()))

    root.mainloop()
