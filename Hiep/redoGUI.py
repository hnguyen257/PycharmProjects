
import os
import shutil

f = open('RedoGUI.txt', 'w+')

current_directory = os.getcwd()
current_file_path = current_directory + '\\' + 'RedoGUI.txt'
cmd_file_path = current_directory + '\\' + 'RedoGUI.cmd'
command = "pip install chardet" + "\n"
command = command + "pip install pyinstaller" + "\n"
command = command + "pyinstaller --onefile --noconsole " + current_directory + "\GUI.py"
f.write(command)
f.close()

if os.path.exists(cmd_file_path):
    os.remove(cmd_file_path)

os.rename(current_file_path, cmd_file_path)

os.system(cmd_file_path)
if os.path.exists(current_directory + '\GUI.exe'):
    os.remove(current_directory + '\GUI.exe')

os.rename(current_directory + '\\dist\\GUI.exe', current_directory + '\GUI.exe')
os.remove(current_directory + '\\GUI.py')
os.remove(current_directory + '\\GUI.spec')
os.remove(current_directory + '\\RedoGUI.cmd')
shutil.rmtree(current_directory + '\\build')
shutil.rmtree(current_directory + '\\dist')
os.remove(current_directory + '\\redoGUI.py')

if os.path.exists(current_directory + '\\Installation.bat'):
    os.remove(current_directory + '\\Installation.bat')
if os.path.exists(current_directory + '\\python-2.7.16(32_bit_version).msi'):
    os.remove(current_directory + '\\python-2.7.16(32_bit_version).msi')
if os.path.exists(current_directory + '\\python-2.7.16(64_bit_version).msi'):
    print 'yes'
    os.remove(current_directory + '\\python-2.7.16(64_bit_version).msi')
