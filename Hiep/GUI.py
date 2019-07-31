#Company: Emerson Process Solution
#Name: Files comparison tool
#Author: Hiep Nguyen
#Released date: 07/17/2019
#version: v1.0

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


#initialize the GUI
root = Tk()
root.title("Emerson files comparison tool v2.0")
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
CheckVar3 = IntVar()
CheckVar4 = IntVar()
CheckVar5 = IntVar()





#Main application
class Application(Frame):
    #local shared variables between functions
    file1 = ''
    file2 = ''
    file3 = ''
    file4 = ''
    files_as_string_1 =[]
    files_as_string_2 =[]
    file_name_list = []
    file_pair_list = []
    file_format_list = []
    diff_total_list = []
    file_in_A_not_in_B = []
    file_in_B_not_in_A = []
    background_color = '#FFFF00'
    diff_color = '#89ED75'

    def setBgColor(self):
        hexstr = askcolor()[1]
        if hexstr:
            self.background_color = hexstr
            self.background_color_button.config(bg=hexstr)

    def setDfColor(self):
        hexstr = askcolor()[1]
        if hexstr:
            self.diff_color = hexstr
            self.diff_color_button.config(bg=hexstr)

    def reset(self):
        self.file1 = ''
        self.file2 = ''
        self.file3 = ''
        self.file4 = ''
        self.files_as_string_1 =[]
        self.files_as_string_2 =[]
        self.file_name_list = []
        self.file_pair_list = []
        self.file_format_list = []
        self.diff_total_list = []
        self.file_in_A_not_in_B = []
        self.file_in_B_not_in_A = []
        downloaded.set(0)
        downloaded_index.set(0)
        root.update()

    #Create 2 progress bar, one is for indexing process and the other for comparing process
    progress = ttk.Progressbar(root, orient = 'horizontal', variable= downloaded, mode = 'determinate')
    progress.pack(fill=BOTH, side = BOTTOM)
    label_progress = Label(wraplength = 490, text = 'Comparing...')
    label_progress.pack(side = BOTTOM)

    progress_index = ttk.Progressbar(root, orient = 'horizontal', variable= downloaded_index, mode = 'determinate')
    progress_index.pack(fill=BOTH, side = BOTTOM)
    label_progress = Label(wraplength = 490, text = 'Indexing...')
    label_progress.pack(side = BOTTOM)



    #Action to take when user click on browse folder A
    def browse_A(self):
        old = self.file1
        self.file1 = tkFileDialog.askdirectory()
        if self.file1 == '':
            self.file1 = old
        self.Text_A.delete(0, last=len(self.Text_A.get()))  #clear current value in the entry box
        self.Text_A.insert(0, self.file1) #put new value in the entry box

    #Action to take when user click on browse folder A
    def browse_B(self):
        old2 = self.file2
        self.file2 = tkFileDialog.askdirectory()
        if self.file2 == '':
            self.file2 = old2
        self.Text_B.delete(0, last=len(self.Text_B.get()))
        self.Text_B.insert(0, self.file2)

    #Action to take when user click on browse output location
    def browse_output(self):
        old3 = 'Default: same folder of the running program'
        self.file3 = tkFileDialog.askdirectory()
        if self.file3 == '':
            self.file3 = old3
        self.Text_C.delete(0, last=len(self.Text_C.get()))
        self.Text_C.insert(0, self.file3)

    #Action to take when user click on compare button
    def Compare(self):
        self.reset()
        if self.background_color == '':
            self.background_color = '#FFFF00'
        if self.diff_color == '':
            self.diff_color = '#89ED75'
        #Get 2 paths to the 2 folder being used for comparison from entry boxes and check their validity
        self.file1 = self.Text_A.get()
        self.file2 = self.Text_B.get()
        if os.path.exists(self.file1) is False or os.path.exists(self.file2) is False:
            if os.path.exists(self.file1) is False and os.path.exists(self.file2) is False:
                tkMessageBox.showinfo("Error", "Both path A and path B are not valid. Please check and try again.")
            elif os.path.exists(self.file1) is True and os.path.exists(self.file2) is False:
                tkMessageBox.showinfo("Error", "Path B not valid. Please check and try again.")
            elif os.path.exists(self.file1) is False and os.path.exists(self.file2) is True:
                tkMessageBox.showinfo("Error", "Path A not valid. Please check and try again.")
            return

        #Get output location path and check its validity
        self.file3 = self.Text_C.get()
        self.file4 = self.Text_E.get()
        if self.file4 == '':
            self.file4 = 'reportH2'
        if os.path.isdir(self.file3) is False and self.file3 != 'Default: same folder of the running program':
            tkMessageBox.showinfo("Error", "File output location not valid or not a folder. Please check and try again.")
            return

        #Check if the user is comparing 2 folders or 2 files and redirect the next action as approriate

        #Action to take if the user is comparing 2 files
        if os.path.isfile(self.file1) is True and os.path.isfile(self.file2) is True:
            self.compare_file()
        #Action to take if the user is comparing 2 folders
        elif os.path.isdir(self.file1) is True and os.path.isdir(self.file2) is True:
            self.compare()
        else:
        #Action to take if the user try to compare a folder with a file and vice versa
            tkMessageBox.showinfo("Error", "Please make sure path A and B are either both folders or both files location. Please check and try again")
            return

        if CheckVar5.get() == 1:
            current_path = os.getcwd().replace('\\','/') + '/' + 'reportH2.txt'
        else: current_path = os.getcwd().replace('\\','/') + '/' + 'reportH2.html'


        # if default and nothing special select, open tab if that option is checked
        # if not default, figure out what location that is. Then send the html and txt file there, either both or individually

        if self.file3 == 'Default: same folder of the running program' and (self.file4 == 'Default: reportH2.html' or self.file4 == 'Default: reportH2.txt'):
            if CheckVar2.get() == 1:
                webbrowser.open_new_tab('file:///' + current_path)
            self.Text_G.configure(text = '  Comparison process is completed !')
            return
        dest_folder = ''
        dest_name = ''
        if self.file3 == 'Default: same folder of the running program':
            dest_folder = os.getcwd().replace('\\','/') + '/'
        else:
            dest_folder = self.file3 + '/'

        if CheckVar5.get() == 0:
            if self.file4 == 'Default: reportH2.html':
                dest_name = 'reportH2.html'
            else:
                dest_name = self.file4 + '.html'
        else:
            if self.file4 == 'Default: reportH2.txt':
                dest_name = 'reportH2.txt'
            else:
                dest_name = self.file4 + '.txt'

        dest = dest_folder + dest_name
        shutil.move(current_path, dest)
        if CheckVar2.get() == 1:
            webbrowser.open_new_tab('file:///' + dest)
        self.Text_G.configure(text = '  Comparison process is completed !')
        return

        

    #Create the user interface layout
    def createWidgets(self):
        #Create browse folder A button
        self.BROWSE_A = Button(self)
        self.BROWSE_A["text"] = "Browse path A"
        self.BROWSE_A["command"] = self.browse_A
        self.BROWSE_A.bind("<Enter>", lambda event: self.BROWSE_A.configure(bg="orange"))
        self.BROWSE_A.bind("<Leave>", lambda event: self.BROWSE_A.configure(bg="white"))
        self.BROWSE_A.grid(row = 3, column = 0, ipadx = 40, ipady = 10, pady = 10)

        #Create browse folder B button
        self.BROWSE_B = Button(self)
        self.BROWSE_B["text"] = "Browse path B"
        self.BROWSE_B["command"] = self.browse_B
        self.BROWSE_B.bind("<Enter>", lambda event: self.BROWSE_B.configure(bg="orange"))
        self.BROWSE_B.bind("<Leave>", lambda event: self.BROWSE_B.configure(bg="white"))
        self.BROWSE_B.grid(row = 6, column = 0, ipadx = 40, ipady = 10, pady = 10)

        #Create browse output location button
        self.BROWSE_D = Button(self)
        self.BROWSE_D["text"] = "Browse output location"
        self.BROWSE_D["command"] = self.browse_output
        self.BROWSE_D.bind("<Enter>", lambda event: self.BROWSE_D.configure(bg="orange"))
        self.BROWSE_D.bind("<Leave>", lambda event: self.BROWSE_D.configure(bg="white"))
        self.BROWSE_D.grid(row = 9, column = 0, ipadx = 20, ipady = 10, pady = 10)


        #Create start comparing button
        self.BROWSE_C = Button(self)
        self.BROWSE_C["text"] = "Compare"
        self.BROWSE_C["command"] = self.Compare
        self.BROWSE_C.bind("<Enter>", lambda event: self.BROWSE_C.configure(bg="green"))
        self.BROWSE_C.bind("<Leave>", lambda event: self.BROWSE_C.configure(bg="white"))
        self.BROWSE_C.grid(row = 15, column = 0, columnspan = 1, rowspan = 3, ipadx = 10, ipady = 10, pady = 10)

        #Create text entry for folder A
        self.Text_A = Entry(self, width=100)
        self.Text_A.grid(row = 3, column = 1, columnspan = 2, ipadx = 0, ipady = 10, pady = 10, padx = 0)

        #Create text entry for folder B
        self.Text_B = Entry(self, width=100)
        self.Text_B.grid(row = 6, column = 1, columnspan = 2, ipadx = 0, ipady = 10, pady = 10, padx = 0)

        #Create text entry for output file's location
        self.Text_C = Entry(self, width=100)
        self.Text_C.insert(0, 'Default: same folder of the running program')
        self.Text_C.grid(row = 9, column = 1, columnspan = 2, ipadx = 0, ipady = 10, pady = 10, padx = 0)

        #Create label for text entry of report's name
        self.Text_F = Label(self, text = 'Name of report: ')
        self.Text_F.grid(row = 12, column = 0, ipadx = 10, ipady = 10, pady = 10, padx = 0)

        #Create text entry for name of the report
        self.Text_E = Entry(self, width=100)
        self.Text_E.insert(0, 'Default: reportH2.html')
        self.Text_E.grid(row = 12, column = 1, columnspan = 2, ipadx = 0, ipady = 10, pady = 10, padx = 0)

        #Create 2 checkbox for diff assist and open when done
        self.Check_A = Checkbutton(self, text = "Highlight differences in each pair of lines   ", variable = CheckVar1,onvalue = 1, offvalue = 0, width = 40)
        self.Check_A.grid(row = 15, column = 1, columnspan = 1, padx = 0)
        self.Check_B = Checkbutton(self, text = "Open report when done                                 ", variable = CheckVar2,onvalue = 1, offvalue = 0, width = 40)
        self.Check_B.grid(row = 16, column = 1, columnspan = 1)
        self.Check_D = Checkbutton(self, text = "Create exception traceback log                      ", variable = CheckVar4,onvalue = 1, offvalue = 0, width = 40)
        self.Check_D.grid(row = 17, column = 1, columnspan = 1)
        self.Check_Q = Checkbutton(self, text = "Quick Diff (generate the overall report only)", variable = CheckVar5,onvalue = 1, offvalue = 0, width = 40, command = self.disable_button)
        self.Check_Q.grid(row = 18, column = 1, columnspan = 1)

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

        #Create label to display what the program is doing
        self.Text_G = Label(self, text = '          Click Compare to begin the process...\n')
        self.Text_G.grid(row = 20, column = 0)

        self.background_color_button = Button(self, text='Background Color ', command=self.setBgColor,bg='#FFFF00')
        self.background_color_button.grid(row=15, column = 2, rowspan = 2, padx=20)
        self.background_color_button.bind("<Enter>", lambda event: self.background_color_button.configure(bg="#bfffff"))
        self.background_color_button.bind("<Leave>", lambda event: self.background_color_button.configure(bg=self.background_color))

        self.diff_color_button = Button(self, text='Differences Color   ', command=self.setDfColor, bg='#89ED75')
        self.diff_color_button.grid(row=17, column = 2, rowspan = 2, padx=20)
        self.diff_color_button.bind("<Enter>", lambda event: self.diff_color_button.configure(bg="#bfffff"))
        self.diff_color_button.bind("<Leave>", lambda event: self.diff_color_button.configure(bg=self.diff_color))


    #Packing all the components and create the GUI
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def disable_button(self):
        if CheckVar5.get() == 1:
            self.Check_A.configure(state = DISABLED)
            self.Check_A.deselect()
            self.Text_E.delete(0,len(self.Text_E.get()))
            self.Text_E.insert(0, 'Default: reportH2.txt')
        else:
            self.Check_A.configure(state = NORMAL)
            self.Check_A.select()
            self.Text_E.delete(0,len(self.Text_E.get()))
            self.Text_E.insert(0, 'Default: reportH2.html')



