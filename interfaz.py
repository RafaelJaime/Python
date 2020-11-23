import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox 
from tkinter import scrolledtext

# Ventanas
root = Tk()
mainwindow = tk.Toplevel(root)
viewcompetitions = tk.Toplevel(root)
groupwindow = tk.Toplevel(root)

# Métodos generales
def on_closing():
    # Mandar peticion de logout
	if messagebox.askokcancel("Logout", "You want to log out?"):
		mainwindow.state(newstate="withdraw")
		viewcompetitions.state(newstate="withdraw")
		groupwindow.state(newstate="withdraw")
		root.state(newstate="normal")

# Métodos ventana 1
def btnCFAccept():
	if len(tInputUsername.get()) == 0:
		messagebox.showwarning("Login error", "Fill the fields to complete the login form.")
	elif tInputUsername.get() == "Hola":
    		# poner message box con que has iniciado sesión
			mainwindow.state(newstate="normal")
			root.state(newstate="withdraw")
	else:
		messagebox.showwarning("Login error", "The username already exists.")

# Metodos ventana2
def btnCFListCompetitions():
	viewcompetitions.state(newstate="normal")
	mainwindow.state(newstate="withdraw")
def btnCFCreateGroup():
	groupwindow.state(newstate="normal")
	mainwindow.state(newstate="withdraw")

# Metodos ventana 3.1
def btnCFClose():
	viewcompetitions.state(newstate="withdraw")
	groupwindow.state(newstate="withdraw")
	mainwindow.state(newstate="normal")

# Metodos ventana 3.2
def btnClickFunction():
	print('clicked')

# Ventana 1
root.geometry('300x100')
root.title('Login')
root.resizable(False, False)
# Widgets ventana 1
label1 = Label(root, text='Username: ').place(x=20, y=20)
tInputUsername=Entry(root)
tInputUsername.place(x=100, y=20)
Button(root, text='Accept', command=btnCFAccept).place(x=110, y=60)

# Ventana 2
mainwindow.title("Main menu")
mainwindow.geometry('300x148')
mainwindow.state(newstate="withdraw")
mainwindow.resizable(False, False)
mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
# Wdigets ventana2
mainwindow.geometry('300x148')
mainwindow.title('Main menu')
Button(mainwindow, text='List of competitions', command=btnCFListCompetitions, width=16).place(x=72, y=16)
Button(mainwindow, text='Create a group', command=btnCFCreateGroup, width=16).place(x=72, y=63)
Label(mainwindow, text='Waiting for a group...').place(x=83, y=112)

# Ventana 3.1
viewcompetitions.title("Competitions")
viewcompetitions.geometry('300x148')
viewcompetitions.state(newstate="withdraw")
viewcompetitions.protocol("WM_DELETE_WINDOW", on_closing)
viewcompetitions.resizable(False, False)
# Wdigets ventana3.1
Label(viewcompetitions, text='Competitions').place(x=100, y=12)
text_area = scrolledtext.ScrolledText(viewcompetitions,  
                                      wrap = tk.WORD,  
                                      width = 33,  
                                      height = 6)

text_area.grid(column = 0, pady = 0, padx = 10) 
text_area.insert(tk.INSERT, """This is a scrolledtext widget to make tkinter text read only. 
Hi 
Geeks !!!
Geeks !!! 
Geeks !!!  
Geeks !!! 
Geeks !!! 
Geeks !!! 
Geeks !!! """)
text_area.configure(state ='disabled')
Button(viewcompetitions, text='Close', command=btnCFClose, width=5).place(x=110, y=112)

# Ventana 3.2
groupwindow.title("Create a group")
groupwindow.geometry('300x148')
groupwindow.state(newstate="withdraw")
groupwindow.protocol("WM_DELETE_WINDOW", on_closing)
groupwindow.resizable(False, False)
# Widgets ventana 3.2
tInputGroupName=Entry(groupwindow)
tInputGroupName.place(x=120, y=7)
Label(groupwindow, text='Group name: ').place(x=29, y=8)
tInputMemberTwo=Entry(groupwindow)
tInputMemberTwo.place(x=120, y=34)
Label(groupwindow, text='Member 2: ').place(x=43, y=35)
tInputMemberThree=Entry(groupwindow)
tInputMemberThree.place(x=120, y=61)
Label(groupwindow, text='Member 3: ').place(x=43, y=62)
Button(groupwindow, text='Close', command=btnCFClose).place(x=220, y=95)
Button(groupwindow, text='Enroll the competition', command=btnClickFunction).place(x=17, y=95)

root.mainloop()