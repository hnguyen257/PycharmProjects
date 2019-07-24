
import sys
import traceback
e = open("test_error.txt", 'w+')
try:
    a = 1/0
except:
    #print traceback.print_exc()
    #a = str(traceback.print_exc())
    pass
a = traceback.format_exc()
#print a
'''
e.close()
e = open("test_error.txt", 'r').read()

print "____________"
print e
print "____________"
'''