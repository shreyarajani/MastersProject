__author__ = 'keertisekharsahoo'
import urllib2
import sys
import os
import sqlite3
from bs4 import BeautifulSoup

class SubtitleFileProcessor():
    def getConnection(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        conn = sqlite3.connect(os.path.join(dir, 'ThruLineDjango/db.sqlite3'))
        conn.text_factory = str
        conn.row_factory = sqlite3.Row
        return conn

    def preProcessSubtitleFiles(self, path):
        basePath = path
        folders = os.listdir(basePath)
        # print("folders",folders)
        for folder in folders:
            if not folder.startswith(".DS_Store"):
                subtitleDirPath = basePath + folder
                filesList = os.listdir(subtitleDirPath)
                srtAndVideoUrlDictionary = {}
                subtitleDataList = []
                saveStatus = False
                value = ""
                key = ""
                for file in filesList:
                    if(file.endswith("srt")):
                        key = subtitleDirPath + "/" +file
                        value = file.replace("srt","mkv")
                        srtAndVideoUrlDictionary[key] = subtitleDirPath + "/" + value
                dialogue = []
                for file in srtAndVideoUrlDictionary:
                    fOpen = open(file)
                    line = fOpen.readline()
                    dialogueStatus = False
                    text = ""
                    while( line != ""):
                        if(dialogueStatus):
                            text += " " + line.split("\r\n")[0].replace("-","")
                        if(line.__contains__("-->")):

                            dialogueStatus = True
                            startTime = line.split("-->")[0]
                            endTime = line.split("-->")[1].split("\r\n")[0]
                        line = fOpen.readline()
                        if(line == "\r\n"):
                            dialogueStatus = False
                            dialogue.append(text)
                            dialogue.append(startTime)
                            dialogue.append(endTime)
                            subtitleDataList.append(dialogue)
                            dialogue = []
                            text = ""
        return subtitleDataList

def main():
    obj = SubtitleFileProcessor()
    obj.preProcessScriptFiles( '/Users/VideoInventory/Friends')

if __name__ == "__main__":
    main()