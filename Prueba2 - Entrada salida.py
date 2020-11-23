import tkinter as tk
from tkinter import ttk
from tkinter import * 

def funcion():
    otra_ventana.state(newstate="withdraw")
    root.state(newstate="normal")

root = tk.Tk()
otra_ventana = tk.Toplevel(root)
otra_ventana.title("Ventana hija")
otra_ventana.state(newstate="withdraw")
tk.Button(otra_ventana, text="Probando el metodo withdraw", command=funcion).place(x=10, y=0)

# this is the function called when the button is clicked
def btnClickFunction():
    print('clicked')
    root.state(newstate="withdraw")
    otra_ventana.state(newstate="normal")

root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='./image/computer.ico'))

# This is the section of code which creates the main window
root.geometry('411x330')
root.configure(background='#FFFAFA')
root.title('Primera ventana')


# This is the section of code which creates the a label
Label(root, text='cuando pulses en el botón aparecerá un texto', bg='#FFFAFA', font=('arial', 12, 'normal')).place(x=49, y=41)


# This is the section of code which creates a button
Button(root, text='Este boton', bg='#FFFAFA', font=('arial', 12, 'normal'), command=btnClickFunction).place(x=138, y=81)


# This is the section of code which creates the a label
Label(root, text='nueva label', bg='#FFFAFA', font=('arial', 12, 'normal')).place(x=144, y=139)
root.mainloop()
