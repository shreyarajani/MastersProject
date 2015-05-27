__author__ = 'keertisekharsahoo'
import urllib2
import sys
import os
import unicodedata
# import sqlite3
import sqlite3 as lite
from bs4 import BeautifulSoup
subtitleDataList = []
class DataPreProcessor():

    def getConnection(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        conn = lite.connect(os.path.join(dir, 'ThruLineDjango/db.sqlite3'))
        conn.text_factory = str
        conn.row_factory = lite.Row
        return conn

    def insertIntoSeasonTable(self, cursor):
        for i in range(1,11):
            sql = "INSERT INTO ThruLine_season VALUES(%d, %d)" % (i, i)
            cursor.execute(sql)

    def insertIntoEpisodeTable(self, cursor):
        basePath = "/Users/VideoInventory/Friends/"
        seasonsList = os.listdir(basePath)
        # print(seasonsList)
        episodeID = 1
        for season in seasonsList:
            if not season.startswith('.DS_Store'):
                seasonID = season[-2:] #  seasonID = 01, 02..
                episodeList = os.listdir(basePath+season)
                for episode in episodeList:
                    if not episode.startswith('.DS_Store') and episode.endswith('.srt'):
                        episodeURL = basePath+season+'/'+episode.split(".srt")[0]+".mkv"
                        episodeName = episode[:2]
                        seasonID = int(seasonID)
                        episodeName = int(episodeName)
                        # print("Episode Id: ",episodeID,"Season id :",seasonID ,"EpisodeName",episodeName,"episode url",episodeURL)
                        cursor.execute("INSERT INTO ThruLine_episode (id, season_id, name, episode_url)VALUES(?, ?, ?, ?)", (episodeID, seasonID, episodeName, episodeURL ))
                        episodeID +=1


    def insertIntoDialogueTable(self,cursor):
        basePath = "/Users/VideoInventory/Friends/"
        seasonsList = os.listdir(basePath)
        count = 0
        dialogueID = 0
        for seasonName in seasonsList:
            if not seasonName.startswith('.DS_Store'):
                seasonID = seasonName[-2:]
                fileList = os.listdir(basePath+seasonName)
                for file in fileList:
                    count +=1
                    raw_text = ""
                    if not file.startswith('.DS_Store') and file.endswith(".srt"):
                        subtitleFileName = file
                        episodeName = file[:2]
                        subtitleFilePath = basePath+seasonName+"/"+subtitleFileName
                        fOpen = open(subtitleFilePath)
                        line = fOpen.readline()
                        dialogueStatus = False
                        while( line != ""):
                            if(dialogueStatus):
                                raw_text += " " + line.split("\r\n")[0].replace("-","")
                            if(line.__contains__("-->")):
                                dialogueStatus = True
                                startTime = line.split("-->")[0]
                                endTime = line.split("-->")[1].split("\r\n")[0]
                            line = fOpen.readline()
                            if(line == "\r\n"):
                                dialogueStatus = False
                                episodeIDTuple = self.getEpisodeID(cursor, int(seasonID), int(episodeName))
                                episodeID = episodeIDTuple[0]
                                # print("raw_text :", raw_text,"start_time", startTime,"end time: ",endTime,"dialogue id:",dialogueID)
                                cursor.execute("INSERT INTO ThruLine_dialogue (id, episode_id, raw_text, start_time, end_time) VALUES(?, ?, ?, ?, ?)",(dialogueID, episodeID, raw_text, startTime, endTime))
                                self.insertDataIntoIndexedDialogueTable(cursor, dialogueID, episodeID , raw_text)
                                dialogueID +=1
                                raw_text = ""

    def createIndexTableForFullTextSearch(self, cursor):
        sql = """CREATE VIRTUAL TABLE indexed_dialogue USING fts3(dialogue_id,episode_id, raw_text)"""
        cursor.execute(sql)

    def insertDataIntoIndexedDialogueTable(self,cursor,dialogue_id,episode_id, raw_text):
        cursor.execute("INSERT INTO indexed_dialogue(dialogue_id, episode_id, raw_text) VALUES(?,?,?)",(dialogue_id,episode_id, raw_text))

    def fullTextSearch(self, cursor, inputList, keyword):
        dialogueIdList = []
        outputList = []
        for episodeID in inputList:
            cursor.execute("SELECT dialogue_id FROM indexed_dialogue WHERE indexed_dialogue MATCH %s AND episode_id = %d " % (keyword, episodeID))
            data = cursor.fetchall()
            dialogueIdList.append(data)
        for dialogue_id in dialogueIdList:
            for i in range(0,len(dialogue_id)):
                cursor.execute("SELECT raw_text, start_time, end_time FROM ThruLine_dialogue WHERE id = %d" % (dialogue_id[i]))
                dat = cursor.fetchall()
                outputList.append(dat)

        for dialogue in outputList:
            print(dialogue)


    def getEpisodeID(self,cursor,seasonID, episodeName):
        sql = "SELECT id FROM ThruLine_episode WHERE season_id = %d and name = %d " % (seasonID, episodeName)
        cursor.execute(sql)
        episodeID = cursor.fetchone()
        return episodeID



    def fetchDataWithFTS(self,cursor, keyword):
        sql = "SELECT id from indexed_dialogue WHERE indexed_dialogue MATCH %s " % (keyword)
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def truncateTable(self,cursor, table):
        # sql = "DELETE FROM indexed_dialogue"
        sql = "DELETE FROM %s" % (table)
        cursor.execute(sql)




def main():
    obj = DataPreProcessor()
    conn = obj.getConnection()
    cursor = conn.cursor()
    # obj.preProcessScriptFiles()
    # obj.truncateTable(cursor)
    # obj.dropTable(cursor)
    # obj.createIndexTableForFullTextSearch(cursor)
    # obj.getData(cursor)
    # obj.fetchDataWithFTS(cursor,'HOW YOU DOING')
    # obj.insertIntoSeasonTable(cursor)
    # obj.insertIntoEpisodeTable(cursor)
    # obj.createIndexTableForFullTextSearch(cursor)
    # obj.insertIntoDialogueTable(cursor)
    # obj.preProcessSubtitleFiles()
    # inputList = [1,7,13,21,23,24,32,33,34,35,36,37,38,46,58,67,68,71,72,83,84,89,90,93,96]
    # obj.fullTextSearch(cursor, inputList, 'HOW YOU DOING')
    # conn.commit()
if __name__ == "__main__":
        main()

