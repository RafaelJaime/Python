import tkinter as tk
from tkinter import ttk
from tkinter import * 
import time

def funcion():
    root.state(newstate='withdraw')
    time.sleep(5)
    root.state(newstate='normal')

root = tk.Tk()
boton = tk.Button(root, text="Probando el metodo state", command=funcion)
boton.pack()
root.mainloop()