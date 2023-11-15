#Programming Exercise 03: Non-Recursive Predictive Parsing
"""Programmers:                         Student No.
    Francis Albert Celeste              2020-09429
    Alfred Lu                           2020-09814
    Harold Clyde Valiente               2020-05249

Program Description:
   The python program implements a non-recursive predictive parser that checks if a given sequence of tokens is valid based on 
   the given syntactic rules.
"""

import tkinter as tk
from tkinter import ttk, filedialog, simpledialog
import re
import os 
import csv

class ProgramNRDP(tk.Tk):
    
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.state('zoomed')
        self.resizable(False,False)
        
        self.prod_data = []
        self.prod_status = None
        self.ptbl_data = []
        self.ptbl_markers = []
        self.ptbl_terminals = []
        self.ptbl_NT = []
        self.ptbl_status = None
        
        self.file_path = ''
        self.loaded_prod_file = ''
        self.loaded_ptbl_file = ''
        self.left_side = left_section(self)
        self.right_side = right_section(self)
        self.mainloop()

    """
        This is a function that executes the loading of the input files into the program when the "LOAD" button is pressed.
        Input: None
        Output: None
    """
    def load_button_command(self):
        # Asks user to choose one input file (.prod or .ptbl) from a directory
        file_path = filedialog.askopenfilename(filetypes=[("Parser Input Files", "*.prod;*.ptbl")])
        # self.file_path = file_path
        
        if file_path:
            if file_path.endswith(".prod"):     # For loading .prod files
                self.file_path = file_path
                self.prod_load_file(file_path)
            elif file_path.endswith(".ptbl"):   # For loading .ptbl files
                self.ptbl_load_file(file_path)
            else:
                print("Invalid file type!")
                
    """
        This is a function that loads a production file into the program when a .prod file is selected by a user.
        It uses the file's path to execute the function.
        Input: File path of the chosen production file
        Output: None
    """
    def prod_load_file(self, file_path):
        """
            This is a function that checks if the sequence of the line number in the first column of the .prod file is from
            1 to n.
            Input: Line number sequence in an array
            Output: Bool value (True or False)
        """
        def is_sequence_starting_from_one(arr):
            # Checks if the array is a sequence starting from 1
            if arr[0] != 1:
                return False

            # Checks if the difference between each element and its next element is 1 
            for i in range(len(arr) - 1):
                if arr[i] + 1 != arr[i + 1]:
                    return False
            return True
        
        if file_path:
            # removes the table
            self.left_side.remove_prod_table()    
            
            # Opens and reads the .prod file
            with open(file_path, "r") as file:
                prod_content = file.read()
            
            # Splits the content of .prod file to lines
            prod_content = prod_content.splitlines()
            line_num = []
            row = []
            self.prod_status = True
            
            # Extracts the contents of the .prod file
            for line in prod_content:
                data = re.split(",", line) # Splits each line content to individual symbol
                line_num.append(int(data[0])) # Collects the line numbers
                row.append(data)
                print(len(data))
                if len(data) != 3:
                    self.prod_status = False
                    break

            if self.prod_data == [] and self.prod_status == False:
                self.left_side.status_label.config(text=f"NO FILE LOADED: Production file cannot be loaded")
            elif is_sequence_starting_from_one(line_num) and self.prod_status == True: # When the line number sequence follows the 1 to n sequence and have complete data
                """
                    Populates the variables that holds necessary data of the .prod file
                """
                self.prod_data = row                                # Contents of the loaded .prod file
                self.loaded_prod_file = file_path.split('/')[-1]    # Stores file name of the loaded .prod file
                
                # Displays status message in the NRD parser UI
                self.left_side.produc_placeholder.config(text=file_path.split('/')[-1])
                self.left_side.status_label.config(text=f"LOADED: {file_path.split('/')[-1]}" )
                
                # Displays the .prod file as a production table
                for x in row:
                    self.left_side.var_used_production_Treeview.insert("", "end", values=x)
                    self.left_side.var_used_production_Treeview.pack(fill='y', expand=True)
                
                self.check_loaded()     # Checks the loaded input files
            elif is_sequence_starting_from_one(line_num) and self.prod_status == False: # When the line number sequence follows the 1 to n sequence but has incomplete data
                self.left_side.status_label.configure(text=f"Incomplete columns in each non-terminal! {self.loaded_prod_file} is loaded.") # Trap Incorrect ID sequence in prod file
                
                # Displays the previous successfully loaded .prod file as a production table
                for x in self.prod_data:
                    self.left_side.var_used_production_Treeview.insert("", "end", values=x)
                    self.left_side.var_used_production_Treeview.pack(fill='y', expand=True)
                return 
            else: # When the line number sequence does not follows the 1 to n sequence
                self.left_side.status_label.configure(text=f"Incorrect ID sequence! {self.loaded_prod_file} is loaded.") # Trap Incorrect ID sequence in prod file
                
                # Displays the previous successfully loaded .prod file as a production table
                for x in self.prod_data:
                    self.left_side.var_used_production_Treeview.insert("", "end", values=x)
                    self.left_side.var_used_production_Treeview.pack(fill='y', expand=True)
                return     

    """
        This is a function that loads a parse table file into the program when a .ptbl file is selected by a user.
        It uses the file's path to execute the function.
        Input: File path of the chosen parse table file
        Output: None
    """
    def ptbl_load_file(self, file_path):
        if file_path:
            self.left_side.remove_parse_table() # Removes the table
            
            # Opens the selected .ptbl file
            with open(file_path, "r") as file:
                data = file.read()  # Reads the loaded .ptbl file
                self.extract_ptbl(file_path, data)  # Extracts the contents of the .ptbl file
            
             # When the parse table file loading is unsuccessful and no .ptbl file is previously loaded successfully
            if self.ptbl_data == []:
                self.left_side.status_label.config(text=f"NO FILE LOADED: Incomplete data in ptbl file")
             # When the parse table file loading is unsuccessful and there is a .ptbl file previously loaded successfully
            elif self.ptbl_status == True:
                self.left_side.status_label.config(text=f"LOADED: {file_path.split('/')[-1]}" )
                self.loaded_ptbl_file = file_path.split('/')[-1]
                self.left_side.ptable_placeholder.config(text=file_path.split('/')[-1])
                
            # Extracts the column headings
            headings = self.ptbl_data[0].strip().split(',')
            self.left_side.var_used_parse_treeview["columns"] = headings
            
            # Creates the parse table UI
            for col in headings:
                self.left_side.var_used_parse_treeview.heading(col, text=col, anchor="center")
                self.left_side.var_used_parse_treeview.column(col, width=80, anchor="center")  # Adjust the width as needed

            # Populate the Treeview with data from the file
            for line in self.ptbl_data[1:]:
                data = line.strip().split(',')
                self.left_side.var_used_parse_treeview.insert("", "end", values=data)
        
            self.left_side.var_used_parse_treeview.pack(fill='y', expand=True)
            self.check_loaded()     # Checks the loaded input files
    
    """
        This is a function that extracts the content of a loaded parse table file (.ptbl). This also determines if the parse 
        table file is not eligible to be loaded.
        Input: File path of the chosen parse table file and the data inside the said file
        Output: None
    """    
    def extract_ptbl(self, file_path, data):
        non_term = []
        content = []
        data = data.splitlines() # Splits the parse table content by line
        
        terminals = re.split(",", data[0]) # Gets the header terminals from the parse table file
        terminal_num = len(terminals)   # Gets the number of terminals in the parse table
        
        # Divides each line of the parse table file, from the second line, to non-terminals and the productions number or blank
        for line in data[1:]:
            row = re.split(",", line)
            
            # Checks if the number of columns in a line is equal to the number of terminals in the parse table
            if terminal_num != len(row):
                if self.ptbl_data != []:    # Condition where there is a previous successfully loaded parse table file
                    self.left_side.status_label.config(text=f"Incomplete data! {self.loaded_ptbl_file} is loaded.")   
                    self.ptbl_status = False
                return 
            
            non_term.append(row[0])
            content.append(row[1:])
        
        # Updates the variables that holds the necessary information needed for the parsing process
        self.loaded_ptbl_file = file_path.split('/')[-1]   
        self.ptbl_data = data
        self.ptbl_terminals = terminals[1:] 
        self.ptbl_NT = non_term
        self.ptbl_markers = content
        self.ptbl_status = True
    
    """
        This is the function that executes the parsing process of the program. It follows the Non-Recursive Predictive Parsing algorithm.
        This is also the function ran when the "PARSE" button is pressed.
        Input: None
        Output: None
    """     
    def parse(self):
        self.right_side.remove_parsing_table() # Removes the parsing table

        self.right_side.parsing_treeview.column("#3", width=250, stretch="no")
        
        """
            This is a function that implements the push operation of the stack used in the parser. It has an additional functionality
            where when an epsilon is encountered (represented by small e), it would not push the symbol to the stack.
            Input: Production table variable and the stack
            Output: None
        """
        def push(prod, stack):
            prod.reverse()
            for symbol in prod:
                if symbol != 'e':
                    stack.append(symbol)
        
        # Initializes the stack with a dollar sign (end of stack) and the first non-terminal    
        stack = []
        stack.append('$')
        stack.append(self.ptbl_NT[0])
        
        input_txt = self.left_side.input_field.get('1.0','end') # Gets the user input from the text input bar
        
        input_buffer = input_txt.split()    # Splits the user input into separate tokens and stores it in an input buffer
        input_buffer.append('$')            # Adds a $ to the end of the input buffer, signifying the end of the buffer
        
        stack_top = stack[-1]       # Initializes the top of the stack to the stack's topmost element
        curr_input_index = 0        # Initializes the current input index to start at the beginning of the input buffer
        
        # Reversed for proper displaying of the stack to the UI
        stack.reverse()
        self.right_side.parsing_treeview.insert("", "end", values=[stack, input_buffer])
        stack.reverse()
        
        # Loop that executes the Non-Recursive Predictive Parsing
        # Ends the loop when the top of the stack and the symbol pointed by the current input index are $
        while(stack_top != '$'):
            action = " "
            row = self.ptbl_NT.index(stack_top) if stack_top in self.ptbl_NT else None
            col = self.ptbl_terminals.index(input_buffer[curr_input_index]) if input_buffer[curr_input_index] in self.ptbl_terminals else None
            
            if stack_top == input_buffer[curr_input_index]: # The top of the stack and the symbol pointed by the current input index are the same terminals
                stack.pop()
                action = f"Match {input_buffer[curr_input_index]} "
                curr_input_index+=1
            elif stack_top in self.ptbl_terminals: # The top of the stack is a terminal but does not match with the symbol pointed by the current input index 
                action = 'ERROR! Top stack terminal does not match with current symbol in input buffer.' 
                break
            elif row == None or col == None or self.ptbl_markers[row][col] == '': # No productions are found based on the parse table
                action = 'ERROR! No production found.'
                break
            elif self.ptbl_markers[row][col] != '': # A production exists in the parse table
                stack.pop()
                prod_index = int(self.ptbl_markers[row][col]) - 1 
                prod = self.prod_data[prod_index][2].split()
                action = f"Output {stack_top} > {self.prod_data[prod_index][2]}"
                push(prod, stack)
            
            reverse_stack = list(reversed(stack))
            
            to_display = [reverse_stack, input_buffer[curr_input_index:], action]
            self.right_side.parsing_treeview.insert("", "end", values=to_display)
            
            stack_top = stack[-1]
        
        # When the top of the stack and the symbol pointed by the current input index are $
        if( stack_top == '$' and input_buffer[curr_input_index] == '$'):
            to_display = ['','', "Match $"]
            self.right_side.parsing_placeholder.config(text=f"Valid. Please see {self.file_path.split('/')[-1].split('.')[0]}.prsd")
            self.right_side.parsing_treeview.insert("", "end", values=to_display)
            self.right_side.parsing_treeview.pack(side='top', anchor='w', fill='y')
            
            # When there are still symbols in the input buffer not accounted for
            if(curr_input_index != len(input_buffer)-1):
                self.right_side.parsing_placeholder.config(text="ERROR")
                to_display = ['','',"ERROR! Does not reach end of input buffer."]
                self.right_side.parsing_treeview.insert("", "end", values=to_display)
                self.right_side.parsing_treeview.pack(side='top', anchor='w', fill='y')  
        else:
            self.right_side.parsing_placeholder.config(text="ERROR")
            to_display = ['','',action] 
            self.right_side.parsing_treeview.insert("", "end", values=to_display)
            self.right_side.parsing_treeview.pack(side='top', anchor='w', fill='y')  
        
        # Creates the output file and sets the path where its going to be saved
        output_filename = self.file_path.split('/')[-1].split('.')[0] + '.prsd'
        output_path = os.path.join(os.path.dirname(self.file_path), output_filename)  
        
        output_filename = simpledialog.askstring("Set File Name", "Enter File Name for '.prsd' file") # Asks user to input a name for the file
        if(output_filename != None ):
            output_filename = f"{output_filename}_{self.loaded_prod_file.replace('.prod', '.prsd')}" 
            
            output_path = os.path.join(os.path.dirname(self.file_path), output_filename)
            
            with open(output_path, 'w', newline='') as output_file:
                writer = csv.writer(output_file)
                # Write the parsing table contents
                for row in self.right_side.parsing_treeview.get_children():
                    values = self.right_side.parsing_treeview.item(row)['values']
                    writer.writerow(values)
                    
            self.right_side.parsing_placeholder.config(text=f"Valid. Please see {output_filename}")
            
        else:
            return
        
    """
        This is a function that verifies if the input files have the same filenames or when at least one of the input files
        are not loaded successfully. When the said conditions are true, the "PARSE" button is disabled.
        Input: None
        Output: None
    """    
    def check_loaded(self):
        self.right_side.remove_parsing_table()
        
        prod_file_loaded = len(self.prod_data) != 0
        ptbl_file_loaded = len(self.ptbl_data) != 0
        
        if prod_file_loaded and ptbl_file_loaded:
            if os.path.exists(self.file_path):
                # Check if filenames match
                if self.loaded_prod_file.split('.')[0] == self.loaded_ptbl_file.split('.')[0]:
                    self.left_side.parse_button.configure(state=tk.NORMAL)
                    self.right_side.parsing_placeholder.config(text="Filenames are the same")
                    self.left_side.parse_button.pack(side = 'left')
                    return  # Return after enabling the parse button
                else:
                    self.left_side.parse_button.config(state=tk.DISABLED)
                    self.right_side.parsing_placeholder.config(text="Filenames are not the same")
            else:
                self.right_side.parsing_placeholder.config(text="Missing .ptbl file")
        else:
            self.right_side.parsing_placeholder.config(text="One of the loaded Files are empty")
            
