__author__ = 'keertisekharsahoo'
import urllib2
import sys
import os
# import sqlite3
import sqlite3 as lite
from bs4 import BeautifulSoup
subtitleDataList = []
class DataPreProcessor():

    def getConnection(self):
        print("connecting.....")
        con = lite.connect('/Users/keertisekharsahoo/Documents/Masters Project/thruline/ThruLineDjango/db.sqlite3')
        # cursor = con.cursor()
        # cursor.execute("INSERT INTO ThruLine_video VALUES(9,10,2,'friends/s2/Phoebe.mp4',30)")
        # con.commit()
        return con

    def preProcessScriptFiles(self):
        debug = False
        print("OMM")
        #Open a file
        fOpen = open("/Users/keertisekharsahoo/Documents/Masters Project/Scripts/season10/1002.html")
        # # line = fOpen.readline()
        # for line in fOpen.readlines():
        #     print(line)
        soupObj = BeautifulSoup(open("/Users/keertisekharsahoo/Documents/Masters Project/Scripts/season10/1001.html"))
        # print("soupObj",soupObj)
        titleTag = soupObj.title
        title = titleTag.contents
        # print("title",title)
        bodyTag = soupObj.body
        # print("bodyTag",bodyTag)
        for child in bodyTag.descendants:
            # print("child",child)
            pass
        pTag = soupObj.html.body.p
        # print("ptag",pTag)
        #list with all p tags. iterate through list length and find texts
        list = soupObj.find_all("p")
        # print("list",list[0])
        # print("list",list[0].contents)
        # print("list",list[1])
        print("type of list",type(list))
        # str = list[2]._str_('charset')
        # str = unicode.join(u'\n',map(unicode,list[2]))
        str1 = str(list[2])
        # print("type",type(str1))
        print("string version of list is ",str1)
        str2 = str1.split(":")
        print("text within the tags",str2[1])
        finalText = str2[1].replace("\r\n","").replace("</p>","")

        # print("string vesrion of result: ",str1)
        if debug:
            print("list ",list[2])
            strongList = list[2].find_all("strong")
            print("strong list",strongList)
            pTag = list[2].p
            print("p tag",pTag)
            strongTag = list[2].strong
            print("strongTag",strongTag)

            print("text within p tag",list[2].string)
            print("text within strong tag",strongTag.string)
        print("===================")
        for line in list:
            strongTag = line.strong
            # print(type(strongTag))
            if strongTag != None:
                character = str(strongTag.string)
                # print("Character: ",character)
                try:
                    strLine = str(line).split(":")[1]
                    finalText = strLine.replace("\r\n","").replace("</p>","").replace("<em>","").replace("</em>","")
                    # print(finalText)
                    print(character+" : "+finalText)
                except IndexError:
                    pass
            else:
                pass

    def preProcessSubtitleFiles(self):
        basePath = "/Users/VideoInventory/Friends/S01/"
        filesList = os.listdir(basePath)
        srtAndVideoUrlDictionary = {}
        saveStatus = False
        value = ""
        key = ""
        for file in filesList:
            # print(file)
            if(file.endswith("srt")):
                key = file
                value = file.replace("srt","mkv")
                srtAndVideoUrlDictionary[key] = basePath + value
        # print(srtAndVideoUrlDictionary)
        # sys.exit(0)
        # subtitleDataList = []
        dialogue = []

        for file in srtAndVideoUrlDictionary:
            # print(type(file))
            # print(str(file))
            # sys.exit(0)
            file = basePath + file
            fOpen = open(file)
            # print(fOpen)
            line = fOpen.readline()
            dialogueStatus = False

            text = ""
            while( line != ""):
                # print(type(line),line)
                if(dialogueStatus):
                    # print("dia",line)
                    text += " " + line.split("\r\n")[0].replace("-","")
                    # dialogue.append(line.split("\r\n")[0])
                if(line.__contains__("-->")):
                    # print(line)
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

            print("subtitle data")
            for data in subtitleDataList:
                print("data",data)
            sys.exit(0)


    def insertIntoEpisodeTable(self, cursor):
        basePath = "/Users/VideoInventory/Friends/"
        seasonsList = os.listdir(basePath)
        # print(seasonsList)
        episodeID = 1
        for season in seasonsList:
            if not season.startswith('.DS_Store'):
                print("Season ", season,"-----------------------")
                # print(season)  # season = S01
                seasonID = season[-2:] #  seasonID = 01, 02..
                # print(seasonID)
                episodeList = os.listdir(basePath+season)
                for episode in episodeList:
                    if not episode.startswith('.DS_Store') and episode.endswith('.srt'):
                        # print(episode) # 01 The One where Monica gets a Roommate.mkv
                        episodeURL = basePath+season+'/'+episode.split(".srt")[0]+".mkv"
                        episodeName = episode[:2]
                        seasonID = int(seasonID)
                        episodeName = int(episodeName)
                        print("Episode Id: ",episodeID,"Season id :",seasonID ,"EpisodeName",episodeName,"episode url",episodeURL)
                        # print(episodeName)
                        cursor.execute("INSERT INTO ThruLine_episode (id, season_id, name, episode_url)VALUES(?, ?, ?, ?)", (episodeID, seasonID, episodeName, episodeURL ))
                        # cursor.execute(sql)
                        episodeID +=1


    def insertIntoDialogueTable(self,cursor):
        basePath = "/Users/VideoInventory/Friends/"
        seasonsList = os.listdir(basePath)
        count = 0
        dialogueID = 0
        for seasonName in seasonsList:
            # print("Season",season)
            if not seasonName.startswith('.DS_Store'):
                print("Season: ",seasonName,'----------------')
                seasonID = seasonName[-2:]
                # print("Season id: ",seasonID)
                fileList = os.listdir(basePath+seasonName) # both srt and mkv file
                for file in fileList: # loop over each subtitle file
                    # print("file",file)
                    count +=1
                    raw_text = ""
                    if not file.startswith('.DS_Store') and file.endswith(".srt"):
                        subtitleFileName = file
                        # print(file)
                        episodeName = file[:2]
                        # print("Episode Name: ",episodeName)
                        # sys.exit(0)
                        # print("Subtitle file name: ",subtitleFileName)
                        subtitleFilePath = basePath+seasonName+"/"+subtitleFileName
                        print("Subtitle file path: ", subtitleFilePath)
                        fOpen = open(subtitleFilePath)
                        line = fOpen.readline()
                        dialogueStatus = False
                        # raw_text = ""
                        while( line != ""):
                            # print("line",line)
                            if(dialogueStatus):
                                raw_text += " " + line.split("\r\n")[0].replace("-","")
                            if(line.__contains__("-->")):
                                dialogueStatus = True
                                startTime = line.split("-->")[0]
                                endTime = line.split("-->")[1].split("\r\n")[0]
                            line = fOpen.readline()
                            if(line == "\r\n"):
                                dialogueStatus = False
                                # print("Dialogue id: ",dialogueID)
                                # print("Season id: ",seasonID,"Episode name: ",episodeName)
                                episodeIDTuple = self.getEpisodeID(cursor, int(seasonID), int(episodeName))
                                episodeID = episodeIDTuple[0]
                                # print("Episode id",type(episodeID))
                                # print(startTime)
                                print("raw_text :", raw_text,"start_time", startTime,"end time: ",endTime,"dialogue id:",dialogueID)
                                # sql = "
                                cursor.execute("INSERT INTO ThruLine_dialogue (id, episode_id, raw_text, start_time, end_time) VALUES(?, ?, ?, ?, ?)",(dialogueID, episodeID, raw_text, startTime, endTime))
                                self.insertDataIntoIndexedDialogueTable(cursor, dialogueID, episodeID , raw_text)
                                dialogueID +=1
                                raw_text = ""
        # sys.exit(0)

    def createIndexTableForFullTextSearch(self, cursor):
        sql = """CREATE VIRTUAL TABLE indexed_dialogue USING fts3(dialogue_id,episode_id, raw_text)"""
        cursor.execute(sql)

    def insertDataIntoIndexedDialogueTable(self,cursor,dialogue_id,episode_id, raw_text):
        cursor.execute("INSERT INTO indexed_dialogue(dialogue_id, episode_id, raw_text) VALUES(?,?,?)",(dialogue_id,episode_id, raw_text))

    def getEpisodeID(self,cursor,seasonID, episodeName):
        sql = "SELECT id FROM ThruLine_episode WHERE season_id = %d and name = %d " % (seasonID, episodeName)
        cursor.execute(sql)
        episodeID = cursor.fetchone()
        return episodeID
    def dropTable(self, cursor):
        sql = "DROP TABLE indexed_dialogue"
        cursor.execute(sql)

    def insertIntoSeasonTable(self, cursor):
        for i in range(1,11):
            sql = "INSERT INTO ThruLine_season VALUES(%d, %d)" % (i, i)
            cursor.execute(sql)

    def func(self):
        for i in range(1,11):
            # print(i)
            sql = "INSERT INTO Season VALUES(%d, %d)" % (i, i)
            print(sql)


    def getData(self, cursor):
        # sql = "SELECT * FROM ThruLine_episode"
        # sql = "SELECT * FROM ThruLine_season"
        # sql = "SELECT * FROM ThruLine_dialogue"
        sql = "SELECT * FROM indexed_dialogue"
        cursor.execute(sql)
        data = cursor.fetchall()
        print("Data is")
        for dat in data:
            print(dat)

    def fetchDataWithFTS(self,cursor):
        # sql = """ SELECT * FROM Table1_indx WHERE Table1_indx MATCH 'Mike such' """
        sql = "SELECT id from indexed_dialogue WHERE indexed_dialogue MATCH 'HOW YOU DOING'"
        cursor.execute(sql)
        data = cursor.fetchall()
        print("FTS result")
        print(data)
        # for dat in data:
            # print(dat)

    def truncateTable(self,cursor):
        # sql = "DELETE FROM indexed_dialogue"
        sql = "DELETE FROM ThruLine_dialogue"
        cursor.execute(sql)

    def fullTextSearch(self, cursor):
        inputList = [1,7,13,21,23,24,32,33,34,35,36,37,38,46,58,67,68,71,72,83,84,89,90,93,96,97,102,108,110,113,115,120,121,122,126,128,130131,132,133,135,143,146,154,157,163,164168,180,184,187,189,196,197,199,201,207,208,209,218]
        # print("list",inputList)
        dialogueIdList = []
        outputList = []
        # for episodeID in list:
        # sql = "SELECT indexed_dialogue.raw_text, ThruLine_dialogue.start_time, ThruLine_dialogue.end_time FROM ThruLine_dialogue INNER JOIN indexed_dialogue ON ThruLine_dialogue.episode_id = indexed_dialogue.id WHERE indexed_dialogue MATCH 'HOW YOU DOING' AND indexed_dialogue.id = 1"
        for episodeID in inputList:
            cursor.execute("SELECT dialogue_id FROM indexed_dialogue WHERE indexed_dialogue MATCH 'HOW YOU DOING' AND episode_id = %d " % (episodeID))
            data = cursor.fetchall()
            # print("data",data)
            dialogueIdList.append(data)
        # print("dialogue id list",dialogueIdList)
        for dialogue_id in dialogueIdList:
            # print("dialogue id",dialogue_id)
            for i in range(0,len(dialogue_id)):
                # pass
                # print("#",dialogue_id[i])

                cursor.execute("SELECT raw_text, start_time, end_time FROM ThruLine_dialogue WHERE id = %d" % (dialogue_id[i]))
                dat = cursor.fetchall()
                outputList.append(dat)
        # print("dat")
        for ele in outputList:
            print(ele)
        # cursor.execute(sql)
        # data = cursor.fetchall()
        # print("fts",data)
        # print(list.__len__())


def main():
    obj = DataPreProcessor()
    # obj.func()
    # obj.preProcessScriptFiles()
    con = obj.getConnection()
    cursor = con.cursor()
    con.text_factory = str
    # obj.truncateTable(cursor)
    # obj.dropTable(cursor)
    # obj.createIndexTableForFullTextSearch(cursor)
    # obj.getData(cursor)
    # obj.fetchDataWithFTS(cursor)
    # obj.insertIntoSeasonTable(cursor)
    # obj.preProcessSubtitleFiles()
    obj.insertIntoEpisodeTable(cursor)
    # obj.createIndexTableForFullTextSearch(cursor)
    # obj.insertIntoDialogueTable(cursor)
    # obj.preProcessSubtitleFiles()
    # obj.fullTextSearch(cursor)





    con.commit()
if __name__ == "__main__":
        main()

