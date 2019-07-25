


a = [1,2,3]
b= [i for i in a]
for i in a:
    a[a.index(i)] = 0

print a
print b