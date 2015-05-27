import pysrt
import os
from bs4 import BeautifulSoup
import sys
import ntpath

def get_filepaths(directory):

    file_paths = []

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename) # Join the two strings in order to form the full filepath.
            file_paths.append(filepath)  # Add it to the list.

    return file_paths

# Run the above function and store its results in a variable.
full_file_paths = get_filepaths("/Users/shreyarajani/MSCS/MS-Sem4/Masters-Project/PythonCode/Preprocessing/Friends-Script")

def readingdir(x,y):
    for f1 in x:
        print "F1: ", f1
        for f2 in y:
            print "F2: ", f2

            with open(f1, 'r') as file1:
                with open(f2, 'r') as file2:
                    same = set(file1).intersection(file2)

                    #print "SAME: ", same
    same.discard('\n')

    with open('a.txt', 'w') as file_out:
        for line in same:
            file_out.write(line)

if __name__ == "__main__":

    x = get_filepaths('/Users/shreyarajani/MSCS/MS-Sem4/Masters-Project/PythonCode/Preprocessing/Friends-Script')

    #Going through the SRT files
    y = get_filepaths('/Users/shreyarajani/MSCS/MS-Sem4/Masters-Project/PythonCode/Preprocessing/Friends-Subtitles')

    get_filepaths(x)
    readingdir(x,y)
