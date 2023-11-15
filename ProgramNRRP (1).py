#Programming Exercise 02: Lexical Analyzer
"""Programmers:                         Student No.
    Francis Albert Celeste              2020-09429
    Alfred Lu                           2020-09814
    Harold Clyde Valiente               2020-05249

Program Description:
   The python program has a partial implementation of a compiler for a customized programming language (PL). 
   A lexical analyzer that has partial implementation requires the software to read custom programming language code, 
   do lexical analysis, and output the analysis results.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import re
import os 
import csv

class ProgramNRRP(tk.Tk):
    
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.state('zoomed')
        self.resizable(False,False)
        
        self.prod_content = []
        self.ptbl_content = []
        self.ptbl_terminals = []
        self.ptbl_NT = []
        
        self.file_path = ''
        self.left_side = left_section(self)
        self.right_side = right_section(self)
        self.mainloop()
        
    def load_button_command(self):
        
        file_path = filedialog.askopenfilename(filetypes=[("Production Files", "*.prod;*.ptbl")])
        self.file_path = file_path
        if file_path:
            self.left_side.status_label.config(text=f"LOADED: {file_path.split('/')[-1]}" )
            if file_path.endswith(".prod"):
                self.left_side.produc_placeholder.config(text=file_path.split('/')[-1])
                self.prod_load_file(file_path)  # Assuming 'app' is the createTable instance
            elif file_path.endswith(".ptbl"):
                self.left_side.ptable_placeholder.config(text=file_path.split('/')[-1])
                self.ptblCreateLoadTable(file_path)
            else:
                print("Invalid file type.")
                

    def prod_load_file(self, file_path):
        self.check_loaded()
        
        if file_path:
            # remove the table
            self.left_side.remove_prod_table()    
            
            """
                To populate the prod_content
            """
            with open(file_path, "r") as file:
                prod_content = file.read()
            
            prod_content = prod_content.splitlines()
            
            for line in prod_content:
                data = re.split(",", line)
                data[0] = int(data[0])
                self.prod_content.append(data)
                self.left_side.var_used_production_Treeview.insert("", "end", values=data)
            
            """ END """

            # Assuming the first row contains column headings
            headings = ['ID', 'NT', 'P']
            self.left_side.var_used_production_Treeview["columns"] = headings
            
            for col in headings:
                self.left_side.var_used_production_Treeview.heading(col, text=col, anchor="center")
                self.left_side.var_used_production_Treeview.column(col, width=100, anchor="center")  # Adjust the width as needed
            
        self.left_side.var_used_production_Treeview.pack(fill='y', expand=True)
        self.check_loaded()

    def ptblCreateLoadTable(self, file_path):
        if file_path:
            self.left_side.remove_parse_table()
            
            """
                To populate the ptbl lists
            """
            with open(file_path, "r") as file:
                ptbl_content = file.read()
                
            ptbl_content = ptbl_content.splitlines()
            
            self.ptbl_terminals = re.split(",", ptbl_content[0])[1:]    
        
            for line in ptbl_content[1:]:
                data = re.split(",", line)
                self.ptbl_NT.append(data[0])
                self.ptbl_content.append(data[1:])
            
            """ END """
            
            # Extract column headings
            headings = ptbl_content[0].strip().split(',')
            self.left_side.var_used_parse_treeview["columns"] = headings
            
            for col in headings:
                self.left_side.var_used_parse_treeview.heading(col, text=col, anchor="center")
                self.left_side.var_used_parse_treeview.column(col, width=100, anchor="center")  # Adjust the width as needed

            # Populate the Treeview with data from the file
            for line in ptbl_content[1:]:
                data = line.strip().split(',')
                self.left_side.var_used_parse_treeview.insert("", "end", values=data)
            
        self.left_side.var_used_parse_treeview.pack(fill='y', expand=True)
        self.check_loaded()
        
    def parse(self, event=None):
        self.right_side.remove_parsing_table()

        headings = [ 'Stack', 'Input Buffer', 'Action']
        self.right_side.parsing_treeview["columns"] = headings
        
        for col in headings:
            self.right_side.parsing_treeview.heading(col, text=col, anchor="center")
            self.right_side.parsing_treeview.column(col, width=150, anchor="center")
        
        def push(prod, stack):
            prod.reverse()
            for symbol in prod:
                if symbol != 'e':
                    stack.append(symbol)
            
        stack = []
        stack.append('$')
        stack.append(self.ptbl_NT[0])
        
        input_txt = self.left_side.input_field.get('1.0','end')
        
        input_buffer = input_txt.split()
        input_buffer.append('$')
        
        stack_top = stack[-1]
        curr_input_index = 0
        stack.reverse()
        self.right_side.parsing_treeview.insert("", "end", values=[stack, input_buffer])
        stack.reverse()
        
        while(stack_top != '$'):
            action = " "
            row = self.ptbl_NT.index(stack_top) if stack_top in self.ptbl_NT else None
            col = self.ptbl_terminals.index(input_buffer[curr_input_index]) if input_buffer[curr_input_index] in self.ptbl_terminals else None
            
            if stack_top == input_buffer[curr_input_index]: # match
                stack.pop()
                action = f"Match {input_buffer[curr_input_index]} "
                curr_input_index+=1
            elif stack_top in self.ptbl_terminals:
                action = 'ERROR! Top stack terminal does not match with current symbol in input buffer.' 
                break
            elif row == None or col == None or self.ptbl_content[row][col] == '': # if basta uy
                action = 'ERROR! No production found.'
                break
            elif self.ptbl_content[row][col] != '':
                stack.pop()
                prod_index = int(self.ptbl_content[row][col]) - 1 
                prod = self.prod_content[prod_index][2].split()
                action = f"Output {stack_top} > {self.prod_content[prod_index][2]}"
                push(prod, stack)
            
            reverse_stack = list(reversed(stack))
            
            to_display = [reverse_stack, input_buffer[curr_input_index:], action]
            self.right_side.parsing_treeview.insert("", "end", values=to_display)
            
            stack_top = stack[-1]
        
        if( stack_top == '$' and input_buffer[curr_input_index] == '$'):
            to_display = ['','', "Match $"]
            self.right_side.parsing_placeholder.config(text=f"Valid. Please see {self.file_path.split('/')[-1].split('.')[0]}.prsd")
            self.right_side.parsing_treeview.insert("", "end", values=to_display)
            self.right_side.parsing_treeview.pack(side='top', anchor='w', fill='y')
            
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
        
        
        output_filename = self.file_path.split('/')[-1].split('.')[0] + '.prsd'
        output_path = os.path.join(os.path.dirname(self.file_path), output_filename)

        with open(output_path, 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            # Write the parsing table contents
            for row in self.right_side.parsing_treeview.get_children():
                values = self.right_side.parsing_treeview.item(row)['values']
                writer.writerow(values)

        self.right_side.parsing_placeholder.config(text=f"Valid. Please see {output_filename}")
        
    def check_loaded(self):
        if(self.prod_content != [] and self.ptbl_content != []):
            self.left_side.parse_button.configure(state=tk.NORMAL)
            
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

        self.var_used_production_Treeview.pack_forget()
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
        self.parsing_treeview.pack(side='top', fill='both', expand=True)
    
    def remove_parsing_table(self):
        for item in self.parsing_treeview.get_children():
                self.parsing_treeview.delete(item)

        self.parsing_treeview.pack_forget()
        self.parsing_treeview.column("#0", width=0, stretch = "no")
        
ProgramNRRP(title="NRRP App", size="1280x720")
