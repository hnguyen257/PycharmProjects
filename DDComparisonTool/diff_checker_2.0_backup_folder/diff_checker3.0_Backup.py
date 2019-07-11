import sys
import os
from os import listdir
import codecs
import traceback
import datetime
import chardet
from difflib import SequenceMatcher
import locale
import io
import xml.etree.ElementTree as ET

files_as_string_1 =[]
files_as_string_2 =[]
file_name_list = []
file_pair_list = []
diff_total_list = []

def main():
    e = open('errors.txt', 'w+')
    index_file()

    number_of_files = len(files_as_string_1)

    f = open("report_prep.txt", "w+")
    h = open("reportH.html", "w+")


    file_name_quantity = {i:1 for i in file_name_list}


    #Go through each file type available
    for current_file_index in range(number_of_files):
        try:
            no_difference = True
            diff_total = 0
            current_line_keeper = 0
            fileName =  str(file_name_list[current_file_index])

            x = file_name_quantity[fileName.split()[0]]
            if x > 1:
                fileName = fileName + '(' + str(x) + ')'

            file_name_quantity[fileName.split()[0]] = x + 1

            file_name_list[current_file_index] = fileName


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
            h.write('   <th>' + 'Line A #' + '</th>' + '\n')
            h.write('   <th>' + fileA + '</th>' + '\n')
            h.write('   <th>' + 'Line B #' + '</th>' + '\n')
            h.write('   <th>' + fileB + '</th>' + '\n')
            h.write('</tr>' + '\n\n')

            #go down the every line of the current file being processed
            current_file_A = files_as_string_1[current_file_index]
            current_file_B = files_as_string_2[current_file_index]



            if fileName == 'ini':
                pass

            for i in range(len(current_file_A)):
                current_file_A[i] = current_file_A[i].replace('\n','').replace('\r','').rstrip()
            current_file_A_temp = [i for i in current_file_A]
            for line in current_file_A_temp:
                if len(line.replace(' ', '')) == 0:
                    current_file_A.remove(line)


            for i in range(len(current_file_B)):
                current_file_B[i] = current_file_B[i].replace('\n','').replace('\r','').rstrip()
            current_file_B_temp = [i for i in current_file_B]
            for line in current_file_B_temp:
                if len(line.replace(' ', '')) == 0:
                    current_file_B.remove(line)

            file_A_diff = []

            count = 0
            '''
            if fileName == 'ini':
                for i in range(len(current_file_A)):
                    print current_file_A[i]
                    print current_file_B[i]
                    a = str(current_file_A[i])
                    b = str(current_file_B[i])
                    for i in range(len(a)):
                        print a[i]
                        print b[i]
                        if a[i] == b[i]:
                            print 'same'
                        else:
                            print 'no'
                    if a == b:
                        print 'same'
                    else:
                        print 'no'
            '''
            current_file_B_original = [i for i in current_file_B]

            for current_line in current_file_A:
                print current_line
                if len(current_line.replace(' ','').replace('\n','').replace('\r','')) == 0:
                    continue
                if current_line in current_file_B:
                    current_file_B.remove(current_line)
                else:
                    diff_total = diff_total + 1
                    file_A_diff.append(current_line)

            if len(current_file_B) != 0 and len(current_file_A)!=0:
                no_difference = False
            line_in_B_left = [i for i in current_file_B]
            #print len(current_file_B)
            #print len(file_A_diff)
            similarity_percentage = [[0 for i in range(len(current_file_B))] for j in range(len(file_A_diff))]

            #print file_A_diff
            #print current_file_B
            print len(file_A_diff)
            for i in range(len(file_A_diff)):
                print i
                for j in range(len(current_file_B)):
                    similarity_percentage[i][j] = SequenceMatcher(None, file_A_diff[i], current_file_B[j]).ratio()
                    #print similarity_percentage[i][j]
                #print similarity_percentage[i]


            most_similar_A = [0 for i in range(len(file_A_diff))]
            most_similar_B = [0 for i in range(len(current_file_B))]

            second_most_similar_A = [0 for i in range(len(file_A_diff))]
            second_most_similar_B = [0 for i in range(len(current_file_B))]

            for i in range(len(file_A_diff)):
                #print file_A_diff[i]
                highest_percentage = None
                highest_percentage_index = None
                second_highest_percentage_index = None
                for j in range(len(current_file_B)):
                    #print current_file_B[j]
                    #print similarity_percentage[i][j]
                    if similarity_percentage[i][j] > highest_percentage:
                        second_highest_percentage_index = highest_percentage_index
                        highest_percentage_index = j
                        highest_percentage = similarity_percentage[i][j]
                most_similar_A[i] = highest_percentage_index
                second_most_similar_A[i] = second_highest_percentage_index


            for j in range(len(current_file_B)):
                #print current_file_B[j]
                highest_percentage = None
                highest_percentage_index = None
                second_highest_percentage_index = None
                for i in range(len(file_A_diff)):
                    #print file_A_diff[i]
                    #print similarity_percentage[i][j]
                    if similarity_percentage[i][j] > highest_percentage:
                        second_highest_percentage_index = highest_percentage_index
                        highest_percentage_index = i
                        highest_percentage = similarity_percentage[i][j]
                most_similar_B[j] = highest_percentage_index
                second_most_similar_B[j] = second_highest_percentage_index



            diff_id = str(diff_total)



            f.write('Line in ' + fileA + ' that are not in ' + fileB + ':' + "\n")
            if len(file_A_diff) == 0:
                f.write('   None' + '\n')

            for current_line in file_A_diff:
                f.write('   line ' +  str(current_file_A.index(current_line)+ 1) + ': ' + current_line + "\n")



            f.write('Line in ' + fileB + ' that are not in ' + fileA + ':' + "\n")
            if len(current_file_B) == 0:
                f.write('   None' + '\n')

            for current_line in current_file_B:
                f.write('   line ' +  str(current_file_B_original.index(current_line)+ 1) + ': ' + current_line + "\n")

            for current_line in file_A_diff:

                h.write('<tr>' + '\n')
                h.write('  <td>' + str(current_file_A.index(current_line)+ 1) + '</td>' + '\n')
                current_file_A[current_file_A.index(current_line)] = None

                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                h.write(escapeHtml(current_line))
                h.write('   </td>' + '\n')

                testing = current_line
                a = file_A_diff.index(current_line)
                file_A_diff[a] = None
                b = most_similar_A[a]

                if b != None and len(current_file_B) > 0:
                    if most_similar_B[b] == a:
                        h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                        current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                        h.write(escapeHtml(current_file_B[b]))
                        line_in_B_left.remove(current_file_B[b])
                        h.write('  </td>' + '\n')
                        continue

                    if second_most_similar_B[b] == a:
                        a2 = most_similar_B[b]
                        if most_similar_A[a2] != b:
                            h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                            current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                            h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                            h.write(escapeHtml(current_file_B[b]))
                            line_in_B_left.remove(current_file_B[b])
                            h.write('  </td>' + '\n')
                            continue


                    if most_similar_B[b] == a:
                        h.write('  <td>' + str(current_file_B_original.index(current_file_B[b]) + 1) + '</td>' + '\n')
                        current_file_B_original[current_file_B_original.index(current_file_B[b])] = None
                        h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                        h.write(escapeHtml(current_file_B[b]))
                        line_in_B_left.remove(current_file_B[b])
                        h.write('  </td>' + '\n')
                        continue


                h.write('  <td>' + ' - ' + '</td>' + '\n')
                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                h.write(' </td>' + '\n')


                h.write('</tr>' + '\n\n')


            for current_line in line_in_B_left:
                if len(current_line.replace(' ','').replace('\n','').replace('\r','')) == 0:
                    continue
                h.write('<tr>' + '\n')
                h.write('  <td>' + ' - ' + '</td>' + '\n')

                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                h.write('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
                h.write(' </td>' + '\n')

                h.write('  <td>' + str(current_file_B_original.index(current_line) + 1) + '</td>' + '\n')
                current_file_B_original[current_file_B_original.index(current_line)] = None

                h.write('   <td ' + 'id="' + fileName + diff_id + '"' + ' style="background-color: #FFFF00">')
                h.write(escapeHtml(current_line))
                h.write('   </td>' + '\n')

                diff_total = diff_total + 1
                h.write('</tr>' + '\n\n')


            diff_total_list.append(diff_total)
            h.write('</table>' + "\n")
            h.write('</div>' + '\n\n')
        except:
            e.write('   Errors occured in file: ' + fileName + '. Manual inspection required' + '\n')
            continue

    f.write(' \n \n \n - End of Report -')
    f.close()
    h.close()
    writeEnding()

def escapeHtml(unsafe):
    safe = unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace("'", "&#039;");
    return safe


def writeEnding():

    f = open("report.txt", "w+")
    f.write("Time: " + str(datetime.datetime.now()) + "\n")
    f.write("Overall result: " + "\n")
    for i in range(len(file_name_list)):
        f.write("      " + file_name_list[i] + ":  " + file_pair_list[i][0] + " and " + file_pair_list[i][1] + "   -   " + str(diff_total_list[i]) + " differences" + "\n")
    f.write('Errors encountered:' + '\n')
    if len(open('errors.txt', 'r').read()) == 0:
        f.write('   None' + '\n')
    f.write(open('errors.txt', 'r').read())

    f.write(open("report_prep.txt", 'r').read())
    f.close()
    os.remove('report_prep.txt')

    number_of_files = len(files_as_string_1)

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

    #print open("reportH.html", 'r').read()

    h.write(open("reportH.html", 'r').read())
    h.write('<div id="Overall result" class="tabcontent">' + '\n')
    h.write('<pre>' + open("report.txt", 'r').read() + '</pre>' + '\n')
    h.write('</div>')



    h.write('''
    <div class="clearfix"></div>

    <script>
    ''')
    writeFooter(h)

def index_file():
    paths = sys.argv[1:]


    folder1_path = paths[0]
    folder2_path = paths[1]

    ##print "Path 1: " + folder1_path
    ##print "Path 2: " + folder2_path

    files_in_folder1 = listdir(folder1_path)
    files_in_folder2 = listdir(folder2_path)
    ##print "Files in folder 1:"
    ##print files_in_folder1

    #print "Files in folder 2:"
    #print files_in_folder2
    a = os.getcwd()
    #print a

    for file1 in files_in_folder1:
        try:
            current_extension = file1.split(".")[1]
            print current_extension
            if(current_extension == 'fm8'):
                e = open('errors.txt', 'a+')
                e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-9 or utf-16. Manual inspection required.' + '\n' )
                continue


            current_file_folder1 = str(folder1_path) + "\\" + file1

            raw = open(current_file_folder1,'rb').read()
            result = chardet.detect(raw)
            #print result
            char = result['encoding']
            print char
            if char not in ['ascii', 'UTF-8','UTF-16','UTF-8-SIG']:
                e = open('errors.txt', 'a+')
                e.write('   File ' + file1 + '\'s encoding is not belong to either ascii, utf-9 or utf-16. Manual inspection required.' + '\n')
                continue

            #try:
            for file2_prep in files_in_folder2:
                file2 = file2_prep
                #print file2.split(".")[1]
                #print current_extension
                if file2.split(".")[1] == current_extension:
                    print file1
                    print file2
                    if (current_extension == 'ini') and (file1 != file2):
                        continue
                    files_in_folder2.remove(file2_prep)
                    current_file_folder2 = str(folder2_path) + "\\" + file2

                    text_file_1 = open(current_file_folder1, 'r').read()
                    text_file_2 = open(current_file_folder2, 'r').read()

                    current_file_as_string_list_1 = []
                    current_file_as_string_list_2 = []

                    f = open('testing.txt', 'w+')
                    for line in text_file_1:
                        result = chardet.detect(line)
                        char = result['encoding']
                        if char not in ['utf-8', 'utf-16', 'ascii']:
                            line = line.decode(char).encode('utf-8','ignore')
                        if line == '\x00':
                            continue
                        f.write(line)
                    f.close()
                    f = open('testing.txt', 'r').readlines()
                    for line in f:
                        current_file_as_string_list_1.append(line)


                    f = open('testing2.txt', 'w+')
                    for line in text_file_2:
                        result = chardet.detect(line)
                        char = result['encoding']
                        if char not in ['utf-8', 'utf-16', 'ascii']:
                            line = line.decode(char).encode('utf-8','ignore')
                        if line == '\x00':
                            continue
                        f.write(line)
                    f.close()
                    f = open('testing2.txt', 'r').readlines()
                    for line in f:
                        current_file_as_string_list_2.append(line)

                    for line in current_file_as_string_list_1:
                        print line
                    print '________________________________________________________________________________________________'
                    for line in current_file_as_string_list_2:
                        print line
                    print '________________________________________________________________________________________________'

                    files_as_string_1.append(current_file_as_string_list_1)
                    files_as_string_2.append(current_file_as_string_list_2)
                    current_file_pair = [file1,file2]
                    file_name_list.append(current_extension)
                    file_pair_list.append(current_file_pair)
                #except:
                #continue
        except:
            e = open('error.txt', 'a+')
            e.write('   Errors occurred in file: ' + file1 + '.\n')
            continue
'''
result = chardet.detect(line)
char = result['encoding']
print result
print line.decode(char)
print line
line = line.encode('utf-8', 'ignore')
'''

'''
try:
                    for line in text_file_2:
                        print line
                        current_file_as_string_list_2_set.add(line)
                        current_file_as_string_list_2.append(line)
                except:
                    text_file_2 = codecs.open(current_file_folder2, "r", char)
                    print text_file_2
                    text_file_2 = open(current_file_folder2, 'r').readlines()
                    print text_file_2
                    for line in text_file_2:
                        print line

'''



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







    #print len(files_as_string_1)
    #print len(files_as_string_2)


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




if __name__ == "__main__":
    main()




