from difflib import SequenceMatcher

a = [[0 for i in range(20)] for j in range(10)]
print a

b = 0
for i in range(10):
    for j in range(20):
        b = i + j
        a[i][j] = b

for i in range(10):
    print a[i]
'''
a = 'member PARAM1482 parameter 3221267659'
b = 'variable percentRange2 float 20122'

current_file_B = []
file_A_diff = []

for i in range(10):
    current_file_B.append(i)
    file_A_diff.append(i)

print current_file_B
print file_A_diff

similarity_percentage = [[0]*10]*10

print similarity_percentage

for i in range(len(file_A_diff)):
    for j in range(len(current_file_B)):
        similarity_percentage[i][j] = SequenceMatcher(None, file_A_diff[i], current_file_B[j]).ratio()

print similarity_percentage


print SequenceMatcher(None, a, b).ratio()

'''

