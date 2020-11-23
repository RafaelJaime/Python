import tkinter as tk
from tkinter import ttk
from tkinter import * 

import time

def funcion():
    root.withdraw()
    time.sleep(5)
    root.deiconify()

root = tk.Tk()
boton = tk.Button(root, text="Probando el metodo withdraw", command=funcion)
boton.pack()
root.mainloop()
