from tkinter import *
from tkinter import messagebox

def donothing():
	pass
	
def add_menus(win):
	menubar = Menu(win)
	
	#Add File Menu Drop Down
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=donothing)
	filemenu.add_command(label="Open", command=donothing)
	filemenu.add_command(label="Save", command=donothing)
	filemenu.add_command(label="Save as...", command=donothing)
	filemenu.add_command(label="Close", command=donothing)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=win.quit)
	
	menubar.add_cascade(label="File", menu=filemenu)
	
	#Add Edit Menu Drop Down
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Undo", command=donothing)
	editmenu.add_separator()
	editmenu.add_command(label="Cut", command=donothing)
	editmenu.add_command(label="Copy", command=donothing)
	editmenu.add_command(label="Paste", command=donothing)
	editmenu.add_command(label="Delete", command=donothing)
	editmenu.add_command(label="Select All", command=donothing)

	menubar.add_cascade(label="Edit", menu=editmenu)
	
	#Add Help Menu Drop Down
	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=donothing)
	helpmenu.add_command(label="About...", command=donothing)
	
	menubar.add_cascade(label="Help", menu=helpmenu)

	win.config(menu=menubar)

def add_button(win,txt,cmd=None):
	b=Button(win,text=txt,command=cmd)
	b.pack()

def msg(msg):
	messagebox.showinfo("Hello",msg)

def open_ide():
	root=Tk()

	root.wm_title("BARD - IDE")
	root.geometry("500x500")

	add_menus(root)
	add_button(root,"Test 1")
	add_button(root,"Test 2")

	root.mainloop()
