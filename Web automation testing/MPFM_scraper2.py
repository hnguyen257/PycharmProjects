#Company: Emerson Process Solution
#Name: PWTTS web automation selenium script writer
#Author: Hiep Nguyen
#Released date: 08/23/2019
#version: v1.0

import tkSimpleDialog
from Tkinter import *
import tkFileDialog
import os
import ttk
import tkMessageBox
import datetime
import chardet
from difflib import SequenceMatcher
import shutil
import webbrowser
import traceback
from tkColorChooser import askcolor
import csv
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#initialize the GUI
root = Tk()
root.title("PWTTS web automation selenium script writer v1.0")
root.geometry("1025x620")
root.wm_minsize(1025,620)

#global variable
downloaded = IntVar()
downloaded_index = IntVar()
CheckVar1 = IntVar()
#default checkbox value is 1 for character compare option
CheckVar1.set(1)
#default checkbox value is 1 for open when completed option
CheckVar2 = IntVar()
CheckVar2.set(1)


#Main application
class Application(Frame):
    win = root
    var_field_input = IntVar()
    var_field_input.set(1)
    var_click = IntVar()
    var_click.set(1)
    var_loop = IntVar()
    var_loop.set(1)
    Text_A = ''
    Text_B = ''
    Text_C = ''
    Text_D = ''
    #local shared variables between functions
    current_text = ''
    current_text = current_text + "#Note: if you manually copy this script to be used elsewhere instead of clicking the \'Generate Script\' button, \n"
    current_text = current_text + "#remember to fix overflow sentences and add the except statements for it to work. \n\n"
    current_text = current_text + 'from selenium import webdriver' + '\n'
    current_text = current_text + 'from selenium.webdriver.common.keys import Keys' + '\n'
    current_text = current_text + 'import time' + '\n'
    current_text = current_text + 'import traceback' + '\n'
    current_text = current_text + 'import win32api' + '\n'
    current_text = current_text + 'from selenium.webdriver.common.by import By' + '\n'
    current_text = current_text + 'from selenium.webdriver.support.ui import WebDriverWait' + '\n'
    current_text = current_text + 'from selenium.webdriver.support import expected_conditions as EC' + '\n'
    current_text = current_text + 'driver = webdriver.Chrome("C:/Python27/chromedriver")' + '\n'
    current_text = current_text + "error_log = '' \n\n\n"
    current_text = current_text + 'try:' + '\n'

    #Action to take when user click on browse folder A
    def address_goto(self):
        address = tkSimpleDialog.askstring('Input', 'Please enter a website address:\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')

        if address == None:
            return
        self.current_text = self.current_text + '\tdriver.get("' + address + '")' + '\n' + '\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box


    def field_input(self):

        self.win = tk.Toplevel()

        win = self.win

        win.geometry("400x320")
        win.wm_minsize(400,300)
        win.wm_title("Field input")

        label_a = tk.Label(win, text="Element identification type")
        label_a.grid(row=0, column=0)

        #b = ttk.Button(win, text="Okay", command=win.destroy)
        #b.grid(row=0, column=1)



        R1 = Radiobutton(win, text="By ID", variable= self.var_field_input, value=1)
        R1.grid(row=1, column=0)

        R2 = Radiobutton(win, text="By Name", variable=self.var_field_input, value=2)
        R2.grid(row=2, column=0)

        R3 = Radiobutton(win, text="By Xpath", variable=self.var_field_input, value=3)
        R3.grid(row=3, column=0)

        label_b = tk.Label(win, text="Field element identification: ")
        label_b.grid(row=4, column=0)

        self.Text_A = Entry(win, width=60)
        self.Text_A.grid(row = 5, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)

        label_c = tk.Label(win, text="What to type in the text field:")
        label_c.grid(row=6, column=0)

        self.Text_B = Entry(win, width=60)
        self.Text_B.grid(row = 7, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)

        done = Button(win)
        done["text"] = "done"
        done["command"] = self.done_field_input
        done.grid(row = 8, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)
    def done_field_input(self):
        identification = self.Text_A.get()
        text_input = self.Text_B.get()
        identification_a = ''
        identification_b = ''
        if self.var_field_input.get() == 1:
            identification_a = 'By.ID'
            identification_b = 'by_id'

        elif self.var_field_input.get() == 2:
            identification_a = 'By.NAME'
            identification_b = 'by_name'

        elif self.var_field_input.get() == 3:
            identification_a = 'By.XPATH'
            identification_b = 'by_xpath'

        self.current_text = self.current_text + "\telem = driver.find_element_" + identification_b + "('" + identification + "')" + '\n'
        self.current_text = self.current_text + "\telem.send_keys('" + text_input + "')" + '\n' + '\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box
        self.win.destroy()
        pass




    status = 0 # 0 mean haven't started yet
    loop_button_color = 'white'
    def loop(self):
        if self.status == 0:
            self.status = 1
            self.loop_button_color = 'red'
            self.LOOP["text"] = "        End Loop         "
        else:
            self.status = 0
            self.loop_button_color = 'white'
            self.LOOP["text"] = "        Start Loop         "
        self.win = tk.Toplevel()
        win = self.win

        win.geometry("400x320")
        win.wm_minsize(400,300)
        win.wm_title("Click item")

        label_a = tk.Label(win, text="Loop type")
        label_a.grid(row=0, column=0)

        #b = ttk.Button(win, text="Okay", command=win.destroy)
        #b.grid(row=0, column=1)

        self.Text_D = Entry(win, width=60)
        self.Text_D.grid(row = 5, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)

        R1 = Radiobutton(win, text="Nonstop", variable= self.var_loop, value=1, command = self.update_loop_field())
        R1.grid(row=1, column=0)

        R2 = Radiobutton(win, text="After following number of cycles:", variable=self.var_loop, value=2, command = self.update_loop_field())
        R2.grid(row=2, column=0)

        R3 = Radiobutton(win, text="After following number of seconds:", variable=self.var_loop, value=3, command = self.update_loop_field())
        R3.grid(row=3, column=0)






        done = Button(win)
        done["text"] = "done"
        done["command"] = self.done_loop
        done.grid(row = 8, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)
    def done_loop(self):
        item = self.Text_D.get()

        self.current_text = self.current_text + '\twait = WebDriverWait(driver, 10)' + '\n'

        identification_a = ''
        identification_b = ''
        if self.var_click.get() == 1:
            identification_a = 'By.ID'
            identification_b = 'by_id'

        elif self.var_click.get() == 2:
            identification_a = 'By.NAME'
            identification_b = 'by_name'

        elif self.var_click.get() == 3:
            identification_a = 'By.XPATH'
            identification_b = 'by_xpath'



        self.current_text = self.current_text + "\telement = wait.until(EC.element_to_be_clickable((" + identification_a + ", '" + item +  "')))" + '\n'
        self.current_text = self.current_text + "\tdriver.find_element_" + identification_b + "('" + item + "').click()" + '\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box
        self.win.destroy()
        return
    a = '1'
    b = '2'
    c = '3'
    def update_loop_field(self):
        if self.var_loop.get() == 1:
            self.Text_D.delete(0, last=len(self.Text_D.get()))  #clear current value in the entry box
            self.Text_D.insert(0, self.a) #put new value in the entry box
            win.update()

        elif self.var_loop.get() == 2:
            self.Text_D.delete(0, last=len(self.Text_D.get()))  #clear current value in the entry box
            self.Text_D.insert(0, self.b) #put new value in the entry box
            win.update()


        elif self.var_loop.get() == 3:
            self.Text_D.delete(0, last=len(self.Text_D.get()))  #clear current value in the entry box
            self.Text_D.insert(0, self.c) #put new value in the entry box

        return




    def click(self):

        self.win = tk.Toplevel()

        win = self.win

        win.geometry("400x320")
        win.wm_minsize(400,300)
        win.wm_title("Click item")

        label_a = tk.Label(win, text="Element identification type")
        label_a.grid(row=0, column=0)

        #b = ttk.Button(win, text="Okay", command=win.destroy)
        #b.grid(row=0, column=1)


        R1 = Radiobutton(win, text="by ID", variable= self.var_click, value=1)
        R1.grid(row=1, column=0)

        R2 = Radiobutton(win, text="by NAME", variable=self.var_click, value=2)
        R2.grid(row=2, column=0)

        R3 = Radiobutton(win, text="by Xpath", variable=self.var_click, value=3)
        R3.grid(row=3, column=0)

        label_b = tk.Label(win, text="Field element identification: ")
        label_b.grid(row=4, column=0)

        self.Text_C = Entry(win, width=60)
        self.Text_C.grid(row = 5, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)


        done = Button(win)
        done["text"] = "done"
        done["command"] = self.done_click
        done.grid(row = 8, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 10)
    def done_click(self):
        item = self.Text_C.get()

        self.current_text = self.current_text + '\twait = WebDriverWait(driver, 10)' + '\n'

        identification_a = ''
        identification_b = ''
        if self.var_click.get() == 1:
            identification_a = 'By.ID'
            identification_b = 'by_id'

        elif self.var_click.get() == 2:
            identification_a = 'By.NAME'
            identification_b = 'by_name'

        elif self.var_click.get() == 3:
            identification_a = 'By.XPATH'
            identification_b = 'by_xpath'



        self.current_text = self.current_text + "\telement = wait.until(EC.element_to_be_clickable((" + identification_a + ", '" + item +  "')))" + '\n'
        self.current_text = self.current_text + "\tdriver.find_element_" + identification_b + "('" + item + "').click()" + '\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box
        self.win.destroy()
        return

    #Action to take when user click on compare button



    def wait(self):
        self.current_text = self.current_text + '\ttime.sleep(10)' + '\n\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box




    #Action to take when user click on compare button
    def screenshot(self):
        self.current_text = self.current_text + '\tdriver.save_screenshot(\'MPFM_test_screenshot.png\')' + '\n' + '\n'
        self.main_text.delete('1.0', END)
        self.main_text.insert(INSERT, self.current_text) #put new value in the entry box




    #Action to take when user click on compare button
    def generate_script(self):
        self.current_text = self.current_text + 'except:' + '\n'
        self.current_text = self.current_text + '\twin32api.MessageBox(0, \'Please check the recently generated error log file for more information. Thank you.\', \' \!/ Error occurs during Selenium web automation testing\')' + '\n' + '\n'
        self.current_text = self.current_text + '\te = open(\'errors.txt\', \'w+\')' + '\n'
        self.current_text = self.current_text + '\te.write(traceback.format_exc() + ' + '\'\\' +  'n\'' + ')' + '\n'
        output = open('script.py', 'wb')
        output.write(self.current_text)




    #Create the user interface layout
    def createWidgets(self):
        #Create browse folder A button
        self.ADDRESS_GOTO = Button(self)
        self.ADDRESS_GOTO["text"] = "    Go to address    "
        self.ADDRESS_GOTO["command"] = self.address_goto
        self.ADDRESS_GOTO.bind("<Enter>", lambda event: self.ADDRESS_GOTO.configure(bg="orange"))
        self.ADDRESS_GOTO.bind("<Leave>", lambda event: self.ADDRESS_GOTO.configure(bg="white"))
        self.ADDRESS_GOTO.grid(row = 2, column = 0, ipadx = 40, ipady = 10, pady = 10)

        #Create browse output location button
        self.FIELD_INPUT = Button(self)
        self.FIELD_INPUT["text"] = "      Type input to field      "
        self.FIELD_INPUT["command"] = self.field_input
        self.FIELD_INPUT.bind("<Enter>", lambda event: self.FIELD_INPUT.configure(bg="orange"))
        self.FIELD_INPUT.bind("<Leave>", lambda event: self.FIELD_INPUT.configure(bg="white"))
        self.FIELD_INPUT.grid(row = 4, column = 0, ipadx = 20, ipady = 10, pady = 10)

        #Create browse output location button
        self.CLICK = Button(self)
        self.CLICK["text"] = "        Click on an item         "
        self.CLICK["command"] = self.click
        self.CLICK.bind("<Enter>", lambda event: self.CLICK.configure(bg="orange"))
        self.CLICK.bind("<Leave>", lambda event: self.CLICK.configure(bg="white"))
        self.CLICK.grid(row = 6, column = 0, ipadx = 20, ipady = 10, pady = 10)

        #Create browse output location button
        self.LOOP = Button(self)
        self.LOOP["text"] = "        Start Loop         "
        self.LOOP["command"] = self.loop
        self.LOOP.bind("<Enter>", lambda event: self.LOOP.configure(bg="orange"))
        self.LOOP.bind("<Leave>", lambda event: self.LOOP.configure(bg=self.loop_button_color))
        self.LOOP.grid(row = 8, column = 0, ipadx = 20, ipady = 10, pady = 10)

        #Create browse output location button
        self.WAIT = Button(self)
        self.WAIT["text"] = "      Wait a certain time       "
        self.WAIT["command"] = self.wait
        self.WAIT.bind("<Enter>", lambda event: self.WAIT.configure(bg="orange"))
        self.WAIT.bind("<Leave>", lambda event: self.WAIT.configure(bg="white"))
        self.WAIT.grid(row = 10, column = 0, ipadx = 20, ipady = 10, pady = 10)


        #Create start comparing button
        self.SCREENSHOT = Button(self)
        self.SCREENSHOT["text"] = "                Screenshot                 "
        self.SCREENSHOT["command"] = self.screenshot
        self.SCREENSHOT.bind("<Enter>", lambda event: self.SCREENSHOT.configure(bg="orange"))
        self.SCREENSHOT.bind("<Leave>", lambda event: self.SCREENSHOT.configure(bg="white"))
        self.SCREENSHOT.grid(row = 12, column = 0, ipadx = 10, ipady = 10, pady = 10)


        #Create start comparing button
        self.GENERATE_SCRIPT = Button(self)
        self.GENERATE_SCRIPT["text"] = "                Generate Script                 "
        self.GENERATE_SCRIPT["command"] = self.generate_script
        self.GENERATE_SCRIPT.bind("<Enter>", lambda event: self.GENERATE_SCRIPT.configure(bg="green"))
        self.GENERATE_SCRIPT.bind("<Leave>", lambda event: self.GENERATE_SCRIPT.configure(bg="white"))
        self.GENERATE_SCRIPT.grid(row = 14, column = 0, ipadx = 10, ipady = 10, pady = 10)


        #Create text entry for folder A
        self.main_text = Text(self, width=100)
        self.main_text.grid(row = 2, column = 1, columnspan = 2, rowspan = 20, ipadx = 0, ipady = 10, pady = 10, padx = 0)


        #Create Emerson logo and place it in the GUI
        try:
            widget = Label(root, compound='top')
            widget.Logo = PhotoImage(file="logo2.gif")
            widget['image'] = widget.Logo
            widget.configure(width = 500, height = 100)
            widget.pack()
        except:
            self.Logo = Label(self, text = 'EMERSON PROCESS SOLUTION')
            self.Logo.grid(row = 21, columnspan = 3, padx = 300, pady = 20)






    #Packing all the components and create the GUI
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()








app = Application(master=root)
if os.path.exists(r'Emerson-Logo.ico'):
    root.iconbitmap(r'Emerson-Logo.ico')
app.mainloop()


