__author__ = 'keertisekharsahoo'
import os
import sys
import subprocess
import re
import json
import pymysql
import insertData
import insertDataDjango
# Django
# from django.db import models
videoDictionary = {}
# global conn
def videoFilePreprocessor():
    base = "/Users/keertisekharsahoo/Documents/Masters Project/Video Inventory"
    showNames = os.listdir(base)
    # print(os.path.isdir("/Users/keertisekharsahoo/Documents/Master's Project/Friends"))
    for show in showNames:
        # print("base + show",base +"/"+ show)
        if(os.path.isdir(base + "/" + show)):
            # print(show)
            seasonsList = os.listdir(base + "/" + show)
            for season in seasonsList:
                if(os.path.isdir(base +"/"+ show+"/"+season)):
                    # print("season",season)
                    episodesList = os.listdir(base +"/"+ show+"/"+season)
                    for episode in episodesList:
                        if ((episode.endswith('.mkv'))):
                            # print("episode ",episode)
                            showID = 123 # for friends
                            #  print(videoDictionary)
                            episodeURL = base +"/"+ show+"/"+season + "/" +episode
                            # print("episode url",episodeURL)
                            # sys.exit(0)
                            episodeNo = episode.split(' ')[0]
                            # print("season",season)
                            list = [showID, season, episodeNo, episodeURL, getDuration(episodeURL)]
                            # videoDictionary[episode] = {};
                            # videoDictionary[episode][showID]={}
                            # videoDictionary[episode][showID][season] = {};
                            videoDictionary[episode] = list;

    # print(videoDictionary)
    # sys.exit(0)
def testMethod():
    for key in videoDictionary:
        print(key)
def printData():
    for key in videoDictionary:
        print(videoDictionary.get(key))
        # print(videoDictionary.get(key))
def connectToDatabase():
    print("Connecting to the Database")
    conn = pymysql.connect(db='ThruLineDB', user='root', passwd='pwd', host='127.0.0.1')
    return conn
def createTables(cursor):
    print("Creating Tables...")
    sql = """CREATE TABLE IF NOT EXISTS VIDEOS
              (
              id INT NOT NULL,
              season_id INT,
              episode_no INT,
              episode_url VARCHAR(255),
              duration INT
              )"""
    cursor.execute(sql)
    sql = """CREATE TABLE IF NOT EXISTS SHOWS
            (
            id INT,
            name VARCHAR(255),
            video_url VARCHAR(255)
            )"""
    cursor.execute(sql)

    sql = """ CREATE TABLE IF NOT EXISTS DIALOGUES
              (
              id INT,
              character_id VARCHAR(255),
              raw_text VARCHAR(255),
              keyword VARCHAR(255),
              start_time INT,
              end_time INT,
              FULLTEXT (raw_text, keyword)
              )"""
    cursor.execute(sql)

    sql = """ CREATE TABLE IF NOT EXISTS CHARACTERS
              (
              id INT,
              name VARCHAR(255),
              show_id INT,
              actor_id INT
              )"""
    cursor.execute(sql)

    sql = """ CREATE TABLE IF NOT EXISTS ACTORS
              (
              id INT,
              name VARCHAR(255),
              photo_url VARCHAR(255)
              )"""
    cursor.execute(sql)

    sql = """CREATE TABLE IF NOT EXISTS REQUESTS
              (
              id INT ,
              keyword VARCHAR(255),
              season INT,
              episode INT,
              characters VARCHAR(255),
              FULLTEXT(keyword)
              )
              """
    cursor.execute(sql)

def insertVideos(cursor,id, season_id, episode_no,episode_url,duration):
    sql = "INSERT INTO VIDEOS VALUES(%d, %d, %d, '%s', %d)" % (id,season_id, episode_no,episode_url,duration)
    cursor.execute(sql)

def insertShows(cursor, id, show_name, video_url):
    sql = """INSERT INTO SHOWS
    VALUES(id, name, video_url)"""
    cursor.execute(sql)

def insertDialogues(cursor, id, raw_text,keyword, start_time, end_time ):
    sql = """INSERT INTO DIALOGUES
              VALUES(id, raw_text, keyword, start_time, end_time)"""
    cursor.execute(sql)

def insertCharacters(cursor, id, character_name, show_id, actor_id):
    sql = """INSERT INTO CHARACTERS
            VALUES(id, character_name, show_id, actor_id)"""
    cursor.execute(sql)

def insertActors(cursor, id, actor_name, photo_url):
    sql = "INSERT INTO ACTORS VALUES(%d, '%s', '%s')" % (id, actor_name, photo_url)
    cursor.execute(sql)

# def insertActors(cursor):
#     sql = """INSERT INTO ACTORS
#             VALUES(789, 'Joey', '/c/folder/friends')"""
#     cursor.execute(sql)

def insertRequests(cursor, id, keyword, episode, season, characters):
    print("id ",keyword)
    sql = "INSERT INTO REQUESTS VALUES(%d, '%s',%d,'%s','%s') % (id, keyword, episode, season, characters)"
    cursor.execute(sql)

    JSON string format data

first_name = models.CharField(max_length=30)
last_name = models.CharField(max_length=30)

class VIDEOS(models.Model):
    id = models.IntegerField()
    season_id = models.CharField(max_length = 30)
    episode_no = models.IntegerField()
    episode_url = models.CharField(max_length = 30)
    duration = models.IntegerField()

class SHOWS(models.Model):
    id = models.IntegerField()
    show_name = models.CharField(max_length = 30)
    video_url = models.CharField(max_length = 50)

