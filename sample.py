import tkinter as tk

# Basic Window
"""
root = tk.Tk()
root.geometry("600x400")
root.wm_state('zoomed')
tk.Label(root,text="Hello world").pack()
root.mainloop()
"""



from tkhtmlview import *

# Initialize Window
root = tk.Tk()
root.geometry("600x400")
root.wm_state('zoomed')


# Create the grid
# NOTE: if using grid system. ALWAYS use coloumnconfigure!

# Responsiveness! Must
root.columnconfigure(0)  # Add weight=int if you want to add weights
root.columnconfigure(1)
root.columnconfigure(2)




# HomeScreen

htmltext = """
<h1>Waka Ama Regional Association Scoring Program</h1>
<p>Gives you the result of the overall Waka Ama winner</p>
"""

# Title = HTMLLabel(root,html=htmltext).grid(column=1, row=0)

FONT_FAMILY = "Helvetica"
title_font = (FONT_FAMILY, 20, "bold") 
heading_font = (FONT_FAMILY, 15) 
default_font = (FONT_FAMILY, 10) 


col_row = 3
for i in range(col_row):
    for j in range(col_row):
        tk.Frame(root,highlightbackground="black",highlightthickness=1).grid(column=i, row=j, ipadx=10, ipady=10,sticky="NSEW")



Title = tk.Label(root,text="Waka Ama Regional Association Scoring Program", font=title_font).grid(column=1,row=0)
Heading = tk.Label(root,text="Gives you the result of the overall Waka Ama winner", font=heading_font).grid(column=1,row=1)
Paragraph = tk.Label(root,text="Gives you the result of the overall Waka Ama winner", font=default_font).grid(column=1,row=2)

# showframes
frame1 = tk.Frame(root,highlightbackground="black",highlightthickness=1)
frame1.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW")



# Finish
root.mainloop()