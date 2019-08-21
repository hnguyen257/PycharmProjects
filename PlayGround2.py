


a = 'hey'
a = a.replace('e','p')
print a



'''
raw = open("C:\Users\E1260297\Desktop\FL_insurance_sample.csv",'r').readline()
print raw

for i in raw:
    print i
    
    import csv
with open('C:\Users\E1260297\Desktop\FL_insurance_sample.csv', newline='') as csvfile:
    for row in csvfile:
        print row
        
        
        
    print ', '.join(row)
        count = count + 1
        if count == 10:
            break        
        
        
import csv


temp = []
with open('C:\Users\E1260297\Desktop\FL_insurance_sample.csv', 'rU') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    for row in spamreader:
        temp.append(''.join(row))
        count = count + 1
        if count == 5:
            break
    for i in temp:
        print i

        
________
import csv

temp = []
with open('C:\Users\E1260297\Desktop\FL_insurance_sample.csv', 'rU') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    count = 0
    print spamreader[0]
    for row in spamreader:
        temp.append(''.join(row))
        count = count + 1
        if count == 5:
            break
    for i in temp:
        print i
________
'''