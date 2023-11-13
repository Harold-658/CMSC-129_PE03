import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ProgramNRRP(tk.Tk):
    
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(size)
        self.state('zoomed')
        self.left_side = left_section(self)
        self.right_side = right_section(self)
        self.mainloop()
        
    def load_button_command(self):
        file_path = filedialog.askopenfilename(filetypes=[("Production Files", "*.prod;*.ptbl")])
        if file_path:
            self.left_side.status_label.config(text=file_path)
            if file_path.endswith(".prod"):
                self.prod_load_file(file_path)  # Assuming 'app' is the createTable instance
            elif file_path.endswith(".ptbl"):
                self.ptblCreateLoadTable(file_path)
            else:
                print("Invalid file type.")

    def prod_load_file(self, file_path):
        # Clear existing data in the Listbox
        self.left_side.var_used_listbox.delete(0, tk.END)

        # Create a frame within tab_var_used_frame
        tree_frame = tk.Frame(self.left_side.frame_2)
        tree_frame.pack( fill=tk.BOTH)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, show="headings")

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack Treeview
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        if file_path:
            # Clear existing data in the Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Read the content of the selected file
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Assuming each line in the file represents a row in the table
            for line in lines:
                data = line.strip().split(',')
                self.tree.insert("", "end", values=data)

            # Assuming the first row contains column headings
            headings = lines[0].strip().split(',')
            self.tree["columns"] = headings
            for col in headings:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, width=100, anchor="center")  # Adjust the width as needed


    def ptblCreateLoadTable(self, file_path):
        # Clear existing data in the Listbox
        self.var_used_listbox.delete(0, tk.END)

        # Create a frame within tab_var_used_frame
        tree_frame = tk.Frame(self.parseFrame)
        tree_frame.pack(expand=tk.YES, fill=tk.BOTH)

        # Create Treeview
        self.tree = ttk.Treeview(tree_frame, show="headings")

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Pack Treeview
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

        if file_path:
            # Clear existing data in the Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Read the content of the selected file
            with open(file_path, "r") as file:
                lines = file.readlines()

            # Extract column headings
            headings = lines[0].strip().split(',')
            self.tree["columns"] = headings
            for col in headings:
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, width=100, anchor="center")  # Adjust the width as needed

            # Populate the Treeview with data from the file
            for line in lines[1:]:
                data = line.strip().split(',')
                self.tree.insert("", "end", values=data)
                