class left_section(tk.Frame):
    
    def __init__(self, parent):
        # INITIALIZE LEFT SECTION FRAME
        
        super().__init__()
        
        self.parent = parent
        self.pack(side = "left", fill = "y", padx= 30, pady= [10, 10])
        
        # Load Button & load-status label
        self.frame_1 = ttk.Frame(self)
        self.frame_1.pack(side = "top", anchor='nw' ,pady = [0, 15])
        
        # self.load_button = tk.Button(self.frame_1, text="Load", command=self.load_button_command, width=10)
        self.load_button = ttk.Button(self.frame_1, text="Load", command=parent.load_button_command, width=10)
        self.load_button.pack(side = "left")
        
        self.status_label = ttk.Label(self.frame_1, text="", font=("Helvetica", 12, 'bold'))
        self.status_label.pack(side = "left")
        
        #-----------------------------------------------------PRODUCTION TABLE------------------------------#
        self.frame_2 = ttk.Frame(self)
        self.frame_2.pack(side = "top", anchor='w')
        
        self.produc_label = ttk.Label(self.frame_2, text="PRODUCTIONS:", font=("Helvetica", 12, "bold"))
        self.produc_label.pack(side = "top")
        
        self.produc_placeholder = ttk.Label(self.frame_2, text="", font=("Helvetica", 10))
        self.produc_placeholder.pack(side = "top", anchor='w', pady=[0, 10])

        # Create variable used display frame
        self.prodFrame = tk.Frame(self, bg="white", relief='sunken', bd=2)
        self.prodFrame.pack(side = 'top', anchor='w', fill='y', pady=[0, 10])
        
        # Create scrollbar for the tab_var_used_frame
        self.var_used_scrollbar = ttk.Scrollbar(self.prodFrame, orient='vertical')
        self.var_used_scrollbar.pack(side='right', fill='y')
        
         # Create a listbox to display the content (you can replace this with your own content)
        self.var_used_production_Treeview = ttk.Treeview(self.prodFrame, yscrollcommand=self.var_used_scrollbar.set)
        
        headings = ['ID', 'NT', 'P']
        self.var_used_production_Treeview["columns"] = headings
        
        for col in headings:
            self.var_used_production_Treeview.heading(col, text=col, anchor="center") # Assuming the first row contains column headings
            self.var_used_production_Treeview.column(col, width=100, anchor="center")  # Adjust the width as needed
    
        self.var_used_production_Treeview.column("#0", width=0, stretch='no')
        self.var_used_production_Treeview.pack(fill='y', expand=True)
        
        # Configure the scrollbar to work with the listbox
        self.var_used_scrollbar.config(command=self.var_used_production_Treeview.yview)
        
        #-----------------------------------------------------PARSE TABLE------------------------------#
        self.frame_3 = ttk.Frame(self)
        self.frame_3.pack(side = 'top', anchor='w')
        
        self.ptable_label = ttk.Label(self.frame_3, text="PARSE TABLE:", font=("Helvetica", 12, "bold"))
        self.ptable_label.pack(side = 'top')

        self.ptable_placeholder = ttk.Label(self.frame_3, text="", font=("Helvetica", 10))
        self.ptable_placeholder.pack(side = 'top',anchor='w', pady=[0, 10])

        # PARSE TABLE
        # Create variable used display frame
        self.parse_frame = tk.Frame(self, bg="white", relief='sunken', bd=2)
        self.parse_frame.pack(side = 'top', fill = "x")

        # Create vertical scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_y = ttk.Scrollbar(self.parse_frame, orient='vertical')
        self.var_used_scrollbar_y.pack(side='right', fill='y')

        # Create horizontal scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_x = ttk.Scrollbar(self.parse_frame, orient='horizontal')
        self.var_used_scrollbar_x.pack(side='bottom', fill='x')

        # Create a listbox to display the content with both vertical and horizontal scrollbars
        self.var_used_parse_treeview = ttk.Treeview(self.parse_frame, yscrollcommand=self.var_used_scrollbar_y.set, xscrollcommand=self.var_used_scrollbar_x.set, height=6)
        self.var_used_parse_treeview.pack(fill='x', expand=True,)

        # Configure the scrollbars to work with the listbox
        self.var_used_scrollbar_y.config(command=self.var_used_parse_treeview.yview)
        self.var_used_scrollbar_x.config(command=self.var_used_parse_treeview.xview)

        #-----------------------------------------------------INPUT SECTION------------------------------#

        self.input_label = ttk.Label(self, text="INPUT", font=("Helvetica", 12, "bold"))
        self.input_label.pack(side = 'top', anchor='w', pady=[10, 0])

        self.frame_4 = ttk.Frame(self)
        self.frame_4.pack(side = 'top', anchor='w')
        
        self.input_field = tk.Text(master = self.frame_4, bg="white", relief='sunken', bd=2, wrap='word', height=1, width=40, padx=5, pady=5)
        self.input_field.pack(side = 'left', padx=[0, 20])

        self.parse_button = tk.Button(master = self.frame_4, text="Parse", command= parent.parse, width="8", state=tk.DISABLED)
        self.parse_button.pack(side = 'left')
    
    def remove_prod_table(self):
        for item in self.var_used_production_Treeview.get_children():
                self.var_used_production_Treeview.delete(item)

        self.var_used_production_Treeview.column("#0", width = 0, stretch = "no")
    
    def remove_parse_table(self):
        for item in self.var_used_parse_treeview.get_children():
                self.var_used_parse_treeview.delete(item)

        self.var_used_parse_treeview.pack_forget()
        self.var_used_parse_treeview.column("#0", width = 0, stretch = "no")     
        
