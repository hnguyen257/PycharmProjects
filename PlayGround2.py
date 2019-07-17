
test = '\n\r'

for i in test:
    if i in ['\n', '\r']:
        print 'yes'
print test

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