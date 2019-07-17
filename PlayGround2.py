import Tkinter as tk



if __name__ == '__main__':
    root = tk.Tk()
    widget = tk.Label(root, compound='top')
    widget.lenna_image_png = tk.PhotoImage(file="logo2.gif")
    widget['text'] = "Lenna.png"
    widget['image'] = widget.lenna_image_png
    widget.pack()
    root.mainloop()
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