
line_A = '<AlarmString>Device Not Responding</AlarmString>'
line_B = '<AlarmString>Device Not connected</AlarmString>'

#line by line character highlights
def character_highlight(line_A, line_B):
    k = 0
    ret = ''
    last_result = 0 # 0 means same, 1 means different
    for i in range(len(line_A)):
        found = 0
        for j in range(k, len(line_B)):
            #print line_A[i]
            #print line_B[j]
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
        #print ret
        #print "________"


    ret = escapeHtml(ret)
    ret = ret.replace('+=^', '<').replace('^=+', '>').replace('#$@','"')
    return ret









def escapeHtml(unsafe):
    safe = unsafe.replace('&', "&amp;").replace('<', "&lt;").replace('>', "&gt;").replace('"', "&quot;").replace("'", "&#039;");
    return safe

print character_highlight(line_A, line_B)
print character_highlight(line_B, line_A)

'''
past example:
+ Name "amp_cal_t1_re.00004E70.0000.0000",
+ Name "amp_cal_t1_re.00004E70.0070.0000",
'''





'''
from difflib import SequenceMatcher


a= '<Severity>ALERT_MAINT_ID</Severity>'
b= '<Severity> </Severity>'
print SequenceMatcher(None, a, b).ratio()
'''