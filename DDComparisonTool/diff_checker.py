import sys
import os
from os import listdir
import codecs
import chardet
import datetime
import locale
import io
import xml.etree.ElementTree as ET

files_as_string_1 =[]
files_as_string_2 =[]
file_name_list = []
file_pair_list = []
diff_total_list = []
def main():
    index_file()
    number_of_files = len(files_as_string_1)

    print file_name_list
    print file_pair_list

    f = open("report_prep.txt", "w+")


    for current_file_index in range(number_of_files):
        no_difference = True
        diff_total = 0
        f = open("report_prep.txt", "a+")
        f.write("\n\n")
        f.write("File type: " + file_name_list[current_file_index] + "\n")
        f.write("Files being compare: " + file_pair_list[current_file_index][0] + "  and  " + file_pair_list[current_file_index][1] + "\n")
        f.write("Differences: " + "\n")
        for current_line in range(len(files_as_string_1[current_file_index])):

            print files_as_string_1[current_file_index][current_line]
            print files_as_string_2[current_file_index][current_line]

            if(files_as_string_1[current_file_index][current_line] == files_as_string_2[current_file_index][current_line]):
                print "Same"
            else:
                if(no_difference):
                    no_difference = False
                print "difference"
                diff_total = diff_total + 1
                f.write("Line " + str(current_line) + "\n")
                f.write("     " + files_as_string_1[current_file_index][current_line] + "\n")
                f.write("     " + files_as_string_2[current_file_index][current_line] + "\n")
        if(no_difference):
            f.write("     None" + "\n")
        diff_total_list.append(diff_total)

    f = open("report.txt", "w+")
    f.write("Time: " + str(datetime.datetime.now()) + "\n")
    f.write("Overall result: " + "\n")
    for i in range(len(file_name_list)):
        f.write("      " + file_name_list[i] + ":  " + file_pair_list[i][0] + " and " + file_pair_list[i][1] + "   -   " + str(diff_total_list[i]) + " differences" + "\n")
    f.write(open("report_prep.txt", 'r').read())
    os.remove('report_prep.txt')




def index_file():
    paths = sys.argv[1:]


    folder1_path = paths[0]
    folder2_path = paths[1]

    print "Path 1: " + folder1_path
    print "Path 2: " + folder2_path

    files_in_folder1 = listdir(folder1_path)
    files_in_folder2 = listdir(folder2_path)
    print "Files in folder 1:"
    print files_in_folder1

    print "Files in folder 2:"
    print files_in_folder2
    a = os.getcwd()
    print a

    try:
        for file1 in files_in_folder1:
            current_extension = file1.split(".")[1]
            if(current_extension == 'fm8'):
                continue
            print current_extension
            current_file_folder1 = str(folder1_path) + "\\" + file1
            print current_file_folder1

            raw = open(current_file_folder1,'rb').read()
            result = chardet.detect(raw)
            print result
            char = result['encoding']
            print char
            if char not in ['ascii', 'UTF-8','UTF-16']:
                continue

            try:
                for file2 in files_in_folder2:
                    print file2.split(".")[1]
                    print current_extension
                    if file2.split(".")[1] == current_extension:
                        print file1
                        print file2
                        if(file1 == 'ddinstal.ini' and file2 != 'ddinstal.ini'):
                            continue
                        current_file_folder2 = str(folder2_path) + "\\" + file2
                        text_file_1 = codecs.open(current_file_folder1, "r", char)

                        raw = open(current_file_folder1, 'rb').read()
                        result = chardet.detect(raw)
                        print result
                        char = result['encoding']
                        print char
                        text_file_2 = codecs.open(current_file_folder2, "r", char)

                        current_file_as_string_list_1 = []
                        current_file_as_string_list_2 = []
                        for line in text_file_1:
                            print line
                            current_file_as_string_list_1.append(line)

                        files_as_string_1.append(current_file_as_string_list_1)

                        for line in text_file_2:
                            print line
                            current_file_as_string_list_2.append(line)

                        files_as_string_2.append(current_file_as_string_list_2)

                        current_file_pair = [file1,file2]
                        file_name_list.append(current_extension)
                        file_pair_list.append(current_file_pair)
                        break
            except:
                    continue
    except:
            pass










    print len(files_as_string_1)
    print len(files_as_string_2)









if __name__ == "__main__":
    main()


'''
text_file = codecs.open(current_file, "r", 'latin-1')

    print "_______________________________________________________________________________"
    #print (text_file.read())
    for line in text_file:
        print line
'''



