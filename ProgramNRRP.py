import tkinter as tk
from tkinter import Menu, scrolledtext
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
        self.tab_var_used_frame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.tab_var_used_frame.place(x=8, y=40, width=368, height=368)

        # Create scrollbar for the tab_var_used_frame
        self.var_used_scrollbar = tk.Scrollbar(self.tab_var_used_frame, orient=tk.VERTICAL)
        self.var_used_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display the content (you can replace this with your own content)
        self.var_used_listbox = tk.Listbox(self.tab_var_used_frame, yscrollcommand=self.var_used_scrollbar.set)
        self.var_used_listbox.pack(fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the listbox
        self.var_used_scrollbar.config(command=self.var_used_listbox.yview)
#-----------------------------------------------------PARSE TABLE------------------------------#
        self.label = tk.Label(root, text="PARSE TABLE:", font=("Helvetica", 12, "bold"))
        self.label.place(x=400, y=2)

        self.label = tk.Label(root, text="<placeholder for ptble file>", font=("Helvetica", 8))
        self.label.place(x=400, y=20)

        # Create variable used display frame
        self.tab_var_used_frame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.tab_var_used_frame.place(x=400, y=40, width=600, height=298)

        # Create vertical scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_y = tk.Scrollbar(self.tab_var_used_frame, orient=tk.VERTICAL)
        self.var_used_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Create horizontal scrollbar for the tab_var_used_frame
        self.var_used_scrollbar_x = tk.Scrollbar(self.tab_var_used_frame, orient=tk.HORIZONTAL)
        self.var_used_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create a listbox to display the content with both vertical and horizontal scrollbars
        self.var_used_listbox = tk.Listbox(self.tab_var_used_frame, yscrollcommand=self.var_used_scrollbar_y.set, xscrollcommand=self.var_used_scrollbar_x.set)
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

        self.tab_var_used_frame = tk.Frame(root, bg="white", relief=tk.SUNKEN, bd=2)
        self.tab_var_used_frame.place(x=8, y=500, width=1200, height=298)

    def load_button_command(self):
        file_path = filedialog.askopenfilename(filetypes=[("Production Files", "*.prod;*.ptbl")])
        if file_path:
            self.label_2_status.config(text=file_path)
            if file_path.endswith(".prod"):
                app.prod_load_file(file_path)  # Assuming 'app' is the createTable instance
            elif file_path.endswith(".ptbl"):
                app.ptbl_load_file(file_path)  # Assuming 'app' is the createTable instance
            else:
                print("Invalid file type.")

    def save_file(self):
        pass  # Implement save functionality

    def save_file_as(self):
        pass  # Implement save as functionality

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgramNRRP(root)
    root.mainloop()
