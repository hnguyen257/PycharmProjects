from difflib import SequenceMatcher

a = 'member PARAM1482 parameter 3221267659'
b = 'variable percentRange2 float 20122'

print SequenceMatcher(None, a, b).ratio()




