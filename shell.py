import ec_lexer
import ec_parser
import tkinter as tk
from tkinter import filedialog, messagebox
from sys import *

def open_file_dialog():
    try:
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("electriC files", "*.ec"), ("All files", "*.*")])

        if not file_path:
            return
        tokens = ec_lexer.read(file_path)
        parser = ec_parser.Parser(tokens)
        ast = parser.parse_ec_prog_statement()
        print(ast)
        messagebox.showinfo("Success", "The file has been processed successfully. An excel file has been generated in the root folder, and the nodes are printed out in the terminal.")

    except Exception as e:
        messagebox.showerror("Error", e)
    
root = tk.Tk()
root.title("electriC")
root.minsize(250,50)

# Make the window appear in the middle of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - root.winfo_reqwidth()) // 2
y_position = (screen_height - root.winfo_reqheight()) // 2
root.geometry(f"+{x_position}+{y_position}")
root.resizable(False, False)

button = tk.Button(root, text="Select a file", command=open_file_dialog)
button.pack(pady=20)

root.mainloop()


#############################
#        Known Issues       #
#############################
    
# 1. None