#Done with the GUI parts, now begin the actual comparing process


    #Function to compare the 2 folder
    def compare(self):
            #Create and get auxiliary document ready
            e = open('errors.txt', 'w+')
            e2 = open('trace_back_log.txt', 'w+')
            f = open("report_prep.txt", "w+")
            h = open("reportH.html", "w+")

            #Indexing the folder, preparing for the comparing process
            self.index_folder()

            #Get number of files and the quantity of each type
            number_of_files = len(self.files_as_string_1)
            file_name_quantity = {i:1 for i in self.file_name_list}

            #Set the number of portion in the progress bar
            Application.progress["maximum"] = number_of_files

            #Progress bar current value
            value = 0
            #Go through each file type available
            for current_file_index in range(number_of_files):
                #Update the progress bar
                value = value + 1
                downloaded.set(value)
                root.update()

                #Begin comparing
                try:
                    #Variables for keeping track and acts as flags for later use
                    no_difference = True
                    diff_total = 0
                    current_line_keeper = 0

                    #If there is multiple file with the same type, these 6 lines below would help differentiate them by assigning a number next to the file type
                    fileName =  str(self.file_name_list[current_file_index])
                    x = file_name_quantity[fileName.split()[0]]
                    if x > 1:
                        fileName = fileName + '(' + str(x) + ')'
                    file_name_quantity[fileName.split()[0]] = x + 1
                    self.file_name_list[current_file_index] = fileName

                    self.Text_G.configure(text = 'Comparing ' + fileName + ' files...')




                    #Getting the 2 current file type being compare
                    fileA = str(self.file_pair_list[current_file_index][0])
                    fileB = str(self.file_pair_list[current_file_index][1])

                    # Write current file type to report_prep.txt
                    f = open("report_prep.txt", "a+")
                    f.write("\n\n")
                    f.write("File type: " + fileName + "\n")
                    file_name_difference = ''
                    if fileA != fileB:
                        file_name_difference = '  (Note: file name is difference)'
                    f.write("Files being compare: " + fileA + '(A)' + "  and  " + fileB + '(B)' + file_name_difference + "\n")
                    f.write("Differences: " + "\n")

                    if CheckVar5.get() == 0:
                        # Write current file type being compare to reportH.html
                        h.write('<div id="' + fileName + '" class="tabcontent">' + '\n')
                        h.write('<table style="width:100%">' + '\n')
                        h.write('<tr>' + '\n')
                        h.write('   <th>' + 'Line A #' + '</th>' + '\n')
                        h.write('   <th>' + fileA + '</th>' + '\n')
                        h.write('   <th>' + 'Line B #' + '</th>' + '\n')
                        h.write('   <th>' + fileB + '</th>' + '\n')
                        h.write('</tr>' + '\n\n')




                    #Getting the content of the 2 files being compared:
                    current_file_A = self.files_as_string_1[current_file_index]
                    current_file_B = self.files_as_string_2[current_file_index]
                    current_file_B_original = [i for i in current_file_B] #Create backup of file B to keep the line number right later
                    #Note: file A's content do not need back up because instead of modifying it we are create a new list with only lines that are different

                    #Remove blank line from content of file B, using temp to iterate the file's content without modifying it at the same time
                    current_file_B_temp = [i for i in current_file_B]
                    for line in current_file_B_temp:
                        if len(line.replace(' ', '').replace('\n','').replace('\r','')) == 0:
                            current_file_B_original[current_file_B_original.index(line)] = None
                            current_file_B.remove(line)

                    #Prepare storage for lines that are different found in file A
                    file_A_diff = []

                    #Prepare storage for lines that are different found in file A
                    for current_line in current_file_A:
                        if len(current_line.replace(' ', '').replace('\n','').replace('\r','')) == 0:
                            continue
                        if current_line in current_file_B:
                            current_file_B_original[current_file_B_original.index(current_line)] = None
                            current_file_B.remove(current_line)

                            current_file_A[current_file_A.index(current_line)] = None
                        else:
                            diff_total = diff_total + 1
                            file_A_diff.append(current_line)


                    #if there is line remain in file A or B, there is at least some difference between them
                    if len(current_file_B) != 0 and len(current_file_A)!=0:
                        no_difference = False

                    #Create a list of lines that are still left in B that were not match up with any line in A
                    line_in_B_left = [i for i in current_file_B]

                    if CheckVar5.get() == 1:
                        self.diff_total_list.append(len(line_in_B_left) + len(file_A_diff))
                        #Get the current difference as ordinal number
                        current_file_A_temp = [i for i in current_file_A]

                        #Write to the overall text report the current file being compare and the differences between them
                        f.write('Line in ' + fileA + '(A)' + ' that are not in ' + fileB + '(B)' + ':' + "\n")
                        if len(file_A_diff) == 0:
                            f.write('   None' + '\n')
                        for current_line in file_A_diff:
                            f.write('   line ' +  str(current_file_A_temp.index(current_line)+ 1) + ': ' + current_line + "\n")
                            current_file_A_temp[current_file_A_temp.index(current_line)] = None

                        current_file_B_original_temp = [i for i in current_file_B_original]
                        f.write('Line in ' + fileB + '(B)' + ' that are not in ' + fileA + '(A)' + ':' + "\n")
                        if len(current_file_B) == 0:
                            f.write('   None' + '\n')
                        else:
                            for current_line in current_file_B:
                                f.write('   line ' +  str(current_file_B_original_temp.index(current_line)+ 1) + ': ' + current_line + "\n")
                                current_file_B_original_temp[current_file_B_original_temp.index(current_line)] = None
                        continue


                    #Create an 2D list of similarity index between each file of A to each file of B and vice versa
                    similarity_percentage = [[0 for i in range(len(current_file_B))] for j in range(len(file_A_diff))]

                    #Getting the similarity index of every pair of file between A and B and store it to the list created earlier
                    for i in range(len(file_A_diff)):
                        for j in range(len(current_file_B)):
                            similarity_percentage[i][j] = SequenceMatcher(None, file_A_diff[i], current_file_B[j]).ratio()

                    #Create most and second most similar line for every line in file A and file B
                    most_similar_A = [0 for i in range(len(file_A_diff))]
                    most_similar_B = [0 for i in range(len(current_file_B))]
                    second_most_similar_A = [0 for i in range(len(file_A_diff))]
                    second_most_similar_B = [0 for i in range(len(current_file_B))]

                    #Fill in the most and second most similar line list for every line in A
                    for i in range(len(file_A_diff)):
                        highest_percentage = None
                        highest_percentage_index = None
                        second_highest_percentage_index = None
                        for j in range(len(current_file_B)):
                            if similarity_percentage[i][j] > highest_percentage:
                                second_highest_percentage_index = highest_percentage_index
                                highest_percentage_index = j
                                highest_percentage = similarity_percentage[i][j]
                        most_similar_A[i] = highest_percentage_index
                        second_most_similar_A[i] = second_highest_percentage_index

                    #Fill in the most and second most similar line list for every line in B
                    for j in range(len(current_file_B)):
                        highest_percentage = None
                        highest_percentage_index = None
                        second_highest_percentage_index = None
                        for i in range(len(file_A_diff)):
                            if similarity_percentage[i][j] > highest_percentage:
                                second_highest_percentage_index = highest_percentage_index
                                highest_percentage_index = i
                                highest_percentage = similarity_percentage[i][j]
                        most_similar_B[j] = highest_percentage_index
                        second_most_similar_B[j] = second_highest_percentage_index


                    #Get the current difference as ordinal number
                    diff_id = str(diff_total)

                    current_file_A_temp = [i for i in current_file_A]

                    #Write to the overall text report the current file being compare and the differences between them
                    f.write('Line in ' + fileA + '(A)' + ' that are not in ' + fileB + '(B)' + ':' + "\n")
                    if len(file_A_diff) == 0:
                        f.write('   None' + '\n')
                    for current_line in file_A_diff:
                        f.write('   line ' +  str(current_file_A_temp.index(current_line)+ 1) + ': ' + current_line.replace('<','&lt;').replace('>', '&gt;') + "\n")
                        current_file_A_temp[current_file_A_temp.index(current_line)] = None

                    current_file_B_original_temp = [i for i in current_file_B_original]
                    f.write('Line in ' + fileB + '(B)' + ' that are not in ' + fileA + '(A)' + ':' + "\n")
                    if len(current_file_B) == 0:
                        f.write('   None' + '\n')
                    else:
                        for current_line in current_file_B:
                            f.write('   line ' +  str(current_file_B_original_temp.index(current_line)+ 1) + ': ' + current_line.replace('<','&lt;').replace('>', '&gt;') + "\n")
                            current_file_B_original_temp[current_file_B_original_temp.index(current_line)] = None

                    #After done writing to the general text report, now writing to the html report as we sorting the lines side by side
                    for current_line in file_A_diff:
                        #Write line number of current line in file A's list of lines that are different
                        h.write('<tr>' + '\n')
                        h.write('  <td>' + str(current_file_A.index(current_line)+ 1) + '</td>' + '\n')
                        current_file_A[current_file_A.index(current_line)] = None
                        #Write current line in file A
                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')


                        #Get index of current line in A, get the most similar line in B of current line in A
                        a = file_A_diff.index(current_line)
                        file_A_diff[a] = None
                        b = most_similar_A[a]


                        #If b is not empty then go ahead and check for mutual similarity
                        if b != None and len(current_file_B) > 0:
                            #if the most similar line in B of current line in A also has current line in A as its most similar line
                            # #..., then we match them together
                            if most_similar_B[b] == a:
                                h.write(self.character_highlight(current_line, current_file_B[b]))
                                h.write('   </td>' + '\n')

                                h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                                current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')


                                h.write(self.character_highlight(current_file_B[b], current_line))
                                line_in_B_left.remove(current_file_B[b])
                                h.write('  </td>' + '\n')
                                h.write('</tr>' + '\n\n')
                                continue

                            #Else check if the most similar line in B of current line in A has current line in A as its second most similar line
                            elif second_most_similar_B[b] == a:
                                a2 = most_similar_B[b]
                                #If its most similar line does not have itself as most similar line, then we match the line in B with current line in A
                                if most_similar_A[a2] != b:
                                    h.write(self.character_highlight(current_line,current_file_B[b]))
                                    h.write('   </td>' + '\n')

                                    h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                                    current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                                    h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                                    h.write(self.character_highlight(current_file_B[b],current_line))
                                    line_in_B_left.remove(current_file_B[b])
                                    h.write('  </td>' + '\n')
                                    h.write('</tr>' + '\n\n')
                                    continue
                            else:
                                h.write(self.escapeHtml(current_line))
                                h.write('   </td>' + '\n')

                        else:
                            h.write(self.escapeHtml(current_line))
                            h.write('   </td>' + '\n')


                        #If there is no similar line in B got matched with current line in A, count it as a missing line and put the missing line (a dash) on the other side
                        h.write('  <td>' + ' - ' + '</td>' + '\n')
                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                        h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                        h.write(' </td>' + '\n')
                        h.write('</tr>' + '\n\n')

                    #Now after all the remaining line in A were taken care of, whatever left in B will be missing line,
                    #since if there was a similar line in A it would have already been matched earlier
                    for current_line in line_in_B_left:
                        h.write('<tr>' + '\n')
                        h.write('  <td>' + ' - ' + '</td>' + '\n')

                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                        h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                        h.write(' </td>' + '\n')

                        h.write('  <td>' + str(current_file_B_original.index(current_line) + 1) + '</td>' + '\n')
                        current_file_B_original[current_file_B_original.index(current_line)] = None

                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                        h.write(self.escapeHtml(current_line))
                        h.write('   </td>' + '\n')

                        diff_total = diff_total + 1
                        h.write('</tr>' + '\n\n')

                    #Add the total number of differences to the list of differences for each file
                    self.diff_total_list.append(diff_total)
                    h.write('</table>' + "\n")
                    h.write('</div>' + '\n\n')

                    #If error occurs, continue checking other file and document it in the overall report
                except:
                    e2 = open('trace_back_log.txt', 'a+')
                    e2.write(traceback.format_exc() + '\n')
                    e = open('errors.txt', 'a+')
                    e.write('   Errors occured in file: ' + fileName + '. Manual inspection required' + '\n')
                    continue

            #finish the current report and close auxiliary supporting document
            f.write(' \n \n \n - End of Report -')
            f.close()
            h.close()
            e.close()
            try:
                e2.close()
            except:
                pass

            #Gather up all the document and write the final reports
            self.writeEnding()

            #Delete the auxiliary documents
            current_path = os.getcwd().replace('\\','/') + '/'
            if CheckVar4.get() == 0:
                os.remove(current_path + 'trace_back_log.txt')    
            os.remove(current_path + 'errors.txt')
            os.remove(current_path + 'reportH.html')
            os.remove(current_path + 'testing.txt')
            os.remove(current_path + 'testing2.txt')
            if CheckVar5.get() == 1:
                os.remove(current_path + 'reportH2.html')

    #Function to compare the 2 files individually
    def compare_file(self):
        #Create and open auxiliary documents
        e = open('errors.txt', 'w+')
        e2 = open('trace_back_log.txt', 'w+')
        f = open("report_prep.txt", "w+")
        h = open("reportH.html", "w+")

        #Index the file and prepare for comparing process
        self.index_file()

        #Set number of files
        number_of_files = 1

        #Set progress bar's number of portion (in this case only 1 files need to be processed)
        Application.progress["maximum"] = 1

        try:
            no_difference = True
            diff_total = 0
            current_line_keeper = 0
            fileName =  str(self.file_name_list[0])

            self.Text_G.configure(text = 'Comparing ' + fileName + ' files...')



            #Getting the 2 current file type being compare
            fileA = str(self.file_pair_list[0][0])
            fileB = str(self.file_pair_list[0][1])

            # Write current file type to report_prep.txt
            f = open("report_prep.txt", "a+")
            f.write("\n\n")
            f.write("File type: " + fileName + "\n")
            file_name_difference = ''
            if fileA != fileB:
                file_name_difference = '  (Note: file name is difference)'
            f.write("Files being compare: " + fileA + '(A)' + "  and  " + fileB + '(B)' + file_name_difference + "\n")
            f.write("Differences: " + "\n")

            if CheckVar5.get() == 0:
                # Write current file type being compare to reportH.html
                h.write('<div id="' + fileName + '" class="tabcontent">' + '\n')
                h.write('<table style="width:100%">' + '\n')
                h.write('<tr>' + '\n')
                h.write('   <th>' + 'Line A #' + '</th>' + '\n')
                h.write('   <th>' + fileA + '</th>' + '\n')
                h.write('   <th>' + 'Line B #' + '</th>' + '\n')
                h.write('   <th>' + fileB + '</th>' + '\n')
                h.write('</tr>' + '\n\n')

            #Getting the content of the 2 files being compared:
            current_file_A = self.files_as_string_1[0]
            current_file_B = self.files_as_string_2[0]
            current_file_B_original = [i for i in current_file_B] #Create backup of file B to keep the line number right later
            #Note: file A's content do not need back up because instead of modifying it we are create a new list with only lines that are different

            #Remove blank line from content of file B, using temp to iterate the file's content without modifying it at the same time
            current_file_B_temp = [i for i in current_file_B]
            for line in current_file_B_temp:
                if len(line.replace(' ', '').replace('\n','').replace('\r','')) == 0:
                    current_file_B_original[current_file_B_original.index(line)] = None
                    current_file_B.remove(line)

            #Prepare storage for lines that are different found in file A
            file_A_diff = []

            #Prepare storage for lines that are different found in file A
            for current_line in current_file_A:
                if len(current_line.replace(' ','').replace('\n','').replace('\r','')) == 0:
                    continue
                if current_line in current_file_B:
                    current_file_B_original[current_file_B_original.index(current_line)] = None
                    current_file_B.remove(current_line)
                else:
                    diff_total = diff_total + 1
                    file_A_diff.append(current_line)

            #if there is line remain in file A or B, there is at least some difference between them
            if len(current_file_B) != 0 and len(current_file_A)!=0:
                no_difference = False

            #Create a list of lines that are still left in B that were not match up with any line in A
            line_in_B_left = [i for i in current_file_B]

            if CheckVar5.get() == 1:
                self.diff_total_list.append(len(line_in_B_left) + len(file_A_diff))
                #Get the current difference as ordinal number
                current_file_A_temp = [i for i in current_file_A]

                #Write to the overall text report the current file being compare and the differences between them
                f.write('Line in ' + fileA + '(A)' + ' that are not in ' + fileB + '(B)' + ':' + "\n")
                if len(file_A_diff) == 0:
                    f.write('   None' + '\n')
                for current_line in file_A_diff:
                    f.write('   line ' +  str(current_file_A_temp.index(current_line)+ 1) + ': ' + current_line + "\n")
                    current_file_A_temp[current_file_A_temp.index(current_line)] = None

                current_file_B_original_temp = [i for i in current_file_B_original]
                f.write('Line in ' + fileB + '(B)' + ' that are not in ' + fileA + '(A)' + ':' + "\n")
                if len(current_file_B) == 0:
                    f.write('   None' + '\n')
                else:
                    for current_line in current_file_B:
                        f.write('   line ' +  str(current_file_B_original_temp.index(current_line)+ 1) + ': ' + current_line + "\n")
                        current_file_B_original_temp[current_file_B_original_temp.index(current_line)] = None
                return







            #Create an 2D list of similarity index between each file of A to each file of B and vice versa
            similarity_percentage = [[0 for i in range(len(current_file_B))] for j in range(len(file_A_diff))]

            #Getting the similarity index of every pair of file between A and B and store it to the list created earlier
            for i in range(len(file_A_diff)):
                for j in range(len(current_file_B)):
                    similarity_percentage[i][j] = SequenceMatcher(None, file_A_diff[i], current_file_B[j]).ratio()


            #Create most and second most similar line for every line in file A and file B
            most_similar_A = [0 for i in range(len(file_A_diff))]
            most_similar_B = [0 for i in range(len(current_file_B))]
            second_most_similar_A = [0 for i in range(len(file_A_diff))]
            second_most_similar_B = [0 for i in range(len(current_file_B))]

            #Fill in the most and second most similar line list for every line in A
            for i in range(len(file_A_diff)):
                highest_percentage = None
                highest_percentage_index = None
                second_highest_percentage_index = None
                for j in range(len(current_file_B)):
                    if similarity_percentage[i][j] > highest_percentage:
                        second_highest_percentage_index = highest_percentage_index
                        highest_percentage_index = j
                        highest_percentage = similarity_percentage[i][j]
                most_similar_A[i] = highest_percentage_index
                second_most_similar_A[i] = second_highest_percentage_index

            #Fill in the most and second most similar line list for every line in B
            for j in range(len(current_file_B)):
                highest_percentage = None
                highest_percentage_index = None
                second_highest_percentage_index = None
                for i in range(len(file_A_diff)):
                    if similarity_percentage[i][j] > highest_percentage:
                        second_highest_percentage_index = highest_percentage_index
                        highest_percentage_index = i
                        highest_percentage = similarity_percentage[i][j]
                most_similar_B[j] = highest_percentage_index
                second_most_similar_B[j] = second_highest_percentage_index


            #Get the current difference as ordinal number
            diff_id = str(diff_total)

            current_file_A_temp = [i for i in current_file_A]

            #Write to the overall text report the current file being compare and the differences between them
            f.write('Line in ' + fileA + '(A)' + ' that are not in ' + fileB + '(B)' + ':' + "\n")
            if len(file_A_diff) == 0:
                f.write('   None' + '\n')
            for current_line in file_A_diff:
                f.write('   line ' +  str(current_file_A_temp.index(current_line)+ 1) + ': ' + current_line.replace('<','&lt;').replace('>', '&gt;') + "\n")
                current_file_A_temp[current_file_A_temp.index(current_line)] = None


            current_file_B_original_temp = [i for i in current_file_B_original]
            f.write('Line in ' + fileB + '(B)' + ' that are not in ' + fileA + '(A)' + ':' + "\n")
            if len(current_file_B) == 0:
                f.write('   None' + '\n')
            else:
                for current_line in current_file_B:
                    f.write('   line ' +  str(current_file_B_original_temp.index(current_line)+ 1) + ': ' + current_line.replace('<','&lt;').replace('>', '&gt;') + "\n")
                    current_file_B_original_temp[current_file_B_original_temp.index(current_line)] = None

            #After done writing to the general text report, now writing to the html report as we sorting the lines side by side
            for current_line in file_A_diff:
                #Write line number of current line in file A's list of lines that are different
                h.write('<tr>' + '\n')
                h.write('  <td>' + str(current_file_A.index(current_line)+ 1) + '</td>' + '\n')
                current_file_A[current_file_A.index(current_line)] = None
                #Write current line in file A
                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')


                #Get index of current line in A, get the most similar line in B of current line in A
                a = file_A_diff.index(current_line)
                file_A_diff[a] = None
                b = most_similar_A[a]

                #If b is not empty then go ahead and check for mutual similarity
                if b != None and len(current_file_B) > 0:
                    #if the most similar line in B of current line in A also has current line in A as its most similar line
                    # #..., then we match them together
                    if most_similar_B[b] == a:
                        h.write(self.character_highlight(current_file_B[b], current_line))
                        h.write('   </td>' + '\n')

                        h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                        current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')

                        h.write(self.character_highlight(current_line, current_file_B[b]))
                        line_in_B_left.remove(current_file_B[b])
                        h.write('  </td>' + '\n')
                        h.write('</tr>' + '\n\n')
                        continue

                    #Else check if the most similar line in B of current line in A has current line in A as its second most similar line
                    elif second_most_similar_B[b] == a:
                        a2 = most_similar_B[b]
                        #If its most similar line does not have itself as most similar line, then we match the line in B with current line in A
                        if most_similar_A[a2] != b:
                            h.write(self.character_highlight(current_line,current_file_B[b]))
                            h.write('   </td>' + '\n')

                            h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                            current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                            h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                            h.write(self.character_highlight(current_file_B[b],current_line))
                            line_in_B_left.remove(current_file_B[b])
                            h.write('  </td>' + '\n')
                            h.write('</tr>' + '\n\n')
                            continue
                    else:
                        h.write(self.escapeHtml(current_line))
                        h.write('   </td>' + '\n')
                else:
                    h.write(self.escapeHtml(current_line))
                    h.write('   </td>' + '\n')




                #If there is no similar line in B got matched with current line in A, count it as a missing line and put the missing line (a dash) on the other side
                h.write('  <td>' + ' - ' + '</td>' + '\n')
                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                h.write(' </td>' + '\n')
                h.write('</tr>' + '\n\n')

            #Now after all the remaining line in A were taken care of, whatever left in B will be missing line,
            #since if there was a similar line in A it would have already been matched earlier
            for current_line in line_in_B_left:
                h.write('<tr>' + '\n')
                h.write('  <td>' + ' - ' + '</td>' + '\n')

                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                h.write(' </td>' + '\n')

                h.write('  <td>' + str(current_file_B_original.index(current_line) + 1) + '</td>' + '\n')
                current_file_B_original[current_file_B_original.index(current_line)] = None

                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: ' + self.background_color + '">')
                h.write(self.escapeHtml(current_line))
                h.write('   </td>' + '\n')

                diff_total = diff_total + 1
                h.write('</tr>' + '\n\n')

            #Add the total number of differences to the list of differences for each file
            self.diff_total_list.append(diff_total)
            h.write('</table>' + "\n")
            h.write('</div>' + '\n\n')

            #If error occurs, continue checking other file and document it in the overall report
        except:
            e2 = open('trace_back_log.txt', 'a+')
            e2.write(traceback.format_exc() + '\n')
            e = open('errors.txt', 'a+')
            e.write('   Errors occured in file: ' + fileName + '. Manual inspection required' + '\n')


        downloaded.set(1)
        root.update()

        #finish the current report and close auxiliary supporting document
        f.write(' \n \n \n - End of Report -')
        f.close()
        h.close()
        e.close()
        try:
            e2.close()
        except:
            pass


        #Gather up all the document and write the final reports
        self.writeEnding()

        #Delete the auxiliary documents
        current_path = os.getcwd().replace('\\','/') + '/'
        if CheckVar4.get() == 0:
            os.remove(current_path + 'trace_back_log.txt')
        os.remove(current_path + 'errors.txt')
        os.remove(current_path + 'reportH.html')
        os.remove(current_path + 'testing.txt')
        os.remove(current_path + 'testing2.txt')
        if CheckVar5.get() == 1:
            os.remove(current_path + 'reportH2.html')



