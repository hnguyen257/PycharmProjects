
import os

current = os.getcwd().replace('\\','/')

print current

if os.path.exists(current):
    print 'yes'