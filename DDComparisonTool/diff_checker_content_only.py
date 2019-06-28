import sys
import os
from os import listdir
import codecs
import chardet
from difflib import SequenceMatcher
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

    f = open("report_prep_content.txt", "w+")
    h = open("reportH_content.html", "w+")




    #Go through each file type available
    for current_file_index in range(number_of_files):
        is_difference = False
        diff_total = 0
        current_line_keeper = 0
        fileName =  str(file_name_list[current_file_index])
        fileA = str(file_pair_list[current_file_index][0])
        fileB = str(file_pair_list[current_file_index][1])

        # Write current file type to report_prep_content.txt
        f = open("report_prep_content.txt", "a+")
        f.write("\n\n")
        f.write("File type: " + fileName + "\n")
        f.write("Files being compare: " + fileA + "  and  " + fileB + "\n")
        f.write("Differences: " + "\n")

        h.write('<div id="' + fileName + '" class="tabcontent">' + '\n')
        h.write('<table style="width:100%">' + '\n')
        h.write('<tr>' + '\n')
        h.write('   <th>' + 'Line #' + '</th>' + '\n')
        h.write('   <th>' + fileA + '</th>' + '\n')
        h.write('   <th>' + fileB + '</th>' + '\n')
        h.write('</tr>' + '\n\n')

        #go down the every line of the current file being processed
        for current_line in range(len(files_as_string_1[current_file_index])):
            print current_line
            h.write('<tr>' + '\n')
            h.write('  <td>' + str(current_line) + '</td>' + '\n')
            used = []
            same_line_found = 0
            highest_similarity_percentage = 0
            highest_similarity_index = 0
            highest_similarity_percentage2 = 0
            highest_similarity_index2 = 0

            for current_line2 in range(len(files_as_string_2[current_file_index])):
                highest_similarity_percentage = 0
                highest_similarity_index = 0
                if current_line2 in used:
                    continue
                #print files_as_string_1[current_file_index][current_line]
                #print files_as_string_2[current_file_index][current_line2]
                if (files_as_string_1[current_file_index][current_line] == files_as_string_2[current_file_index][current_line2]):
                    h.write('  <td>' + str(files_as_string_1[current_file_index][current_line]).rstrip() + '</td>' + '\n')
                    h.write('  <td>' + str(files_as_string_2[current_file_index][current_line2]).rstrip() + '</td>' + '\n')
                    used.append(current_line2)
                    same_line_found = 1
                    break
                else:
                    if (files_as_string_1[current_file_index][current_line][0] != files_as_string_2[current_file_index][current_line2][0]):
                        continue

                    current_percentage = SequenceMatcher(None, files_as_string_2[current_file_index][current_line2], files_as_string_1[current_file_index][current_line]).ratio()
                    if highest_similarity_percentage < current_percentage:
                        highest_similarity_percentage = current_percentage
                        highest_similarity_index = current_line2
            if same_line_found == 0:
                if (is_difference == False):
                    is_difference = True
                if highest_similarity_percentage != 0:
                    for current_line3 in range(current_line, len(files_as_string_1[current_file_index])):
                        same_line_found2 = 0
                        if files_as_string_1[current_file_index][current_line3] == files_as_string_2[current_file_index][highest_similarity_index]:
                            same_line_found2 = 1
                            break
                        if (files_as_string_2[current_file_index][highest_similarity_index][0] != files_as_string_1[current_file_index][current_line3][0]):
                            continue
                        current_percentage2 = SequenceMatcher(None, files_as_string_2[current_file_index][highest_similarity_index], files_as_string_1[current_file_index][current_line3]).ratio()
                        if highest_similarity_percentage2 < current_percentage2:
                            highest_similarity_percentage2 = current_percentage2
                            highest_similarity_index2 = current_line3
                if highest_similarity_percentage < highest_similarity_percentage2 or highest_similarity_percentage == 0:
                    diff_id = str(diff_total)
                    h.write('   <td ' + 'id="' + str(file_name_list[current_file_index]) + diff_id + '"' + ' style="background-color: #FFFF00">')
                    h.write('<font style="background-color: #89ED75">' + str(files_as_string_1[current_file_index][current_line]).rstrip() + '</font>')
                    h.write('</td>' + '\n')
                    h.write('   <td style="background-color: #FFFF00">')
                    h.write('<font style="background-color: #89ED75">')
                    for a in range(len(str(files_as_string_1[current_file_index][current_line]).rstrip())):
                        h.write('&nbsp;&nbsp;')
                    h.write('</font>')
                    h.write('</td>' + '\n')

                    diff_total = diff_total + 1
                    f.write("Line " + str(current_line) + "\n")
                    f.write("     " + files_as_string_1[current_file_index][current_line] + "\n")
                    f.write("     ------ \"Missing line\" -----     " + "\n")
                else:

                    used.append(highest_similarity_index)
                    length_a = len(str(files_as_string_1[current_file_index][current_line]).rstrip())
                    length_b = len(str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip())

                    diff_id = str(diff_total)
                    length_use = length_a
                    if length_a > length_b:
                        length_use = length_b
                    h.write('   <td ' + 'id="' + str(file_name_list[current_file_index]) + diff_id + '"' + ' style="background-color: #FFFF00">')
                    for a in range(length_use):
                        print str(files_as_string_1[current_file_index][current_line]).rstrip()[a]
                        print str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a]
                        if str(files_as_string_1[current_file_index][current_line]).rstrip()[a] != str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a]:
                            h.write('<font style="background-color: #89ED75">' + str(files_as_string_1[current_file_index][current_line]).rstrip()[a] + '</font>')
                        else:
                            h.write(str(files_as_string_1[current_file_index][current_line]).rstrip()[a])
                    if length_a > length_b:
                        h.write('<font style="background-color: #89ED75">')
                        for a in range(length_use, length_a):
                            h.write(str(files_as_string_1[current_file_index][current_line]).rstrip()[a])
                        h.write('</font>')
                    else:
                        h.write('<font style="background-color: #89ED75">')
                        for a in range(length_use, length_b):
                            h.write('&nbsp;&nbsp;')
                        h.write('</font>')

                    h.write('</td>' + '\n')

                    length_use = length_b
                    if length_b > length_a:
                        length_use = length_a
                    h.write('   <td style="background-color: #FFFF00">')
                    for a in range(length_use):
                        print str(files_as_string_1[current_file_index][current_line]).rstrip()[a]
                        print str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a]
                        if str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a] != str(files_as_string_1[current_file_index][current_line]).rstrip()[a]:
                            h.write('<font style="background-color: #89ED75">' + str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a] + '</font>')
                        else:
                            h.write(str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a])
                    if length_b > length_a:
                        h.write('<font style="background-color: #89ED75">')
                        for a in range(length_use, length_b):
                            h.write(str(files_as_string_2[current_file_index][highest_similarity_index]).rstrip()[a])
                        h.write('</font>')
                    else:
                        h.write('<font style="background-color: #89ED75">')
                        for a in range(length_use, length_a):
                            h.write('&nbsp;&nbsp;')
                        h.write('</font>')
                    h.write('</td>' + '\n')
                    diff_total = diff_total + 1
                    f.write("Line " + str(current_line) + "\n")
                    f.write("     " + files_as_string_1[current_file_index][current_line] + "\n")
                    f.write("     " + files_as_string_2[current_file_index][highest_similarity_index] + "\n")
            h.write('</tr>' + '\n\n')
        if (is_difference == False):
            f.write("     None" + "\n")
        diff_total_list.append(diff_total)
        h.write('</table>' + "\n")
        h.write('</div>' + '\n\n')

    f = open("report_content.txt", "w+")
    f.write("Time: " + str(datetime.datetime.now()) + "\n")
    f.write("Overall result: " + "\n")
    for i in range(len(file_name_list)):
        f.write("      " + file_name_list[i] + ":  " + file_pair_list[i][0] + " and " + file_pair_list[i][
            1] + "   -   " + str(diff_total_list[i]) + " differences" + "\n")
    f.write(open("report_prep_content.txt", 'r').read())
    f.close()
    os.remove('report_prep_content.txt')






    h = open("reportH2_content.html", "w+")
    writeHeader(h)

    h.write('<div class="tab">' + "\n")
    h.write(
        '          <button class="tablinks" onmouseover="openFile(event, \'' + 'Overall result' + '\')"' + '>' + 'Overall result' + '</button>' + "\n")
    for current_file_index in range(number_of_files):
        fileName = str(file_name_list[current_file_index])
        color = '#ccffee"'
        if diff_total_list[current_file_index] > 0:
            color = '#ff9999"'
        h.write(
            '          <button class="tablinks" onmouseover="openFile(event, \'' + fileName + '\')"' + 'style="background-color:' + color + '>' + fileName + '</button>' + "\n")
    h.write('    </div>')

    h.write(open("reportH_content.html", 'r').read())
    h.write('<div id="Overall result" class="tabcontent">' + '\n')
    h.write('<pre>' + open("report_content.txt", 'r').read() + '</pre>' + '\n')
    h.write('</div>')
    h.write('''
        <div class="clearfix"></div>

        <script>
        ''')
    h.write('var currentFile = ' + "''" + '\n')
    h.write('var currentDiff = 0 \n')
    h.write('var dict = {}; \n')
    for i in range(len(file_name_list)):
        h.write('dict["' + file_name_list[i] + '"] = ' + str(diff_total_list[i]) + '\n')
    writeFooter(h)

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

def writeFooter(h):
    #h = open("reportH.html", "a+")
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
  currentFile = fileName;
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("myBtn").style.display = "block";
    document.getElementById("myBtn2").style.display = "block";
  } else {
    document.getElementById("myBtn").style.display = "none";
    document.getElementById("myBtn2").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// When the user clicks on the button, go to next line of differences
function goNext() {
   var a = '#' + currentFile +currentDiff;
  if(currentDiff < dict[currentFile]){
  	currentDiff = currentDiff + 1;
  }else{
  	currentDiff = 0;
  }
  location.href = a
  window.scrollBy(0, 200);
}

</script>

</body>
</html>
''')







    print len(files_as_string_1)
    print len(files_as_string_2)


def writeHeader(h):
    #h = open("reportH.html", "a+")
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

#myBtn2 {
  display: none;
  position: fixed;
  top: 20px;
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

#myBtn2:hover {
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
<button onclick="goNext()" id="myBtn2" title="Go to next line of difference">Next</button>

''')

    return h




if __name__ == "__main__":
    main()





















