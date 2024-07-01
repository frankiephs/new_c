import tkinter as tk
from tkinter import filedialog

# command= lambda: -are nameless functions. since command only asks for the function name not call it, we will use lambda and pass the call function to pass a value to the function

root = tk.Tk()
root.geometry("600x400")
root.wm_state('zoomed')

# main routine

def hello(text):
    hello = tk.Label(root,text=text)
    hello.pack()

ask = tk.Entry(root)
ask.pack()

button = tk.Button(root,text="Open",command= lambda : hello(ask.get()))
button.pack()

root.mainloop()