#line by line character highlights
    def character_highlight(self, line_a, line_b):
        if CheckVar1.get() == 0:
            return self.escapeHtml(line_a)
        #line_a = str(line_a).rstrip().lstrip()
        #line_b = str(line_b).rstrip().lstrip()
        ret = ''
        len_a = len(line_a)
        len_b = len(line_b)
        len_used = len_a
        top_down = 0
        bottom_up = len_used - 1
        if len_a > len_b:
            len_used = len_b
        diff = 0
        diff_bottom = 0
        for i in range(len_used):
            if line_a[i] != line_b[i]:
                diff = 1
                top_down = i
                break

        end_b = len_b - 1
        for i in range(len_a-1, -1, -1):
            if line_a[i] != line_b[end_b]:
                diff = 1
                diff_bottom = 1
                bottom_up = i
                break
            end_b = end_b - 1

        flag = 0
        if bottom_up < top_down:
            flag = 1
            holder = top_down
            top_down = bottom_up
            bottom_up = holder
        if diff == 0 or ((bottom_up-top_down) == (len_a-1) and flag == 1):
            for i in range(len_a):
                ret = ret + line_a[i]
        else:
            for i in range(top_down):
                ret = ret + line_a[i]
            ret = ret + '+=^font style=#$@background-color: ' + self.diff_color + '#$@^=+'
            if diff_bottom == 0:
                bottom_up = top_down
            for i in range(top_down, bottom_up+1):
                ret = ret + line_a [i].replace(' ', '^$^nbsp;')
            ret = ret + '+=^/font^=+'
            for i in range(bottom_up+1, len_a):
                ret = ret + line_a[i]


        ret = self.escapeHtml(ret)
        ret = ret.replace('+=^', '<').replace('^=+', '>').replace('#$@','"').replace('^$^', '&')
        return ret

    #Replacing unsafe characters with acceptable ones before writing it to the HTML document
    def escapeHtml(self, unsafe):
        safe = unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace("'", "&#039;");
        return safe

    #Gather the auxiliary documents and use them to write the final report
    def writeEnding(self):
        #Write the final overall report
        f = open("reportH2.txt", "w+")
        f.write("Time: " + str(datetime.datetime.now()) + "\n")
        f.write("Overall result: " + "\n")
        for i in range(len(self.file_name_list)):
            f.write("      " + self.file_name_list[i] + ":  " + self.file_pair_list[i][0] + ' (' + self.file_format_list[i][0] + ') ' + " and " + self.file_pair_list[i][1] + ' (' + self.file_format_list[i][1] + ') ' + "   -   " + str(self.diff_total_list[i]) + " differences" + "\n")

        if len(self.file_in_A_not_in_B) != 0 or len(self.file_in_B_not_in_A) != 0:
            f.write('Notes: ' + '\n')
            if CheckVar5.get() == 0:
                f.write('</pre>' + '\n')
                for i in self.file_in_A_not_in_B:
                    f.write('<p style="background-color: ' + self.background_color + ';display:table">   File type ' + i + ' is in folder A but not in folder B </p>' + '\n')
                for i in self.file_in_B_not_in_A:
                    f.write('<p style="background-color: ' + self.background_color + ';display:table">   File type ' + i + ' is in folder B but not in folder A </p>' + '\n')
                f.write('<pre>' + '\n')
            else:
                f.write('\n\n')
                for i in self.file_in_A_not_in_B:
                    f.write('-----> File type ' + i + ' is in folder A but not in folder B' + '\n')
                for i in self.file_in_B_not_in_A:
                    f.write('-----> File type ' + i + ' is in folder B but not in folder A' + '\n')
                f.write('\n\n')

            for i in range(len(self.file_name_list)):
                if self.file_pair_list[i][0] != self.file_pair_list[i][1] and self.file_format_list[i][0] == self.file_format_list[i][1]:
                    f.write('   ' + self.file_name_list[i])
                    f.write('  : file names are different' + '\n')
                elif self.file_pair_list[i][0] == self.file_pair_list[i][1] and self.file_format_list[i][0] != self.file_format_list[i][1]:
                    f.write('   ' + self.file_name_list[i])
                    f.write('  : file\'s encodings format are different' + '\n')
                elif self.file_pair_list[i][0] != self.file_pair_list[i][1] and self.file_format_list[i][0] != self.file_format_list[i][1]:
                    f.write('   ' + self.file_name_list[i])
                    f.write('  : file names and encoding format are different' + '\n')

        f.write('Errors encountered:' + '\n')
        if len(open('errors.txt', 'r').read()) == 0:
            f.write('       None' + '\n')
        else:
            f.write(open('errors.txt', 'r').read())

        f.write(open("report_prep.txt", 'r').read())
        f.close()
        os.remove('report_prep.txt')

        if CheckVar5.get() == 0:
            #Write the html report
            number_of_files = len(self.files_as_string_1)
            h = open("reportH2.html", "w+")
            #write the header for html report
            self.writeHeader(h)

            h.write('<div class="tab">' + "\n")
            h.write('          <button class="tablinks" onmouseover="openFile(event, \'' + 'Overall result' + '\')"'  + '>' + 'Overall result' + '</button>' + "\n")
            for current_file_index in range(number_of_files):
                fileName = str(self.file_name_list[current_file_index])
                color = '#ccffee"'
                if self.diff_total_list[current_file_index] > 0:
                    color = '#ff9999"'
                h.write(
                    '          <button class="tablinks" onmouseover="openFile(event, \'' + fileName + '\')"' + 'style="background-color:' + color + '>'  + fileName + '</button>' + "\n")
            h.write('    </div>')

            h.write(open("reportH.html", 'r').read())
            h.write('<div id="Overall result" class="tabcontent">' + '\n')
            h.write('<pre>' + open("reportH2.txt", 'r').read() + '</pre>' + '\n')
            h.write('</div>')
            h.write('''
            <div class="clearfix"></div>
            <script>
            ''')
            #write the footer for the html report
            self.writeFooter(h)

    #Indexing the folder and prepare it for the report
    def index_folder(self):
        #Get the paths to 2 folder being compared
        folder1_path = self.file1
        folder2_path = self.file2

        #Get all the files inside that folder
        files_in_folder1 = os.listdir(folder1_path)
        files_in_folder2 = os.listdir(folder2_path)

        #Set the total portions needed for the progress bar
        Application.progress_index["maximum"] = len(files_in_folder1)

        files_in_folder1_temp = [i for i in files_in_folder1]
        files_in_folder2_temp = [i for i in files_in_folder2]

        # files_in_folder1_temp
        #print files_in_folder2_temp
        #Check the folder's content between the 2 folder
        past_A = []
        for file1 in files_in_folder1:
            found = False
            for file2 in files_in_folder2_temp:
                if file2 == None:
                    continue
                if file1.split(".")[1] == file2.split('.')[1]:
                    found = True
                    files_in_folder2_temp[files_in_folder2_temp.index(file2)] = None
                    break
            if found == False:
                temp = file1.split('.')[1]
                if temp in self.file_in_A_not_in_B:
                    temp = file1.split('.')[1] + '(Duplicate)'
                self.file_in_A_not_in_B.append(temp)
            past_A.append(file1.split('.')[1])

        past_B = []
        for file2 in files_in_folder2:
            found = False
            for file1 in files_in_folder1_temp:
                if file1 == None:
                    continue
                if file2.split(".")[1] == file1.split('.')[1]:
                    found = True
                    files_in_folder1_temp[files_in_folder1_temp.index(file1)] = None
                    break
            if found == False:
                temp = file2.split('.')[1]
                if temp in past_B:
                    temp = file2.split('.')[1] + '(Duplicate)'
                self.file_in_B_not_in_A.append(temp)
            past_B.append(file2.split('.')[1])

        #Going through each file in folder 1 and find the correspond file in folder 2
        value = 0
        for file1 in files_in_folder1:
            self.Text_G.configure(text = '      Preparing the files before comparison...\n' + 'indexing ' + file1 + '...')
            #Update the progress bar
            value = value + 1
            downloaded_index.set(value)
            root.update()

            try:
                current_extension = file1.split(".")[1]

                #Hard-coded to save time, since the program can detect it later anyway however it gonna take awhile so we just gonna take it out before that happen to save time.
                if(current_extension == 'fm8'):
                    e = open('errors.txt', 'a+')
                    e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n' )
                    continue

                #Get the path to current file in folder 1(or A)
                current_file_folder1 = str(folder1_path) + "\\" + file1

                #Check the encoding format for current file
                raw = open(current_file_folder1,'rb').read()
                result = chardet.detect(raw)
                char = result['encoding']
                #If the encoding format is not the usual one we would just skip it and leave it for manual inspection
                if char not in ['ascii', 'UTF-8','UTF-16','UTF-8-SIG']:
                    e = open('errors.txt', 'a+')
                    e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n')
                    continue

                #Go through the second folder and search for corresponsing file
                for file2_prep in files_in_folder2:
                    file2 = file2_prep

                    #if same extension, then we found the corresponding file for current file in folder 1(or A)
                    if file2.split(".")[1] == current_extension:
                        #Get the path to current file in folder 2(or B)
                        current_file_folder2 = str(folder2_path) + "\\" + file2

                        #Check for compatible encoding format
                        raw = open(current_file_folder2,'rb').read()
                        result = chardet.detect(raw)
                        char2 = result['encoding']
                        #if the encoding format is not compatible, skip it.
                        if char2 not in ['ascii', 'UTF-8','UTF-16','UTF-8-SIG']:
                            e = open('errors.txt', 'a+')
                            e.write('   File ' + file2 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n')
                            continue

                        #When there are multiple file with the same extension, they sometimes have the same name and sometimes they do not,
                        #... when that happen, we just using the just first come first serve system, however in this case we want to make sure
                        #... that the ddinstall.ini file were matched with the right one in the other folder, since they are usually have the same name
                        if (current_extension == 'ini') and (file1 != file2):
                            continue

                        #If this is really the corresponding file, we gonna match them up and remove them from current list of files in folder 2 so we
                        #... would not be using it more than once.
                        files_in_folder2.remove(file2_prep)

                        #Read the 2 corresponding text file from folde 1 and 2
                        text_file_1 = open(current_file_folder1, 'r').read()
                        text_file_2 = open(current_file_folder2, 'r').read()

                        #prepare a list to store the lines in these files
                        current_file_as_string_list_1 = []
                        current_file_as_string_list_2 = []

                        #adding lines from current file in folder 1 to the string list of the current file:
                        #... if some characters are odd, convert it to utf-8
                        f = open('testing.txt', 'w+')
                        for line in text_file_1:
                            result = chardet.detect(line)
                            char = result['encoding']
                            if char not in ['utf-8', 'utf-16', 'ascii']:
                                try:
                                    line = line.decode(char).encode('utf-8','ignore')
                                except:
                                    line = line.decode('latin-1').encode('utf-8','ignore')
                            if line == '\x00':
                                continue
                            f.write(line)
                        f.close()
                        f = open('testing.txt', 'r').readlines()
                        for line in f:
                            current_file_as_string_list_1.append(line)

                        #adding lines from current file in folder 1 to the string list of the current file
                        #... if some characters are odd, convert it to utf-8
                        f = open('testing2.txt', 'w+')
                        for line in text_file_2:
                            result = chardet.detect(line)
                            char = result['encoding']
                            if char not in ['utf-8', 'utf-16', 'ascii']:
                                try:
                                    line = line.decode(char).encode('utf-8','ignore')
                                except:
                                    line = line.decode('latin-1').encode('utf-8','ignore')
                            if line == '\x00':
                                continue
                            f.write(line)
                        f.close()
                        f = open('testing2.txt', 'r').readlines()
                        for line in f:
                            current_file_as_string_list_2.append(line)

                        #Add the 2 string list to the list of all the file's content
                        self.files_as_string_1.append(current_file_as_string_list_1)
                        self.files_as_string_2.append(current_file_as_string_list_2)

                        #Add the current file pair to the file pair list
                        current_file_pair = [file1,file2]
                        #Add the current format to the current format pair list
                        current_format_pair = [char, char2]
                        #Add thhe file name, pair and format pair to the overall lists
                        self.file_name_list.append(current_extension)
                        self.file_pair_list.append(current_file_pair)
                        self.file_format_list.append(current_format_pair)
                        break

            #If there were any error occured during the process, write it to the errors file log
            except:
                e = open('errors.txt', 'a+')
                e.write('   Errors occurred in file: ' + file1 + '.\n')
                e2 = open('trace_back_log.txt', 'a+')
                e2.write(traceback.format_exc() + '\n')
                continue

    #index the individual file
    def index_file(self):
        #getting 2 file names
        file_path_A = self.file1
        file1 = os.path.split(file_path_A)[-1]
        file_path_B = self.file2
        file2 = os.path.split(file_path_B)[-1]

        #Set the total portions needed for the progress bar
        Application.progress_index["maximum"] = 1
        self.Text_G.configure(text = '      Preparing the files before comparison...\n' + 'indexing ' + file1 + '...')
        try:
            current_extension = file1.split(".")[1]
            if(current_extension == 'fm8'):
                e = open('errors.txt', 'a+')
                e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n' )
                return

            other_extension = file2.split(".")[1]
            if(current_extension != other_extension):
                e = open('errors.txt', 'a+')
                e.write('*** warning: 2 files being compared are not the same file type ! ***' + '\n' )

            #Check the encoding format for current file
            raw = open(file_path_A,'rb').read()
            result = chardet.detect(raw)
            char = result['encoding']
            #If the encoding format is not the usual one we would just skip it and leave it for manual inspection
            if char not in ['ascii', 'UTF-8','UTF-16','UTF-8-SIG']:
                e = open('errors.txt', 'a+')
                e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n')
                return

            #Check the encoding format for other file
            raw = open(file_path_B,'rb').read()
            result = chardet.detect(raw)
            char2 = result['encoding']
            #If the encoding format is not the usual one we would just skip it and leave it for manual inspection
            if char2 not in ['ascii', 'UTF-8','UTF-16','UTF-8-SIG']:
                e = open('errors.txt', 'a+')
                e.write('   File ' + file2 + '\'s encoding is not belong to either ascii, utf-8 or utf-16. Manual inspection required.' + '\n')
                return


            text_file_1 = open(file_path_A, 'r').read()
            text_file_2 = open(file_path_B, 'r').read()

            current_file_as_string_list_1 = []
            current_file_as_string_list_2 = []

            #adding lines from current file in folder 1 to the string list of the current file:
            #... if some characters are odd, convert it to utf-8
            f = open('testing.txt', 'w+')
            for line in text_file_1:
                result = chardet.detect(line)
                char = result['encoding']
                if char not in ['utf-8', 'utf-16', 'ascii']:
                    try:
                        line = line.decode(char).encode('utf-8','ignore')
                    except:
                        line = line.decode('latin-1').encode('utf-8','ignore')
                if line == '\x00':
                    continue
                f.write(line)
            f.close()
            f = open('testing.txt', 'r').readlines()
            for line in f:
                current_file_as_string_list_1.append(line)

            #adding lines from current file in folder 1 to the string list of the current file
            #... if some characters are odd, convert it to utf-8
            f = open('testing2.txt', 'w+')
            for line in text_file_2:
                result = chardet.detect(line)
                char = result['encoding']
                if char not in ['utf-8', 'utf-16', 'ascii']:
                    try:
                        line = line.decode(char).encode('utf-8','ignore')
                    except:
                        line = line.decode('latin-1').encode('utf-8','ignore')
                if line == '\x00':
                    continue
                f.write(line)
            f.close()
            f = open('testing2.txt', 'r').readlines()
            for line in f:
                current_file_as_string_list_2.append(line)

            #Add the 2 string list to the list of all the file's content
            self.files_as_string_1.append(current_file_as_string_list_1)
            self.files_as_string_2.append(current_file_as_string_list_2)

            #Add the current file pair to the file pair list
            current_file_pair = [file1,file2]
            #Add the current format to the current format pair list
            current_format_pair = [char, char2]
            #Add thhe file name, pair and format pair to the overall lists
            self.file_name_list.append(current_extension)
            self.file_pair_list.append(current_file_pair)
            self.file_format_list.append(current_format_pair)

            downloaded_index.set(1)
            root.update()

        #If there were any error occured during the process, write it to the errors file log
        except:
            e = open('errors.txt', 'a+')
            e.write('   Errors occurred in file: ' + file1 + '.\n')
            e2 = open('trace_back_log.txt', 'a+')
            e2.write(traceback.format_exc() + '\n')

    #write the javascript accommodate the HTML file, h is the final HTML report being passed to the function
    def writeFooter(self, h):
        h.write('''
    function openFile(evt, fileName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      document.getElementById(fileName).style.display = "block";
      evt.currentTarget.className += " active";
    }
    
    window.onscroll = function() {scrollFunction()};
    
    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("myBtn").style.display = "block";
      } else {
        document.getElementById("myBtn").style.display = "none";
      }
    }
    
    // When the user clicks on the button, scroll to the top of the document
    function topFunction() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }
    
    </script>
    
    </body>
    </html>
    ''')







        ##print len(files_as_string_1)
        ##print len(files_as_string_2)

    #write the CSS style sheet to accommodate the HTML file, input and output h is the final HTML report being passed to the function
    def writeHeader(self, h):
        h.write('''
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {box-sizing: border-box}
    body {font-family: "Lato", sans-serif;}
    
    html {
      scroll-behavior: smooth;
    }
    
    #myBtn {
      display: none;
      position: fixed;
      bottom: 20px;
      right: 30px;
      z-index: 99;
      font-size: 18px;
      border: none;
      outline: none;
      background-color: red;
      color: white;
      cursor: pointer;
      padding: 15px;
      border-radius: 4px;
    }
    
    #myBtn:hover {
      background-color: #555;
    }
    
    
    /* Style the tab */
    .tab {
      float: left;
      position:fixed;
      border: 1px solid #ccc;
      background-color: #f1f1f1;
      width: 20%;
      height: 500px;
    }
    
    /* Style the buttons inside the tab */
    .tab button {
      display: block;
      background-color: inherit;
      color: black;
      padding: 22px 16px;
      width: 100%;
      border: none;
      outline: none;
      text-align: left;
      cursor: pointer;
      font-size: 17px;
    }
    
    /* Change background color of buttons on hover */
    .tab button:hover {
      background-color: #80bfff!important ;
    }
    
    /* Create an active/current "tab button" class */
    .tab button.active {
      background-color: #80bfff!important;
    }
    
    /* Style the tab content */
    .tabcontent {
      float: right;
      padding: 0px 12px;
      width: 70%;
      border-left: none;
      height: 300px;
      display: none;
    }
    
    /* Clear floats after the tab */
    .clearfix::after {
      content: "";
      clear: both;
      display: table;
    }
    </style>
    </head>
    <body>
    
    <button onclick="topFunction()" id="myBtn" title="Go to top">Top</button>
    
    ''')

        return h


app = Application(master=root)
if os.path.exists(r'Emerson-Logo.ico'):
    root.iconbitmap(r'Emerson-Logo.ico')
app.mainloop()


