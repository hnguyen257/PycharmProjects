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


    h = open("reportH.html", "w+")




    #Go through each file type available
    for current_file_index in range(number_of_files):
        no_difference = True
        diff_total = 0
        #current_line_keeper = 0
        fileName =  str(file_name_list[current_file_index])
        fileA = str(file_pair_list[current_file_index][0])
        fileB = str(file_pair_list[current_file_index][1])

        # Write current file type to report_prep.txt
        f = open("report_prep.txt", "a+")
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
        
        used = []
        #go down the every line of the current file being processed
        current_file_a = files_as_string_1[current_file_index]
        for current_line_a in range(len(current_file_a)):
            same_line_found = 0
            h.write('<tr>' + '\n')
            h.write('  <td>' + str(current_line_a) + '</td>' + '\n')
            current_file_b = files_as_string_2[current_file_index]
            for current_line_b in range(len(current_file_a)):
                if current_line_b in used:
                    continue
                if current_file_a[current_line_a] == current_file_b[current_line_b]:
                    h.write('  <td>' + str(current_file_a[current_line_a]).rstrip() + '</td>' + '\n')
                    h.write('  <td>' + str(current_file_b[current_line_b]).rstrip() + '</td>' + '\n')
                    same_line_found = 1
                    used.append(current_line_b)
            if same_line_found == 0

            




















    f = open("report.txt", "w+")
    f.write("Time: " + str(datetime.datetime.now()) + "\n")
    f.write("Overall result: " + "\n")
    for i in range(len(file_name_list)):
        f.write("      " + file_name_list[i] + ":  " + file_pair_list[i][0] + " and " + file_pair_list[i][1] + "   -   " + str(diff_total_list[i]) + " differences" + "\n")
    f.write(open("report_prep.txt", 'r').read())
    f.close()
    os.remove('report_prep.txt')

    h = open("reportH2.html", "w+")
    writeHeader(h)

    h.write('<div class="tab">' + "\n")
    h.write('          <button class="tablinks" onmouseover="openFile(event, \'' + 'Overall result' + '\')"'  + '>' + 'Overall result' + '</button>' + "\n")
    for current_file_index in range(number_of_files):
        fileName = str(file_name_list[current_file_index])
        color = '#ccffee"'
        if diff_total_list[current_file_index] > 0:
            color = '#ff9999"'
        h.write(
            '          <button class="tablinks" onmouseover="openFile(event, \'' + fileName + '\')"' + 'style="background-color:' + color + '>'  + fileName + '</button>' + "\n")
    h.write('    </div>')

    h.write(open("reportH.html", 'r').read())
    h.write('<div id="Overall result" class="tabcontent">' + '\n')
    h.write('<pre>' + open("report.txt", 'r').read() + '</pre>' + '\n')
    h.write('</div>')
    h.write('''
    <div class="clearfix"></div>

    <script>
    ''')
    h.write('var currentFile = ' + "''" + '\n')
    h.write('var currentDiff = 0 \n')
    h.write('var dict = {}; \n')
    for i in range(len(file_name_list)):
        h.write('dict["' + file_name_list[i] + '"] = ' + str(diff_total_list[i]) + '\n' )
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


'''
text_file = codecs.open(current_file, "r", 'latin-1')

    print "_______________________________________________________________________________"
    #print (text_file.read())
    for line in text_file:
        print line
'''



