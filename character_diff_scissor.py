

line_a = '	<Severity>ALERT_FAILED_ID</Severity>'
line_b = '	<Severity>ALERT_FAILED_ID</Severity>'

#line by line character highlights
def character_highlight(line_a, line_b):
    ret = ''
    len_a = len(line_a)
    len_b = len(line_b)
    len_used = len_a
    top_down = 0
    bottom_up = len_used - 1
    if len_a > len_b:
        len_used = len_b
    diff = 0
    for i in range(len_used):
        #print line_a[i]
        #print line_b[i]
        if line_a[i] != line_b[i]:
            diff = 1
            top_down = i
            break

    end_b = len_b - 1
    for i in range(len_a-1, -1, -1):
        #print line_a[i]
        #print line_b[end_b]
        if line_a[i] != line_b[end_b]:
            diff = 1
            bottom_up = i
            break
        end_b = end_b - 1

    print top_down
    print bottom_up

    if bottom_up < top_down:
        holder = top_down
        top_down = bottom_up
        bottom_up = holder
    if diff == 0 or (bottom_up-top_down) == (len_a-1):
        for i in range(len_a):
            ret = ret + line_a[i]
    else:
        #print top_down
        #print bottom_up
        for i in range(top_down):
            ret = ret + line_a[i]
            print ret
        ret = ret + '+=^font style=#$@background-color: #89ED75#$@^=+'
        for i in range(top_down, bottom_up+1):
            ret = ret + line_a [i]
            print ret
        ret = ret + '+=^/font^=+'
        for i in range(bottom_up+1, len_a):
            ret = ret + line_a[i]
            print ret


    ret = escapeHtml(ret)
    ret = ret.replace('+=^', '<').replace('^=+', '>').replace('#$@','"')
    return ret

def escapeHtml(unsafe):
    safe = unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace("'", "&#039;");
    return safe

print character_highlight(line_a, line_b)
print character_highlight(line_b, line_a)









'''

    k = 0
    ret = ''
    last_result = 0 # 0 means same, 1 means different
    for i in range(len(line_A)):
        found = 0
        for j in range(k, len(line_B)):
            ##print line_A[i]
            ##print line_B[j]
            if line_A[i] == line_B[j]:
                if last_result == 1:
                    if i < len(line_A)-1 and j < len(line_B)-1:
                        if line_A[i + 1] == line_B[j + 1]:
                            last_result = 0
                            ret = ret + '+=^/font^=+'
                            ret = ret + line_A[i]
                            k = j + 1
                            found = 1
                            break
                    else:
                        last_result = 0
                        ret = ret + '+=^/font^=+'
                        ret = ret + line_A[i]
                        k = j + 1
                        found = 1
                        break
                else:
                    ret = ret + line_A[i]
                    k = j + 1
                    found = 1
                    break
            else:
                found = 0
                #k = j + 1
                break
        if found == 0:
            if last_result == 0:
                last_result = 1
                ret = ret + '+=^font style=#$@background-color: #89ED75#$@^=+'
            ret = ret + line_A[i]
        ##print ret
        ##print "________"


    ret = escapeHtml(ret)
    ret = ret.replace('+=^', '<').replace('^=+', '>').replace('#$@','"')
    return ret









def escapeHtml(unsafe):
    safe = unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace("'", "&#039;");
    return safe

#print character_highlight(line_A, line_B)
#print character_highlight(line_B, line_A)
'''