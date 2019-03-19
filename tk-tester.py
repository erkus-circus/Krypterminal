import krypt
from krypt import commands as c
import tkinter as tk


def execl():
    krypt.execCmd('open tests.txt')

if __name__ == "__main__":
    root = tk.Tk()
    root.title('KryptoTests')
    btn = tk.Button(root, text='Exec command', command=execl)
    btn.pack()
    root.mainloop()