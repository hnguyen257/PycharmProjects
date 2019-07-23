
import os
import shutil

f = open('RedoGUI.txt', 'w+')

current_directory = os.getcwd()
current_file_path = current_directory + '\\' + 'RedoGUI.txt'
cmd_file_path = current_directory + '\\' + 'RedoGUI.cmd'
command = "pyinstaller --onefile --noconsole " + current_directory + "\GUI.py"

f.write(command)
f.close()

os.rename(current_file_path, cmd_file_path)

os.system(cmd_file_path)

os.rename(current_directory + '\\dist\\GUI.exe', current_directory + '\GUI.exe')
os.remove(current_directory + '\\GUI.py')
os.remove(current_directory + '\\GUI.spec')
os.remove(current_directory + '\\RedoGUI.cmd')
shutil.rmtree(current_directory + '\\build')
shutil.rmtree(current_directory + '\\dist')
os.remove(current_directory + '\\redoGUI.py')


