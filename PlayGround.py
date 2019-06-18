

f = open("testing.html", "w+")
f.write("\<!DOCTYPE html\>
<html>
<body>

<p><font color="red">This is some text!</font></p>
<p><font color="blue">This is some text!</font></p>

<p>The color attribute is not supported in HTML5. Use CSS instead.</p>

</body>
</html>
")




'''

def cheeseshop(kind, kindb, *b, **a):
    print "-- Do you have any " + kind + "?"
    print "-- I'm sorry, we're all out of " + kindb
    for i in a:
        print(i)
    print "-" * 40
    for j in b:
        print j


cheeseshop("Limburger",
           "It's really very, VERY runny, sir.", "Michael Palin",
           "John Cleese",
           "Cheese Shop Sketch", abc = "blah", daef="blah blah", ghi = "blah blah blah"
           )

print raw



    print "_______________________________________________________________________________"
    raw2 = io.open(current_file, encoding="ISO-8859-1")
    for line in raw2:
        print line
'''