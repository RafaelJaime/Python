import tkinter as tk
from tkinter import ttk
from tkinter import * 
# Ventanas
root = Tk()

# Métodos ventana 1
def btnLogin():
    print('clicked')
def btnRegister():
	print('clicked')
def getInputBoxValue():
	userInput = tInputEmailLogin.get()
	return userInput

# Ventana 1
root.geometry('300x100')
root.title('Login')
root.resizable(False, False)

# Widgets ventana 1
Label(root, text='Email:').place(x=20, y=20)
Button(root, text='Login', command=btnLogin).place(x=220, y=50)
Button(root, text='Register', command=btnRegister).place(x=20, y=50)
tInputEmailLogin=Entry(root, width=26)
tInputEmailLogin.place(x=70, y=20)

# Cerramos
root.mainloop()