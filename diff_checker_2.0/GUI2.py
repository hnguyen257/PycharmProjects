import Tkinter
import tkFileDialog

def main():

    Tkinter.Tk().withdraw() # Close the root window
    in_path = tkFileDialog.askopenfilename()
    print in_path

if __name__ == "__main__":
    main()