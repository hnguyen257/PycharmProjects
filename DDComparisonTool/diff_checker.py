import sys
import os
from os import listdir
import xml.etree.ElementTree as ET


def main():
    paths = sys.argv[1:]


    folder_path = paths[0]
    print folder_path
    files = listdir(folder_path)
    print files

    a = os.getcwd()
    print a

    text_file = open(str(folder_path) + "\\" + files[0], "r")
    lines = text_file.readlines()

    for i in range(len(lines)):
        a = lines[i].decode("utf-8", "ignore")
        print a




if __name__ == "__main__":
    main()