class DIALOGUES(models.Model):
    id = models.IntegerField()
    character_id = models.CharField(max_length = 30)
    raw_text = models.TextField(max_length = 30)
    keyword = models.CharField(max_length = 30)
    start_time = models.IntegerField()
    end_time = models.IntegerField()

class CHARACTERS(models.Model):
    id = models.IntegerField()
    character_name = models.CharField(max_length = 30)
    show_id = models.IntegerField()
    actor_id = models.IntegerField()

class ACTORS(models.Model):
    id = models.IntegerField()
    actor_name = models.CharField(max_length = 30)
    photo_url = models.CharField(max_length = 30)

class REQUESTS(models.Model):
    id = models.IntegerField()
    keyword = models.TextField(max_length = 30)
    season = models.IntegerField()
    episode = models.IntegerField()
    characters = models.CharField(max_length = 30)

def insertVideos(id,season_id, episode_no,episode_url,duration):
    v = VIDEOS(id= id,season_id = season_id, episode_no = episode_no,episode_url = episode_url,duration = duration)
    v.save()

def insertShows(id, show_name, video_url):
    s = SHOWS(id = id, show_name = show_name, video_url = video_url)
    s.save()

def insertDialogues(id, raw_text,keyword, start_time, end_time):
    d = DIALOGUES(id = id, raw_text = raw_text,keyword = keyword, start_time = start_time, end_time = end_time)
    d.save()

def insertCharacters(id, character_name, show_id, actor_id):
    c = CHARACTERS(id = id, character_name = character_name, show_id = show_id, actor_id = actor_id)
    c.save()

def insertActors(id, actor_name, photo_url):
    a = ACTORS(id = id, actor_name = actor_name, photo_url = photo_url)
    a.save()

def insertRequests(id, keyword, episode, season, characters):
    r = REQUESTS(id = id, keyword = keyword, episode = episode, season = season, characters = characters)
    r.save()

def fetchDataForThumbnailDisplay(cursor, keyword):
    sql = """ SELECT VIDEOS.EPISODE_URL AS URL, (DIALOGUES.END_TIME - DIALOGUES.START_TIME) AS DURATION
    FROM DIALOGUES WHERE MATCH(RAW_TEXT) AGAINST(keyword)
    """
    cursor.execute(sql)
    data = cursor.fetchall()
    return data

def getData(cursor, tableName):
    sql = """ SELECT * FROM tableName"""
    cursor.execute(sql)
    data = cursor.fetchall()
    print("data is ",data)

def dropTable(cursor, tableName):
    print("Dropping table: ",tableName)
    sql = """DROP TABLE tableName"""
    cursor.execute(sql)


def insertIntoDataBase(cursor):
    print("Inserting into database......")
    # sql = """.schema shows"""
    for key in videoDictionary:
        id = videoDictionary.get(key)[0]
        season_id = videoDictionary.get(key)[1]
        episode_no = videoDictionary.get(key)[2]
        url = videoDictionary.get(key)[3]
        duration = videoDictionary.get(key)[4]
        sql = """ INSERT INTO VIDEOS
                  VALUES(id,season_id,episode_no,url,duration) """
        cursor .execute(sql)
    # sql = """ INSERT INTO VIDEOS
    #           VALUES(12,'FRND', 10,'frends/sesn10/eps1/',20)"""
    # cursor.execute(sql)
    # sql = """  INSERT INTO ACTORS
    #             VALUES(100,'Keanu Reeves','c/mycomp/foo/myfiles')"""
    # cursor.execute(sql)
    # cursor.close()
def getDataFromDatabase(cursor):
    print("getting data from the database")
    sql = """  SELECT * FROM VIDEOS """
    cursor.execute(sql)



fileName = "/Users/keertisekharsahoo/Documents/Masters Project/Video Inventory"
def getLength(fileName):
    print("file path is:",fileName)
    result = subprocess.Popen(["ffprobe", fileName, '-print_format', 'json', '-show_streams', '-loglevel', 'quiet'],
     stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    return float(json.loads(result.stdout.read())['streams'][0]['duration'])

def getDuration(episodeURL):
    try:
        process = subprocess.Popen(['/usr/bin/ffmpeg',  '-i', episodeURL], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
    except Exception:
        pass
    return 0
def main():
    # videoFilePreprocessor()
    # testMethod()
    # duration = getLength(fileName)
    insertDataObj = insertData.DataManipulation()
    connObj = insertDataObj.connectToDatabase()
    cursor = connObj.cursor()
    insertDataObj.createTables(cursor)
    # dropTable(cursor)
    # insertIntoDataBase(cursor)
    # id, keyword, episode, season, characters
    # insertRequests(cursor, 110, 'how u doing ?', 23, 45, 'Ross')
    # insertActors(cursor, 400, 'Joey','c/mycomp/foo')
    insertDataObj.insertVideos(cursor, 4, 5, 6,'/foo/video/floder',203)
    insertDataObj.insertShows(cursor, 24, 'frnds','/video/fr1/')
    insertDataObj.insertDialogues(cursor, 99, 2, 'test', 'test', 100,999)
    insertDataObj.insertCharacters(cursor, 99, 'test', 67, 89)
    insertDataObj.insertActors(cursor, 43, 'test','test')
    insertDataObj.insertRequests(cursor, 123, 'wqndlnlqwdl  nwldnlenwdnldw  n   ldnlendl    nlnewldnl   nqwlnw  dlnldnw ndn920102fekdnckn 88 jj')
    # insertActors(cursor)
    # getData(cursor, ACTORS)
    # data = fetchDataForThumbnailDisplay(cursor)
    connObj.commit()
    cursor.close()
    print("Done with database manipulation and committed the changes.")

if __name__ == "__main__":
    main()