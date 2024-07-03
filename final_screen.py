# use CustomTkinter
import customtkinter as CT
import tkinter as tk # for GUI
from tkinter import filedialog # for getting files
import file_read as fr # for file reading
from tkinter import messagebox # for warnings and info
import scoring # for scoring
import csv_export # for exporting
import datetime # for log dates


class gui_c:
    def __init__(self, master):
        
        CT.set_appearance_mode("light")
        self.root = master
        self.root.geometry("600x400")
        self.root.wm_state('zoomed')
        
        # expand the root
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.points_refference = {
        "1":8,
        "2":7,
        "3":6,
        "4":5,
        "5":4,
        "6":3,
        "7":2,
        "8":1,
        ">":1,
        }

        self.font_family = "Helvetica"

        self.title_font = (self.font_family,50,"bold") #35
        self.heading_font = (self.font_family,30) #30
        self.default_font = (self.font_family,20) #20
        


        self.loading_delay = 1
        self.logs_path = "logs"
        
        self.selected_year = None
        self.ShowError = False
        self.error_list = []
        self.current_frame = None
        self.filter_case_sensitive = False
        
        # settings
        self.filter_keyword = None

        # Show the home frame initially
        self.HomeScreen()
        self.save_to_logfile("Opened Program")


    def HomeScreen(self):
        # initialize the screen
        self.current_frame = CT.CTkFrame(self.root)
        self.save_to_logfile("HomeScreen") # save to log file

        # initialize the grid 3 rows
        self.current_frame.rowconfigure(1,weight=1) # center is much bigger
        self.current_frame.columnconfigure(0, weight=1)  # make sure column stretches
        

        # creating nav bar frame
        nav_bar = CT.CTkFrame(self.current_frame) 
        nav_bar.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to two columns
        nav_bar.columnconfigure(0,weight=1)
        nav_bar.columnconfigure(1, weight=1)
        

        # nav bar help button
        help_button = CT.CTkButton(nav_bar,text="Help", command=lambda:self.show_screen(self.HelpScreen),font=self.default_font)
        help_button.grid(column=1, sticky="NE",padx=10,pady=10)

        
        # creating the body frame
        body_frame = CT.CTkFrame(self.current_frame)
        body_frame.grid(column=0, row=1, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.
        
        # initialize the body frame to have only maxed 1 cell
        body_frame.rowconfigure(0, weight=1)
        body_frame.columnconfigure(0, weight=1)

        # Create a group for the components
        body_inner_frame = CT.CTkFrame(body_frame, fg_color="transparent")
        body_inner_frame.grid(column=0, row=0, sticky="")

        # Title
        
        title_label = CT.CTkLabel(body_inner_frame,text="WAKA AMA",font=self.title_font)
        title_label.grid()

        # subtitle
        subtitle_label = CT.CTkLabel(body_inner_frame,text="Regional Association Scoring Program",font=self.heading_font)
        subtitle_label.grid()

        # Paragraph
        paragraph_label = CT.CTkLabel(body_inner_frame,text="Make sure it is a valid parent folder. Parent Folder should not contain non-folder items inside.",font=self.default_font)
        paragraph_label.grid()

        # Open Folder Button
        OpenFolder = CT.CTkButton(body_inner_frame, text="Open Folder", command=self.get_folder_path,font=self.default_font)
        OpenFolder.grid(padx=10,pady=10)

        # Finalize the Screen
        self.current_frame.grid(row=0, column=0, sticky="NSEW")


    def get_folder_path(self):
        self.save_to_logfile("Get Golder Path")
        folder_path = filedialog.askdirectory()

        if folder_path:
            self.parent_path = folder_path
            self.show_screen(self.SelectYearsScreen,data=folder_path)  # Pass function reference without calling it
        else:
            messagebox.showwarning("Error while Processing", "Invalid File Folder\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            
    def SelectYearsScreen(self, parent_path):

        # initialize the screen
        self.save_to_logfile("Select Years screen")
        self.current_frame = CT.CTkFrame(self.root)

        # initialize the grid 3 rows
        self.current_frame.rowconfigure(1,weight=1) # center is much bigger
        self.current_frame.columnconfigure(0, weight=1)  # make sure column stretches

        # creating nav bar frame
        nav_bar = CT.CTkFrame(self.current_frame) 
        nav_bar.grid(column=0, row=0, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to two columns
        nav_bar.columnconfigure(0,weight=1)
        nav_bar.columnconfigure(1, weight=1)

        # adding nav bar back button
        Back_Button = CT.CTkButton (nav_bar, text = "Back",font=self.default_font,command=lambda: self.show_screen(self.HomeScreen))
        Back_Button.grid(column=0,row=0,sticky="NW",padx=10,pady=10)

        # creating the body frame
        body_frame = CT.CTkFrame(self.current_frame)
        body_frame.grid(column=0, row=1, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize the body frame to have only maxed 1 cell
        body_frame.rowconfigure(0, weight=1)
        body_frame.columnconfigure(0, weight=1)

        
        # Create a group for the components
        body_inner_frame = CT.CTkFrame(body_frame, fg_color="transparent")
        body_inner_frame.grid(column=0, row=0, sticky="")


        # Title
        title = CT.CTkLabel(body_inner_frame,text="Select year", font=self.title_font)
        title.grid()

        # Available years label
        available_years_label = CT.CTkLabel(body_inner_frame,text="Available Year/s", font=self.heading_font)
        available_years_label.grid()

        # Table Label
        headers_label = CT.CTkLabel(body_inner_frame,text="Year | Files",font=self.default_font)
        headers_label.grid()

        # fetch the children folders
        try:
            years_and_files = fr.file_read_c.return_years(parent_path)
        except:
            error = f"[Invalid folder] Select Another folder | {parent_path}"
            messagebox.showwarning("Error while Processing", f"{error}\n\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            self.show_screen(self.HomeScreen)
            return
            

        
        # years & Files Table
        
        for i in years_and_files:
            year_label = CT.CTkLabel(body_inner_frame,text=f"{i} : {years_and_files[i]} file/s",font=self.default_font)
            year_label.grid()
        

        # creating bottom bar frame
        bottom_bar_frame = CT.CTkFrame(self.current_frame) 
        bottom_bar_frame.grid(column=0, row=2, ipadx=10, ipady=10,sticky="NSEW") # coloumn span. fills the space for 3 cells.

        # initialize nav bar to three columns
        bottom_bar_frame.columnconfigure(0,weight=1)
        bottom_bar_frame.columnconfigure(1, weight=1)
        bottom_bar_frame.columnconfigure(2, weight=1)

        # input configuration
        placeholder_color = "white"
        year_input_placeholder = "Type your year"
        filter_input_placeholder = "Type your filter keyword"

        # Years Input

        

        year_input = CT.CTkEntry(bottom_bar_frame,font=self.default_font, fg_color="grey",width=200,placeholder_text=year_input_placeholder, placeholder_text_color=placeholder_color)
        year_input.grid(column=0,row=0)


        # Filter input

        filter_input = CT.CTkEntry(bottom_bar_frame,fg_color='grey',font=self.default_font,width=300,placeholder_text=filter_input_placeholder, placeholder_text_color=placeholder_color)
        filter_input.grid(column=1,row=0)




        # Continue Button
        select_year_button = CT.CTkButton(bottom_bar_frame,text="Select year",font=self.default_font,command= lambda : self.select_year(year_input,years_and_files, filter_input))
        select_year_button.grid(column=2,row=0)


        # Finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")
        

    def select_year(self,year_input,years_dictionary,filter_input):
        self.save_to_logfile("Select Year")
        user_input = year_input.get() # returns into string
        
        filter_keyword = filter_input.get()

        if filter_keyword:
            messagebox.showinfo("Info", f"Keyword: {filter_keyword}")
            self.filter_keyword = filter_keyword
        

        if user_input.isdigit():
            if user_input in list(years_dictionary.keys()):
                self.selected_year = user_input
                self.show_screen(self.LoadingScreen,user_input)
            else:
                messagebox.showerror("Incorrect Year", f"'{user_input}'is not part of the folders list")
                
        else:
            messagebox.showerror("Incorrect Input", f"'{user_input}' is not a year")

        

    
        
    def LoadingScreen(self, year_input):
        self.save_to_logfile("Loading Screen")
        self.current_frame = CT.CTkFrame(self.root)

        # finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")

        self.Loading_label = CT.CTkLabel(self.current_frame, text=f"{year_input} | Starting the program...")
        
        self.Loading_label.pack()
        self.progressbar = CT.CTkProgressBar(self.current_frame, mode="indeterminate",indeterminate_speed=self.loading_delay)
        self.progressbar.pack()
        self.progressbar.start()

        path_prefix = "WakaNats"
        self.year_path = fr.file_read_c.find_year_path(self.parent_path, year_input, prefix=path_prefix)
        self.files_list = fr.file_read_c.return_files(self.year_path)

        if self.files_list:
            self.update_loading_label(f"Getting files from year {self.selected_year}, {len(self.files_list)} files found")
            self.root.after(self.loading_delay, self.process_files)
        else:
            self.update_loading_label("No files found")

    def process_files(self):
        self.save_to_logfile("Process Files")
        if self.filter_keyword: # if keyword specified
            self.filtered_files_list = []
            self.current_file_index = 0
            self.root.after(self.loading_delay, self.filter_files)
        else:
            self.filtered_files_list = self.files_list # if there is no keyword specified 
            self.root.after(self.loading_delay, self.process_filtered_files)

    def filter_files(self):
        if self.current_file_index < len(self.files_list): # if file index lower than the count of files
            filename = self.files_list[self.current_file_index] # get every single filenames from the files list
            self.update_loading_label(f"Getting files from year {self.selected_year}, Checking {filename}...") # change statement

            if self.filter_case_sensitive:
                if self.filter_keyword in filename: # if the filename have keyword
                    self.filtered_files_list.append(filename) # add the file in the file list
                    self.update_loading_label(f"Getting files from year {self.selected_year}, {filename} satisfied") # change statement
            else:
                if self.filter_keyword.lower() in filename.lower(): # if the filename have keyword
                    self.filtered_files_list.append(filename) # add the file in the file list
                    self.update_loading_label(f"Getting files from year {self.selected_year}, {filename} satisfied") # change statement

            self.current_file_index += 1 # if no keyowrd, then proceed to another file
            self.root.after(self.loading_delay, self.filter_files) # repeat
        else:
            self.root.after(self.loading_delay, self.process_filtered_files) # if checked every file

    # if no keyword or with keyword
    def process_filtered_files(self):
        self.save_to_logfile("Process Filtered Files")

        if self.filtered_files_list == []:
            messagebox.showinfo("Keyword Not found", f"There are no files containing '{self.filter_keyword}' found.\n\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            self.show_screen(self.HomeScreen)
            return


        self.files_regional_association_score_list = [] 
        self.current_file_index = 0 # resets
        self.root.after(self.loading_delay, self.process_file)

    def process_file(self):
        if self.current_file_index < len(self.filtered_files_list):
            filename = self.filtered_files_list[self.current_file_index]
            self.update_loading_label(f"Processing file: {filename}")
            
            filepath = f"{self.year_path}/{filename}"
            file_contents = fr.file_read_c.return_content(filepath)
            formatted_file_contents = fr.file_read_c.format_content(file_contents, filename)     
            if formatted_file_contents == "ERROR":
                self.save_to_logfile(f"ERROR: {formatted_file_contents} | {filename}")
                error = f"There is an error on your file: | {filename}"
                if self.ShowError:
                    messagebox.showwarning("Error while Processing", f"{error}\n\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
                print(formatted_file_contents)
                
                self.error_list.append(error)
            else:
                
                file_regional_association_scores = scoring.scoring_c.return_scores(formatted_file_contents, self.points_refference)
                self.files_regional_association_score_list.append(file_regional_association_scores)

            self.current_file_index += 1
            self.root.after(self.loading_delay, self.process_file)
        else:
            self.root.after(self.loading_delay, self.finalize_processing)

    def finalize_processing(self):
        self.save_to_logfile("finalize Processing")
        year_regional_association_scores = scoring.scoring_c.return_year_sum_score(self.files_regional_association_score_list)
        year_regional_association_scores = scoring.scoring_c.sort_score(year_regional_association_scores)
        self.show_screen(self.ResultsScreen, year_regional_association_scores)



    def update_loading_label(self, text):
        self.Loading_label.configure(text=text)
        self.root.update_idletasks()
        



    def ResultsScreen(self, year_regional_association_scores):
        self.save_to_logfile("Results Screen")

        self.current_frame = CT.CTkFrame(self.root)

        Home_Button = CT.CTkButton (self.current_frame, text = "Home",command=lambda: self.show_screen(self.HomeScreen))
        Home_Button.pack()


        title = CT.CTkLabel(self.current_frame, text=f"Results for {self.selected_year} {self.filter_keyword}", font=self.title_font)
        title.pack()


        
        table_frame = CT.CTkScrollableFrame(self.current_frame, border_width=2,width=300)

        table_frame.columnconfigure(1, weight=1)  # Higher weight for column 1 in the first row

        
        cell_border_width = 1
        cell_color = "transparent"
        cell_height = 30
        small_cell_width = 30

        CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height,width=small_cell_width).grid(row=0,column=0)
        CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height).grid(row=0,column=1)
        CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height,width=small_cell_width).grid(row=0,column=2)

        CT.CTkLabel(table_frame, text="Place").grid(row=0, column=0)
        CT.CTkLabel(table_frame, text="Regional Association").grid(row=0, column=1)
        CT.CTkLabel(table_frame, text="Points").grid(row=0, column=2)
        



        for place, i in enumerate(year_regional_association_scores.items(), start=1):
            name, points = i

            CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height,width=small_cell_width).grid(row=place,column=0)
            CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height).grid(row=place,column=1)
            CT.CTkFrame(table_frame, border_width=cell_border_width,fg_color=cell_color,height=cell_height,width=small_cell_width).grid(row=place,column=2)

            CT.CTkLabel(table_frame, text=place).grid(row=place, column=0)
            CT.CTkLabel(table_frame, text=name).grid(row=place, column=1)
            CT.CTkLabel(table_frame, text=points).grid(row=place, column=2)

        
        
        table_frame.pack()

        

        OpenLogs = CT.CTkButton(self.current_frame,text="Open Logs", command= self.LogsScreen)
        OpenLogs.pack()
        SaveCSV = CT.CTkButton(self.current_frame,text="Save to CSV", command=lambda:self.show_screen(self.pick_save,year_regional_association_scores))
        SaveCSV.pack()

        # finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")


    
    def LogsScreen(self):
        self.save_to_logfile("Logs Screen")
        log_win=CT.CTkToplevel()

        Back_Button = CT.CTkButton (log_win, text = "Back",command=log_win.destroy)
        Back_Button.pack()

        # Add a Scrollbar(horizontal)
        vertical_scrollbar= CT.CTkScrollbar(log_win, orientation='vertical')
        vertical_scrollbar.pack(side=tk.RIGHT, fill='y')


        Title = CT.CTkLabel(log_win, text="Logs Screen")
        Title.pack()

        Text = tk.Text(log_win, yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.configure(command=Text.yview)
        Text.pack()
        

        with open("logs", "r") as logfile_content:
            logs_list = logfile_content.readlines()

        for i in logs_list:
            Text.insert(tk.END,i)

        Text.configure(state=tk.DISABLED) # after insert
            
    
    def HelpScreen(self):
        self.save_to_logfile("Help Screen")
        
        self.current_frame = CT.CTkFrame(self.root)

        Back_Button = CT.CTkButton (self.current_frame, text = "Back",command=lambda: self.show_screen(self.HomeScreen))
        Back_Button.pack()


        CT.CTkLabel(self.current_frame, text="Help Screen").pack()
        
        # finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")



    def pick_save(self,year_regional_association_score):
        self.save_to_logfile("Pick Save")

        folder_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")])
        
        if folder_path:
            answer = messagebox.askyesno("Confirm path",f"Are you sure you want to save to this location? \n {folder_path}")
            if answer:
                csv_export.csv_c.csv_export(year_regional_association_score,folder_path)
                
                self.show_screen(self.SaveScreen,folder_path)
        else:
            messagebox.showwarning("Error while Processing", "Invalid File Folder\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            self.show_screen(self.ResultsScreen,year_regional_association_score)    
    
        


    def SaveScreen(self,folder_path):


        self.save_to_logfile(f"{self.filter_keyword} {self.selected_year} results saved to CSV in {folder_path}")

        self.current_frame = CT.CTkFrame(self.root)
        Home_Button = CT.CTkButton (self.current_frame, text = "Home",command=lambda: self.show_screen(self.HomeScreen))
        Home_Button.grid()


        CT.CTkLabel(self.current_frame, text=f"{self.selected_year} {self.filter_keyword} results Successfully saved to CSV").grid()
        CT.CTkLabel(self.current_frame, text=f"{folder_path}").grid()

        OpenLogs = CT.CTkButton(self.current_frame,text="Open Logs", command= self.LogsScreen)
        OpenLogs.grid()

        # finalize
        self.current_frame.grid(row=0, column=0, sticky="NSEW")

    
    def show_screen(self, Screen_function,data=None):
        self.save_to_logfile(f"Changed screen ")
        if self.current_frame:
            self.current_frame.grid_forget()  # Hide current frame
            self.current_frame = None

        if data:
            Screen_function(data)
        else:
            try:
                Screen_function(data)
            except:
                Screen_function()
    
    def save_to_logfile(self,data):
        file_path = self.logs_path
        try:
            with open(file_path, 'a') as file:
                # Ensure the string starts on a new line if the file already has content
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if file.tell() != 0:
                    file.write(f"\n{current_time}")
                file.write(f"\n{data} ")
            print(f"Log updated | {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Create the main Tkinter window
root = CT.CTk()
app = gui_c(root)
root.mainloop()