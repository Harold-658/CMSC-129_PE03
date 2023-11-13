import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class ProgramNRRP:
    def __init__(self, root):
        self.root = root
        self.root.title("CRAZY NRRP")
        self.root.geometry("768x1366")
       
        #PRODUCTIONS SECTION
        self.label = tk.Label(root, text="PRODUCTIONS:", font=("Helvetica", 12, "bold"))
        self.label.place(x=8, y=2)

        self.label = tk.Label(root, text="<placeholder for prod.file>", font=("Helvetica", 8))
        self.label.place(x=8, y=20)

        # Create variable used display frame
        self.prodFrame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.prodFrame.place(x=8, y=40, width=368, height=368)

        # Create scrollbar for the tab_var_used_frame
        self.var_used_scrollbar = tk.Scrollbar(self.prodFrame, orient=tk.VERTICAL)
        self.var_used_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display the content (you can replace this with your own content)
        self.var_used_listbox = tk.Listbox(self.prodFrame, yscrollcommand=self.var_used_scrollbar.set)
        self.var_used_listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the listbox
        self.var_used_scrollbar.config(command=self.var_used_listbox.yview)
#-----------------------------------------------------PARSE TABLE------------------------------#
        self.label = tk.Label(root, text="PARSE TABLE:", font=("Helvetica", 12, "bold"))
        self.label.place(x=400, y=2)

        self.label = tk.Label(root, text="<placeholder for ptble file>", font=("Helvetica", 8))
        self.label.place(x=400, y=20)

        # Create variable used display frame
        self.parseFrame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.parseFrame.place(x=400, y=40, width=600, height=298)

        # Create vertical scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_y = tk.Scrollbar(self.parseFrame, orient=tk.VERTICAL)
        self.var_used_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Create horizontal scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_x = tk.Scrollbar(self.parseFrame, orient=tk.HORIZONTAL)
        self.var_used_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a listbox to display the content with both vertical and horizontal scrollbars
        self.var_used_listbox = tk.Listbox(self.parseFrame, yscrollcommand=self.var_used_scrollbar_y.set, xscrollcommand=self.var_used_scrollbar_x.set)
        self.var_used_listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbars to work with the listbox
        self.var_used_scrollbar_y.config(command=self.var_used_listbox.yview)
        self.var_used_scrollbar_x.config(command=self.var_used_listbox.xview)

        self.label_2_loaded = tk.Label(root, text="LOADED:", font=("Helvetica", 12, "bold"))
        self.label_2_loaded.place(x=400, y=350)

        self.label_2_status = tk.Label(root, text="<placeholderforprod.file>", font=("Helvetica", 8))
        self.label_2_status.place(x=474, y=352)

        self.insert_button = tk.Button(root, text="Load", command=self.load_button_command, width=8)
        self.insert_button.place(x=474 + self.label_2_status.winfo_reqwidth() + 8, y=350)


#-----------------------------------------------------INPUT SECTION------------------------------#
        # Create label for status
        self.label_2 = tk.Label(root, text="INPUT", font=("Helvetica", 12, "bold"))
        self.label_2.place(x=90, y=430)

        self.bi_console_frame = tk.Text(bg="white", relief=tk.SUNKEN, bd=2, wrap=tk.WORD, height=1, width=40)
        self.bi_console_frame.place(x=150, y=432)

        self.insert_button = tk.Button(root, text="Parse", command="", width="8")
        self.insert_button.place(x=480, y=430)

#-----------------------------------------------------PROCESS TABLE------------------------------#

        # Create label for status
        self.label_2 = tk.Label(root, text="PARSING: ", font=("Helvetica", 12, "bold"))
        self.label_2.place(x=8, y=480)

        self.bi_console_frame = tk.Text(bg="white", relief=tk.SUNKEN, bd=2, wrap=tk.WORD, height=1, width=40)
        self.bi_console_frame.place(x=150, y=432)

        self.label_2 = tk.Label(root, text="<placeholder for status>", font=("Helvetica", 8))
        self.label_2.place(x=100, y=484)

        self.par_var_used_frame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.par_var_used_frame.place(x=8, y=500, width=1200, height=298)

    def load_button_command(self):
        file_path = filedialog.askopenfilename(filetypes=[("Production Files", "*.prod;*.ptbl")])
        if file_path:
            self.label_2_status.config(text=file_path)
            if file_path.endswith(".prod"):
                self.prod_load_file(file_path)  # Assuming 'app' is the createTable instance
            elif file_path.endswith(".ptbl"):
                self.ptblCreateLoadTable(file_path)
            else:
                print("Invalid file type.")

    def prod_load_file(self, file_path):
        # Clear existing data in the Listbox
        self.var_used_listbox.delete(0, tk.END)

        # Create a frame within tab_var_used_frame
        tree_frame = tk.Frame(self.prodFrame)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramNRRP(root)
    root.mainloop()
