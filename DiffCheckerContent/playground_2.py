from difflib import SequenceMatcher


a = []

for i in range(10):
    c = [i,i+1]
    d = [i+2,i+3]
    a.append([c,d])

print a
print a[0]
print a[0][0]
print a[0][0][0]