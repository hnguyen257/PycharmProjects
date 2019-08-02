File comparison tool instructions:
Date: 08/02/2019

First time user:
Make sure to copy the entire folder to your local computer before proceeding to the next step
1. Go to "Copy and paste(if no installation needed)" folder
2. Click on GUI to see if the program works on your computer, if it works, copy the three files in there into your whereever you want to use the program. 
3. If it does not work and nothing show up, you have to install it, follow the following step to install your program.


Installation steps:

1. Go to Installation_folder
2. Read installation instruction pdf file for pictures if needed.

2. Install python using the python installer file, choose the 32 or 64 bit version depend on your system.
	(notes: choose install for all users, select all the features, make sure to for the "add python.exe to path", choose "entire feature will be installed on the local hard drive")
3. Click on installation.bat
4. Wait till the GUI.exe file appears, now copy the GUI.exe and 2 logo files(optional) to where you want to store the program.
5. Done.



_______________________________________


Trouble shoot:
1. The program looks like it is freezing sometimes?
- Because the graphic interface Tkinter was run at the same time as the comparison process is running, therefore sometimes it might not be able to update the screen as quick as it should but your comparison process is not freezing.
2. Nothing show up in the report?
- You might want to check the trace back log file, there might be a runtime error occurs
3. When i click on Installation, there was no executable been made?
- You might have a bad python installation on your computer, so even if you already have python install, click on the python installation file, remove the current version, then reinstall it follow the instructions
- Else, you might have your internet connection disabled, please allow internet for installation.
4. My installation process not working?
- Please make sure you did not rename the folder with a space character in between, just keep the old name and it should be able to run, since terminal might not run the command if there is a space character in the path




_______________________________________
+++++++++++++++++++++++++++++++++++++++

Comparing rules:
- The program will skip blank lines and will not count it toward the differences.
- Since the program will auto sort the similar lines line by line, the time it take to compare the 2 files will not depend on the length of the file but the number of differences between them. Usually it takes less than 1 minute for files with less than 20 differences and will increase tremendously as the number of differences between them increases. So if the wait time is too long, you might be comparing 2 set of totally different files.
- If two line looks like they are identical but still flagged as being different, it is because one line might have extra blank space in them, usually in the form of ' ', '\n' or '\r'.



_______________________________________

For any future question and concerns, feel free to contact:
Hiep Nguyen
Email: hiepnguyen8069@gmail.com
Make sure the subject related to EMERSON or else the email might get ignored. Thank you.


		