class right_section(tk.Frame):
    def __init__(self, parent):
        # INITIALIZE LEFT SECTION FRAME
        
        super().__init__()
        self.parent = parent
        self.pack(side = "left", fill = "both", expand = True, padx= 30, pady= [10, 30])
        
        # Label for Parsing section
        
        self.frame_1 = tk.Frame(self)
        self.frame_1.pack(side = "top", anchor='w')
        
        self.parsing_label = ttk.Label(self.frame_1, text="PARSING:", font=("Helvetica", 12, "bold"))
        self.parsing_label.pack(side = "top", anchor='w')
        
        self.parsing_placeholder = ttk.Label(self.frame_1, text="", font=("Helvetica", 8))
        self.parsing_placeholder.pack(side = "top", pady=[0, 10])
        
        self.parsing_treeview = ttk.Treeview(self, height=50)
        
        headings = [ 'Stack', 'Input Buffer', 'Action']
        self.parsing_treeview["columns"] = headings
        
        for col in headings:
            self.parsing_treeview.heading(col, text=col, anchor="center")
            self.parsing_treeview.column(col, anchor="center")
            
        self.parsing_treeview.column("#0", width=0, stretch = "no")
        
        self.parsing_treeview.pack(side='top', fill='both', expand=True)
    
    def remove_parsing_table(self):
        for item in self.parsing_treeview.get_children():
                self.parsing_treeview.delete(item)

        # self.parsing_treeview.column("#0", width=0, stretch = "no")
        
ProgramNRDP(title="NRDP App", size="1280x720")