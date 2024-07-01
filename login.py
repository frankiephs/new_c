import tkinter as tk

root = tk.Tk()
root.geometry("600x400")

# coloumn,row

# Configure column weights for the first row
root.columnconfigure(0, weight=1)  # Lower weight for column 0 in the first row
root.columnconfigure(1, weight=2)  # Higher weight for column 1 in the first row





# first col, first row
frame1 = tk.Frame(root,highlightbackground="black",highlightthickness=1)
frame1.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW")
rectangle_1 = tk.Label(root, text="Rectangle 1", bg="green", fg="white")
rectangle_1.grid(column=0, row=0, ipadx=10, ipady=10, sticky="W")

frame2 = tk.Frame(root,highlightbackground="black",highlightthickness=1)
frame2.grid(column=1, row=0, ipadx=10, ipady=10,sticky="NSEW")
rectangle_2 = tk.Label(root, text="Rectangle 2", bg="red", fg="white")
rectangle_2.grid(column=1, row=0, ipadx=10, ipady=10, sticky="E")

# first col, second row
frame5 = tk.Frame(root,highlightbackground="black",highlightthickness=1,bg="cyan")
frame5.grid(column=0, row=1, ipadx=10, ipady=10,sticky="NSEW")

# Second Col, second row, 
frame3 = tk.Frame(root,highlightbackground="black",highlightthickness=1)
frame3.grid(column=1, row=1, ipadx=10, ipady=10,sticky="NSEW")
rectangle_3 = tk.Label(root, text="Rectangle 3", bg="blue", fg="white")
rectangle_3.grid(column=1, row=1, ipadx=10, ipady=10)

# fills entire row 5
frame4 = tk.Frame(root,highlightbackground="black",highlightthickness=1)
frame4.grid(column=0, row=5, ipadx=10, ipady=10,sticky="NSEW", columnspan=2) # coloumn span. fills the space for 2 cells.
rectangle_4 = tk.Label(frame4, text="Rectangle 4", bg="orange", fg="black")
rectangle_4.pack(fill="both", expand=True) # pack fill + expand=True. Fills the entire frame



# fills entire row 6
frame6 = tk.Frame(root, highlightbackground="black", highlightthickness=1)
frame6.grid(column=0, row=6, ipadx=10, ipady=10, sticky="NSEW", columnspan=2)  # column span. fills the space for 2 cells.

frame6.columnconfigure(0, weight=1)
frame6.columnconfigure(1, weight=1)
frame6.rowconfigure(0,weight=1)

# row 6 first cell
frame6_first = tk.Frame(frame6, highlightbackground="black", highlightthickness=1)
frame6_first.grid(column=0, row=0, ipadx=10, ipady=10, sticky="NSEW")  # grid inside frame6

# row 6 second cell
frame6_second = tk.Frame(frame6, highlightbackground="black", highlightthickness=1)
frame6_second.grid(column=1, row=0, ipadx=10, ipady=10, sticky="NSEW")  # grid inside frame6

rectangle_6 = tk.Label(frame6_first, text="Rectangle 6", bg="grey", fg="black")
rectangle_6.pack(fill="both", expand=True)  # pack fill + expand=True. Fills the entire frame


root.mainloop()