class left_section(tk.Frame):
    
    def __init__(self, parent):
        # INITIALIZE LEFT SECTION FRAME
        
        super().__init__()
        
        self.parent = parent
        self.pack(side = "left", fill = "y", padx= 30, pady= [0, 30])
        
        # Load Button & load-status label
        self.frame_1 = ttk.Frame(self)
        self.frame_1.pack(side = "top", anchor='nw' ,pady = 15)
        
        # self.load_button = tk.Button(self.frame_1, text="Load", command=self.load_button_command, width=10)
        self.load_button = ttk.Button(self.frame_1, text="Load", command=parent.load_button_command, width=10)
        self.load_button.pack(side = "left")
        
        self.status_label = ttk.Label(self.frame_1, text="<placeholder for loaded file>", font=("Helvetica", 8))
        self.status_label.pack(side = "left")
        
        #-----------------------------------------------------PRODUCTION TABLE------------------------------#
        self.frame_2 = ttk.Frame(self)
        self.frame_2.pack(side = "top", anchor='w')
        
        self.produc_label = ttk.Label(self.frame_2, text="PRODUCTIONS:", font=("Helvetica", 12, "bold"))
        self.produc_label.pack(side = "top")
        
        self.produc_placeholder = ttk.Label(self.frame_2, text="<placeholder for prod.file>", font=("Helvetica", 8))
        self.produc_placeholder.pack(side = "top", pady=[0, 10])

        # Create variable used display frame
        self.prodFrame = tk.Frame(self, bg="white", relief='sunken', bd=2)
        self.prodFrame.pack(side = 'top', anchor='w', fill='y', pady=[0, 20])
        
        # Create scrollbar for the tab_var_used_frame
        self.var_used_scrollbar = ttk.Scrollbar(self.prodFrame, orient='vertical')
        self.var_used_scrollbar.pack(side='right', fill='y')

        # Create a listbox to display the content (you can replace this with your own content)
        self.var_used_listbox = tk.Listbox(self.prodFrame, yscrollcommand=self.var_used_scrollbar.set, width=40)
        self.var_used_listbox.pack(fill='y', expand=True)

        # Configure the scrollbar to work with the listbox
        self.var_used_scrollbar.config(command=self.var_used_listbox.yview)
        
        #-----------------------------------------------------PARSE TABLE------------------------------#
        self.frame_3 = ttk.Frame(self)
        self.frame_3.pack(side = 'top', anchor='w')
        
        self.ptable_label = ttk.Label(self.frame_3, text="PARSE TABLE:", font=("Helvetica", 12, "bold"))
        self.ptable_label.pack(side = 'top')

        self.ptable_placeholder = ttk.Label(self.frame_3, text="<placeholder for ptble file>", font=("Helvetica", 8))
        self.ptable_placeholder.pack(side = 'top', pady=[0, 10])

        # Create variable used display frame
        self.parseFrame = tk.Frame(self, bg="white", relief='sunken', bd=2)
        self.parseFrame.pack(side = 'top', fill = "x", pady=[0, 20])

        # Create vertical scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_y = ttk.Scrollbar(self.parseFrame, orient='vertical')
        self.var_used_scrollbar_y.pack(side='right', fill='y')

        # Create horizontal scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_x = ttk.Scrollbar(self.parseFrame, orient='horizontal')
        self.var_used_scrollbar_x.pack(side='bottom', fill='x')

        # Create a listbox to display the content with both vertical and horizontal scrollbars
        self.var_used_listbox = tk.Listbox(self.parseFrame, yscrollcommand=self.var_used_scrollbar_y.set, xscrollcommand=self.var_used_scrollbar_x.set, width=100)
        self.var_used_listbox.pack(fill='both', expand=True)

        # Configure the scrollbars to work with the listbox
        self.var_used_scrollbar_y.config(command=self.var_used_listbox.yview)
        self.var_used_scrollbar_x.config(command=self.var_used_listbox.xview)

        #-----------------------------------------------------INPUT SECTION------------------------------#

        self.input_label = ttk.Label(self, text="INPUT", font=("Helvetica", 12, "bold"))
        self.input_label.pack(side = 'top', anchor='w')

        self.frame_4 = ttk.Frame(self)
        self.frame_4.pack(side = 'top', anchor='w')
        
        self.input_field = tk.Text(master = self.frame_4, bg="white", relief='sunken', bd=2, wrap='word', height=1, width=40)
        self.input_field.pack(side = 'left', padx=[0, 20])

        self.parse_button = ttk.Button(master = self.frame_4, text="Parse", command="", width="8")
        self.parse_button.pack(side = 'left')
        
class right_section(tk.Frame):
     def __init__(self, parent):
        # INITIALIZE LEFT SECTION FRAME
        
        super().__init__()
        self.parent = parent
        self.pack(side = "left", fill = "both", expand = True, padx= 30, pady= [15, 30])
        
        # Label for Parsing section
        
        self.frame_1 = tk.Frame(self)
        self.frame_1.pack(side = "top", anchor='w')
        
        self.parsing_label = ttk.Label(self.frame_1, text="PRODUCTIONS:", font=("Helvetica", 12, "bold"))
        self.parsing_label.pack(side = "top")
        
        self.parsing_placeholder = ttk.Label(self.frame_1, text="<placeholder for prod.file>", font=("Helvetica", 8))
        self.parsing_placeholder.pack(side = "top", pady=[0, 10])
        
        self.parsing_frame = tk.Frame(self, bg="white", relief=tk.SUNKEN, bd=2)
        self.parsing_frame.pack(side='top', fill='both', expand=True)
        
ProgramNRRP(title="NRRP App", size="1280x720")

