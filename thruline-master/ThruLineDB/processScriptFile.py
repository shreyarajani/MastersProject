__author__ = 'keertisekharsahoo'
import urllib2
import sys
import os
import sqlite3
from bs4 import BeautifulSoup
class ScriptFileProcessor():
    def getConnection(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        conn = sqlite3.connect(os.path.join(dir, 'ThruLineDjango/db.sqlite3'))
        conn.text_factory = str
        conn.row_factory = sqlite3.Row
        return conn

    def preProcessScriptFiles(self, basePath):
        scriptFolders = os.listdir(basePath)
        characterDialogueList = []
        for singleScriptFolder in scriptFolders:
            if not singleScriptFolder.startswith(".DS_Store"):
                debug = False
                singleScriptFolderPath = basePath + "/" + singleScriptFolder
                scriptFiles = os.listdir(singleScriptFolderPath)
                count = 0
                for scriptFile in scriptFiles:
                    if not(scriptFile.startswith(".DS_Store")):
                        scriptFilePath = singleScriptFolderPath + "/" + scriptFile
                        soupObj = BeautifulSoup(open(scriptFilePath))
                        titleTag = soupObj.title
                        title = titleTag.contents
                        bodyTag = soupObj.body
                        for child in bodyTag.descendants:
                            pass
                        pTag = soupObj.html.body.p
                        list = soupObj.find_all("p")
                        for line in list:
                            if(line.text != None):
                                try:
                                    singleList = []
                                    text = line.text
                                    character = text.split(":")[0].encode('utf8')
                                    dialogue = text.split(":")[1].encode('utf8')
                                    singleList.append(character)
                                    singleList.append(dialogue)
                                    characterDialogueList.append(singleList)
                                except IndexError:
                                    pass
                                except AttributeError:
                                    pass
                            elif(line.span != None):
                                try:
                                    spanTag = line.span
                                    dialogue = spanTag.contents[1].encode("utf8")
                                    character = spanTag.contents[0].string.encode("utf8")
                                    singleList.append(character)
                                    singleList.append(dialogue)
                                    characterDialogueList.append(singleList)
                                except IndexError:
                                    pass
                                except UnicodeEncodeError:
                                    pass
                                except AttributeError:
                                    pass
                            elif(line.strong != None):
                                strongTag = line.strong
                                singleList = []
                                try:
                                    character = str(strongTag.string)
                                    dialogue = line.contents[1].replace("\r\n","").replace("</p>","").replace("<em>","").replace("</em>","")
                                except IndexError:
                                    pass
                                except TypeError:
                                    pass
                                except UnicodeEncodeError:
                                    pass
                                singleList.append(character)
                                singleList.append(dialogue)
                                characterDialogueList.append(singleList)
        return characterDialogueList


def main():
    obj = ScriptFileProcessor()
    obj.preProcessScriptFiles( '/Users/VideoInventory/Friends-Script')

if __name__ == "__main__":
        main()