import sys
import os
from os import listdir
import codecs
import chardet
import datetime
import locale
import io
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher

files_as_string_1 =[]
files_as_string_2 =[]
file_name_list = []
file_pair_list = []
diff_total_list = []
def main():
    index_file()
    number_of_files = len(files_as_string_1)
    count = 0
    simAll = []
    #Go through each file type available
    for current_file_index in range(number_of_files):
        simA = []
        simB = []
        print current_file_index
        for current_line in range(len(files_as_string_1[current_file_index])):
            #print current_line
            a = files_as_string_1[current_file_index][current_line]
            #print a
            hper = 0
            hind = 0
            for current_line2 in range(len(files_as_string_2[current_file_index])):
                if current_line2 in simA:
                    continue
                b = files_as_string_2[current_file_index][current_line2]
                #print b
                if a == b:
                    hind = current_line2
                    break
                result = SequenceMatcher(None, a, b).ratio()
                if hper < result:
                    hper = result
                    hind = current_line2
            simA.append(hind)

        for current_line in range(len(files_as_string_2[current_file_index])):
            #print current_line
            a = files_as_string_2[current_file_index][current_line]
            #print a
            hper = 0
            hind = 0
            for current_line2 in range(len(files_as_string_1[current_file_index])):
                if current_line2 in simB:
                    continue
                b = files_as_string_1[current_file_index][current_line2]
                #print b
                if a == b:
                    hind = current_line2
                    break
                result = SequenceMatcher(None, a, b).ratio()
                if hper < result:
                    hper = result
                    hind = current_line2
            simA.append(hind)
        simAll.append([simA,simB])

    print simAll
    print simAll[0]
    print simAll[0][0]
    print simAll[0][0][0]





def index_file():
    paths = sys.argv[1:]


    folder1_path = paths[0]
    folder2_path = paths[1]



    files_in_folder1 = listdir(folder1_path)
    files_in_folder2 = listdir(folder2_path)


    a = os.getcwd()


    try:
        for file1 in files_in_folder1:
            current_extension = file1.split(".")[1]
            if(current_extension == 'fm8'):
                continue

            current_file_folder1 = str(folder1_path) + "\\" + file1


            raw = open(current_file_folder1,'rb').read()
            result = chardet.detect(raw)

            char = result['encoding']

            if char not in ['ascii', 'UTF-8','UTF-16']:
                continue

            try:
                for file2 in files_in_folder2:

                    if file2.split(".")[1] == current_extension:

                        if(file1 == 'ddinstal.ini' and file2 != 'ddinstal.ini'):
                            continue
                        current_file_folder2 = str(folder2_path) + "\\" + file2
                        text_file_1 = codecs.open(current_file_folder1, "r", char)

                        raw = open(current_file_folder1, 'rb').read()
                        result = chardet.detect(raw)

                        char = result['encoding']

                        text_file_2 = codecs.open(current_file_folder2, "r", char)

                        current_file_as_string_list_1 = []
                        current_file_as_string_list_2 = []
                        for line in text_file_1:

                            current_file_as_string_list_1.append(line)

                        files_as_string_1.append(current_file_as_string_list_1)

                        for line in text_file_2:

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


if __name__ == "__main__":
    main()


'''
text_file = codecs.open(current_file, "r", 'latin-1')

    print "_______________________________________________________________________________"
    #print (text_file.read())
    for line in text_file:
        print line
'''



