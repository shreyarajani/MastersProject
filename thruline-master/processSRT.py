import pysrt
import os
from bs4 import BeautifulSoup
import sys
import ntpath

def extractHTML(x,y):


    soup = BeautifulSoup(open("Friends-Script/season01/0101.html"))
    index = 1
    srtdict = {}

    title = ''.join(soup.find('h1'))
    fname = "Friends-Script/season01/0101.html"
    ntpath.basename(fname)
    subs = pysrt.open('Friends-Subtitles/S01/0101.srt')
    fileLen = len(subs)
    head, tail = ntpath.split(fname)
    filename, dot, ext = tail.partition('.')

    for node in soup.findAll('p'):
        dialogues = ''.join(node.findAll(text=True))
        #print "Dialogues: ", dialogues
        character, colon, dia = dialogues.partition(':')

        #print "DIA: ", dia

        for l in range(0,fileLen):
            starttime = subs[l].start
            endtime = subs[l].end
            #timedict[starttime] = endtime
            #srtdict[l] = timedict
            sub = subs[l].text
            #print "SUB: ", sub
        #sys.exit(0)

            if sub in dia or dia in sub:
                #print "sub", sub
                srtdict[index] = {}
                srtdict[index][starttime] = {}
                srtdict[index][starttime][endtime] = {}
                srtdict[index][starttime][endtime] = sub
                index += 1

    file = open(filename+'.txt', 'w+')
    file.write(str(srtdict))
    file.close()

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
    #Going through HTML files
    x = get_filepaths('/Users/shreyarajani/MSCS/MS-Sem4/Masters-Project/PythonCode/Preprocessing/Friends-Script')

    #Going through the SRT files
    y = get_filepaths('/Users/shreyarajani/MSCS/MS-Sem4/Masters-Project/PythonCode/Preprocessing/Friends-Subtitles')

    extractHTML(x,y)