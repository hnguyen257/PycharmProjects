from Tkinter import tkFileDialog
from Tkinter import *
import os

def browse_button_0():
    global folder_path_0
    filename = filedialog.askdirectory()
    folder_path_0.set(filename)

def browse_button_1():
    global folder_path_1
    filename = filedialog.askdirectory()
    folder_path_1.set(filename)

def start():
    global root
    os.system("python dd_comp.py \""+folder_path_0.get()+"\" \""+folder_path_1.get()+"\"")
    root.destroy()

def cancel():
    global root
    root.destroy()

def check_paths(*args):
    global folder_path_0
    global folder_path_1
    global start_button

    start_button.config(state=DISABLED)
    if folder_path_0.get() != "" and folder_path_1.get() != "":
        start_button.config(state=NORMAL)

    if os.path.exists(folder_path_0.get()) and os.path.exists(folder_path_1.get()):
        start_button.config(state=NORMAL)


root = Tk()
# tkinter Variable Setup
# ------------------------------------------------------------
# Path 1 Initialization and Trace
folder_path_0 = StringVar()
folder_path_0.trace("w", check_paths)

# Path 2 Initialization and Trace
folder_path_1 = StringVar()
folder_path_1.trace("w", check_paths)

# Error Message 1 Initialization
error_message_0 = StringVar()

# Error Message 2 Initialization
error_message_1 = StringVar()
# ------------------------------------------------------------



# Path 1 Grouping
# ------------------------------------------------------------
# Input Label
label_path_0 = Label(master=root, text="DD Folder #1")
label_path_0.grid(row=0, column=0, columnspan=2, sticky=W+E)

# Browse Button Configuration
browse_path_0 = Button(text="Browse", command=browse_button_0)
browse_path_0.grid(row=1, column=0, sticky=W+E)

# Path Entry Configuration
text_entry_0 = Entry(master=root,textvariable=folder_path_0)
text_entry_0.grid(row=1, column=1, sticky=W+E)

# Error Message Configuration
error_label_0 = Label(master=root, textvariable=error_message_0, fg='red')
error_label_0.grid(row=2, column=0, columnspan=2)
# ------------------------------------------------------------



# Path 2 Grouping
# ------------------------------------------------------------
# Input Label
label_path_1 = Label(master=root, text="DD Folder #2")
label_path_1.grid(row=3, column=0, columnspan=2, sticky=W+E)

# Browse Button Configuration
browse_path_1 = Button(text="Browse", command=browse_button_1)
browse_path_1.grid(row=4, column=0, sticky=W+E)

# Path Entry Configuration
text_entry_1 = Entry(master=root,textvariable=folder_path_1)
text_entry_1.grid(row=4, column=1, sticky=W+E)

# Error Message Configuration
error_label_1 = Label(master=root, textvariable=error_message_1, fg='red')
error_label_1.grid(row=5, column=0, columnspan=2)
# ------------------------------------------------------------


# Start / Cancel Grouping
# ------------------------------------------------------------
# Start Button and Configuration
start_button = Button(text="Start", command=start, state=DISABLED)
start_button.grid(row=6, column=0, sticky=W+E)
# Cancel Button and Configuration
cancel_button = Button(text="Cancel", command=cancel)
cancel_button.grid(row=6, column=1, sticky=W+E)



mainloop()
