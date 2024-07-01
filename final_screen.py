import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import file_read as fr
from tkinter import messagebox
import scoring
import csv_export
import datetime
class gui_c:
    def __init__(self, master):
        self.root = master
        self.root.geometry("600x400")
        self.root.wm_state('zoomed')
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
        
        self.save_to_logfile("HomeScreen")
        self.current_frame = tk.Frame(self.root)

        help_button = tk.Button(self.current_frame,text="Help", command=lambda:self.show_screen(self.HelpScreen))
        help_button.pack()

        
        

        title_label = tk.Label(self.current_frame,text="WAKA AMA PROGRAM")
        title_label.pack()

        paragraph_label = tk.Label(self.current_frame,text="Make sure it is a valid parent folder. Parent Folder should not contain non-folder items inside.")
        paragraph_label.pack()


        OpenFolder = tk.Button(self.current_frame, text="Open Folder", command=self.get_folder_path)
        OpenFolder.pack()

        # Pack the frame to display
        self.current_frame.pack(fill=tk.BOTH, expand=True)



    def get_folder_path(self):
        self.save_to_logfile("Get Golder Path")
        folder_path = filedialog.askdirectory()

        if folder_path:
            
            self.show_screen(self.SelectYearsScreen,data=folder_path)  # Pass function reference without calling it
        else:
            messagebox.showwarning("Error while Processing", "Invalid File Folder\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            
    def SelectYearsScreen(self, parent_path):
        self.save_to_logfile("Select Years screen")
        self.current_frame = tk.Frame(self.root)

        Back_Button = tk.Button (self.current_frame, text = "Back",command=lambda: self.show_screen(self.HomeScreen))
        Back_Button.pack()

        try:
            years_and_files = fr.file_read_c.return_years(parent_path)
        except:
            error = f"[Invalid folder] Select Another folder | {parent_path}"
            messagebox.showwarning("Error while Processing", f"{error}\n\n -For more details, go to Help.\n -To check all errors, go to logs after this process")
            self.show_screen(self.HomeScreen)
            return
            

        headers_label = tk.Label(self.current_frame,text="Year | FIles")
        headers_label.pack()
        
        
        for i in years_and_files:
            year_label = tk.Label(self.current_frame,text=f"{i} : {years_and_files[i]}",relief="sunken")
            year_label.pack()
        
                
        select_year_label = tk.Label(self.current_frame,text="Type the available years above")
        select_year_label.pack()
        input_label = tk.Entry(self.current_frame)
        input_label.pack()
        


        filter_label = tk.Label(self.current_frame,text="Type your filter keyword. Leave Blank if none")
        filter_label.pack()
        filter_input = tk.Entry(self.current_frame)
        filter_input.pack()

        select_year_button = tk.Button(self.current_frame,text="Select year",command= lambda : self.select_year(input_label,years_and_files, filter_input))
        select_year_button.pack()

        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.parent_path = parent_path

    def select_year(self,input_label,years_dictionary,filter_input):
        self.save_to_logfile("Select Year")
        user_input = input_label.get() # returns into string
        
        filter_keyword = filter_input.get()

        if filter_keyword:
            messagebox.showinfo("Info", f"filter keyword:{filter_keyword}")
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
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

        self.Loading_label = tk.Label(self.current_frame, text=f"{year_input} | Starting the program...")
        
        self.Loading_label.pack()
        self.progressbar = ttk.Progressbar(self.current_frame, length=300, mode="indeterminate")
        self.progressbar.pack()
        self.progressbar.start(self.loading_delay)

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
        self.save_to_logfile("Filter Files")
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
        self.Loading_label.config(text=text)
        self.root.update_idletasks()
        



    def ResultsScreen(self, year_regional_association_scores):
        self.save_to_logfile("Results Screen")

        self.current_frame = tk.Frame(self.root)

        Home_Button = tk.Button (self.current_frame, text = "Home",command=lambda: self.show_screen(self.HomeScreen))
        Home_Button.pack()


        title = tk.Label(self.current_frame, text=f"Results for {self.selected_year} {self.filter_keyword}")
        title.pack()


        container = ttk.Frame(self.current_frame, borderwidth=2, relief="groove")
        canvas = tk.Canvas(container, borderwidth=2, relief="ridge")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        table_frame = ttk.Frame(canvas,borderwidth=2, relief="sunken")

        table_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=table_frame)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        table_frame.columnconfigure(0, weight=1)  # Lower weight for column 0 in the first row
        table_frame.columnconfigure(1, weight=2)  # Higher weight for column 1 in the first row
        table_frame.columnconfigure(0, weight=1)  # Lower weight for column 0 in the first row

        ttk.Label(table_frame, text="Place").grid(row=0, column=0)
        ttk.Label(table_frame, text="Regional Association").grid(row=0, column=1)
        ttk.Label(table_frame, text="Points").grid(row=0, column=2)

        for place, i in enumerate(year_regional_association_scores.items(), start=1):
            name, points = i
            ttk.Label(table_frame, text=place).grid(row=place, column=0)
            ttk.Label(table_frame, text=name).grid(row=place, column=1)
            ttk.Label(table_frame, text=points).grid(row=place, column=2)
        
        
        
        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.current_frame.pack(fill=tk.BOTH, expand=True)

        OpenLogs = tk.Button(self.current_frame,text="Open Logs", command= self.LogsScreen)
        OpenLogs.pack()
        SaveCSV = tk.Button(self.current_frame,text="Save to CSV", command=lambda:self.show_screen(self.pick_save,year_regional_association_scores))
        SaveCSV.pack()

    
    def LogsScreen(self):
        self.save_to_logfile("Logs Screen")
        log_win=tk.Toplevel()

        Back_Button = tk.Button (log_win, text = "Back",command=log_win.destroy)
        Back_Button.pack()

        # Add a Scrollbar(horizontal)
        vertical_scrollbar= tk.Scrollbar(log_win, orient='vertical')
        vertical_scrollbar.pack(side=tk.RIGHT, fill='y')


        Title = tk.Label(log_win, text="Logs Screen")
        Title.pack()

        Text = tk.Text(log_win, yscrollcommand=vertical_scrollbar.set)
        vertical_scrollbar.config(command=Text.yview)
        Text.pack()
        

        with open("logs", "r") as logfile_content:
            logs_list = logfile_content.readlines()

        for i in logs_list:
            Text.insert(tk.END,i)

        Text.configure(state=tk.DISABLED) # after insert
            


    
        
        
    
    def HelpScreen(self):
        self.save_to_logfile("Help Screen")
        
        self.current_frame = tk.Frame(self.root)

        Back_Button = tk.Button (self.current_frame, text = "Back",command=lambda: self.show_screen(self.HomeScreen))
        Back_Button.pack()


        tk.Label(self.current_frame, text="Help Screen").pack()
        self.current_frame.pack(fill=tk.BOTH, expand=True)  # Show new frame
        self.current_frame = self.current_frame

        self.current_frame.pack(fill=tk.BOTH, expand=True)

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
        Home_Button = tk.Button (self.current_frame, text = "Home",command=lambda: self.show_screen(self.HomeScreen))
        Home_Button.pack()


        self.current_frame = tk.Frame(self.root)
        tk.Label(self.current_frame, text=f"{self.selected_year} {self.filter_keyword} results Successfully saved to CSV").pack()
        tk.Label(self.current_frame, text=f"{folder_path}").pack()

        OpenLogs = tk.Button(self.current_frame,text="Open Logs", command= self.LogsScreen)
        OpenLogs.pack()
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    


    def show_screen(self, Screen_function,data=None):
        self.save_to_logfile(f" Changed screen ")
        if self.current_frame:
            self.current_frame.pack_forget()  # Hide current frame
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
                    file.write('\n')
                    file.write(f"\n{current_time}")
                file.write(f"{data} \n")
            print(f"Log updated | {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
app = gui_c(root)
root.mainloop()