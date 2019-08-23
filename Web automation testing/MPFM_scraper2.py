#Company: Emerson Process Solution
#Name: Files comparison tool
#Author: Hiep Nguyen
#Released date: 08/19/2019
#version: v2.1
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


#initialize the GUI
root = Tk()
root.title("PWTTS files comparison tool v2.0 csv version")
root.geometry("840x500")
root.wm_minsize(860,620)

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
    #local shared variables between functions
    current_text = ''
    current_text = current_text + 'from selenium import webdriver' + '\n'
    current_text = current_text + 'from selenium.webdriver.common.keys import Keys' + '\n'
    current_text = current_text + 'import time' + '\n'
    current_text = current_text + 'from selenium.webdriver.support.ui import WebDriverWait' + '\n'
    current_text = current_text + 'from selenium.webdriver.support import expected_conditions as EC' + '\n'
    current_text = current_text + 'driver = webdriver.Chrome("C:/Python27/chromedriver")' + '\n'


    #Action to take when user click on browse folder A
    def address_goto(self):
        address = tkSimpleDialog.askstring('Input', 'Please enter a website address: ')
        self.current_text = self.current_text + 'driver.get("' + address + '")' + '\n' + '\n'
        self.Text_A.delete('1.0', END)
        self.Text_A.insert(INSERT, self.current_text) #put new value in the entry box

    #Action to take when user click on browse folder A
    def field_input(self):
        name = tkSimpleDialog.askstring('Input', 'Please enter name of the input field: ')
        input_info = tkSimpleDialog.askstring('Input', 'Please enter what to insert to input field: ')
        self.current_text = self.current_text + "elem = driver.find_element_by_name('" + name + "')" + '\n'
        self.current_text = self.current_text + "log_in.send_keys('" + input_info + "')" + '\n' + '\n'
        self.Text_A.delete('1.0', END)
        self.Text_A.insert(INSERT, self.current_text) #put new value in the entry box

    #Action to take when user click on browse output location
    def click(self):
        item = tkSimpleDialog.askstring('Input', 'Please enter id of item to be clicked ')
        self.current_text = self.current_text + 'try:' + '\n'
        self.current_text = self.current_text + '\twait = WebDriverWait(driver, 10)' + '\n'
        self.current_text = self.current_text + "\telement = wait.until(EC.element_to_be_clickable((By.ID, '" + item +  "')))" + '\n'
        self.current_text = self.current_text + "\tdriver.find_element_by_id('" + item + "').click()" + '\n'
        self.current_text = self.current_text + 'except:' + '\n'
        self.current_text = self.current_text + '\tpass' + '\n' + '\n'
        self.Text_A.delete('1.0', END)
        self.Text_A.insert(INSERT, self.current_text) #put new value in the entry box


    #Action to take when user click on compare button
    def screenshot(self):
        self.current_text = self.current_text + 'driver.save_screenshot(\'foo.png\')' + '\n' + '\n'
        self.Text_A.delete('1.0', END)
        self.Text_A.insert(INSERT, self.current_text) #put new value in the entry box
        

    #Create the user interface layout
    def createWidgets(self):
        #Create browse folder A button
        self.ADDRESS_GOTO = Button(self)
        self.ADDRESS_GOTO["text"] = "Go to address"
        self.ADDRESS_GOTO["command"] = self.address_goto
        self.ADDRESS_GOTO.bind("<Enter>", lambda event: self.ADDRESS_GOTO.configure(bg="orange"))
        self.ADDRESS_GOTO.bind("<Leave>", lambda event: self.ADDRESS_GOTO.configure(bg="white"))
        self.ADDRESS_GOTO.grid(row = 3, column = 0, ipadx = 40, ipady = 10, pady = 10)


        #Create browse folder B button
        self.FIELD_INPUT = Button(self)
        self.FIELD_INPUT["text"] = "Type input to field"
        self.FIELD_INPUT["command"] = self.field_input
        self.FIELD_INPUT.bind("<Enter>", lambda event: self.FIELD_INPUT.configure(bg="orange"))
        self.FIELD_INPUT.bind("<Leave>", lambda event: self.FIELD_INPUT.configure(bg="white"))
        self.FIELD_INPUT.grid(row = 6, column = 0, ipadx = 40, ipady = 10, pady = 10)

        #Create browse output location button
        self.CLICK = Button(self)
        self.CLICK["text"] = "Click on an item"
        self.CLICK["command"] = self.click
        self.CLICK.bind("<Enter>", lambda event: self.CLICK.configure(bg="orange"))
        self.CLICK.bind("<Leave>", lambda event: self.CLICK.configure(bg="white"))
        self.CLICK.grid(row = 9, column = 0, ipadx = 20, ipady = 10, pady = 10)


        #Create start comparing button
        self.SCREENSHOT = Button(self)
        self.SCREENSHOT["text"] = "Screenshot"
        self.SCREENSHOT["command"] = self.screenshot
        self.SCREENSHOT.bind("<Enter>", lambda event: self.SCREENSHOT.configure(bg="green"))
        self.SCREENSHOT.bind("<Leave>", lambda event: self.SCREENSHOT.configure(bg="white"))
        self.SCREENSHOT.grid(row = 15, column = 0, columnspan = 1, rowspan = 3, ipadx = 10, ipady = 10, pady = 10)

        #Create text entry for folder A
        self.Text_A = Text(self, width=100)
        self.Text_A.grid(row = 3, column = 1, columnspan = 2, rowspan = 5, ipadx = 0, ipady = 10, pady = 10, padx = 0)


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

        #Create label to create space
        self.Text_K = Label(self, text = '')
        self.Text_K.grid(row = 19, column = 0, pady = 10)




    #Packing all the components and create the GUI
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()








app = Application(master=root)
if os.path.exists(r'Emerson-Logo.ico'):
    root.iconbitmap(r'Emerson-Logo.ico')
app.mainloop()


