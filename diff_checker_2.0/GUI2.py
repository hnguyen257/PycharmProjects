from Tkinter import *
import ttk
import numpy as np

root = Tk()

files = iter(np.arange(1,10))


downloaded = IntVar()

def loading():
    downloaded.set(next(files)) # update the progress bar
    root.update()

def manager():
    loading()
    loading()
    loading()
    loading()
    loading()


'''
def loading():
    try:
        downloaded.set(next(files)) # update the progress bar
        root.after(1, loading) # call this function again in 1 millisecond
    except StopIteration:
        # the files iterator is exhausted
        root.destroy()
'''

progress= ttk.Progressbar(root, orient = 'horizontal', maximum = 10, variable=downloaded, mode = 'determinate')
progress.pack(fill=BOTH)
start = ttk.Button(root,text='start',command=manager)
start.pack(fill=BOTH)

root.mainloop()


'''
from Tkinter import *
import ttk
import numpy as np
import time

root = Tk()

files = iter(np.arange(1,10))


downloaded = IntVar()
value = 0

def loading():
    global value
    value = value + 1
    downloaded.set(1)  # update the progress bar

def manager():
    loading()
    loading()
    loading()

progress= ttk.Progressbar(root, orient = 'horizontal', maximum = 3, variable=0, mode = 'determinate')
progress.pack(fill=BOTH)
start = ttk.Button(root,text='start',command=manager)
start.pack(fill=BOTH)

root.mainloop()




from Tkinter import *
import ttk
import numpy as np
import time

root = Tk()

files = iter(np.arange(1,100))


downloaded = IntVar()
def loading():
    try:
        downloaded.set(100) # update the progress bar
        root.after(1, loading) # call this function again in 1 millisecond
    except StopIteration:
        # the files iterator is exhausted
        root.destroy()


progress= ttk.Progressbar(root, orient = 'horizontal', maximum = 100, variable=downloaded, mode = 'determinate')
progress.pack(fill=BOTH)
start = ttk.Button(root,text='start',command=loading)
start.pack(fill=BOTH)

root.mainloop()

'''