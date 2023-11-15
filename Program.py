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
import tkinter as tk  # Import the tkinter library for creating the graphical user interface
from tkinter import *  # Import additional elements from tkinter
from tkinter import scrolledtext, Menu, messagebox  # Import specific tkinter elements
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename  # Import file open and save dialog functions from tkinter
import os  # Import the 'os' module for working with the operating system
from pathlib import Path  # Import the 'Path' class from the 'pathlib' module for working with file paths
import re

class Program(tk.Tk):
    def __init__(self, title, size):
        # Initialize the Application
        super().__init__()

        # Set the title and window size
        self.window_name = title
        
        self.currDir = os.getcwd()
        self.prod_file = ""
        self.prod_file_name = ""
        self.ptbl_file = ""
        self.ptbl_file_name = ""
        
        self.prod_content = []
        
        self.ptbl_content = []
        self.ptbl_terminals = []
        self.ptbl_NT = []
        
        btn = Button(self, text="Button", command=self.open_file)
        btn.place(x=50, y=50)
        
        btn = Button(self, text="Parse", command=self.parse)
        btn.place(x=50, y=80)

        self.mainloop() # Start the main application loop
        
    def open_file(self, event=None):
        ftype = [('Production File', ['*.prod']), ('Parse Table File', ['*.ptbl'])]
        file = open(askopenfilename(initialdir=self.currDir, title='Select file', filetypes=ftype))  # Open a file dialog to select production/parse table files
        
        file_details = os.path.basename(file.name).split(".")
        print(file_details)
        
        if file_details[-1] == "prod":
            self.prod_file_name = file_details[0]
            prod_content = file.read()          
            self.getProdContent(strip = prod_content.splitlines())
        elif file_details[-1] == "ptbl":
            self.ptbl_file_name = file_details[0]
            ptbl_content = file.read()
            self.getPtblContent(strip = ptbl_content.splitlines())
    
    def getProdContent(self, strip):
        for line in strip:
            str = re.split(",", line)
            str[0] = int(str[0])
            self.prod_content.append(str)
            
    def getPtblContent(self, strip):
        self.ptbl_terminals = re.split(",", strip[0])[1:]
            
        for line in strip[1:]:
            str = re.split(",", line)
            self.ptbl_NT.append(str[0])
            self.ptbl_content.append(str[1:])
            
    def parse(self, event=None):
        def push(prod, stack):
            prod.reverse()
            for symbol in prod:
                if symbol != 'e':
                    stack.append(symbol)
            
        stack = []
        stack.append('$')
        stack.append(self.ptbl_NT[0])
        
        print(self.prod_content)
        print(self.ptbl_terminals)
        print(self.ptbl_NT)
        print(self.ptbl_content)
        
        input_txt = '  + id *   id  '
        
        input_buffer = input_txt.split()
        input_buffer.append('$')
        
        print(stack[-1])
        print(input_buffer)
        
        stack_top = stack[-1]
        curr_input_index = 0
        
        while(stack_top != '$'):
            print(f"before:{stack}")
            
            row = self.ptbl_NT.index(stack_top) if stack_top in self.ptbl_NT else None
            col = self.ptbl_terminals.index(input_buffer[curr_input_index]) if input_buffer[curr_input_index] in self.ptbl_terminals else None
            
            if stack_top == input_buffer[curr_input_index]:
                stack.pop()
                curr_input_index+=1
                print(f"after:{stack}")
            elif stack_top in self.ptbl_terminals:
                print(f"after:{stack}")
                print("Error!")
                break
            elif row == None or col == None or self.ptbl_content[row][col] == '':
                print(f"after:{stack}")
                print("Error adshjasd!")
                break
            elif self.ptbl_content[row][col] != '':
                stack.pop()
                prod_index = int(self.ptbl_content[row][col]) - 1
                prod = self.prod_content[prod_index][2].split()
                push(prod, stack)
                print(f"after:{stack}")
            
            stack_top = stack[-1]      
        
Program("Non-Recursive Predictive Parser", "1150x596")