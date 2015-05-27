__author__ = 'keertisekharsahoo'
import os
import re
import json
import pymysql
class DataManipulation():

    def connectToDatabase(self):
        print("Connecting to the Database")
        conn = pymysql.connect(db='ThruLineDB', user='root', passwd='pwd', host='127.0.0.1')
        return conn
    def createTables(self,cursor):
        print("Creating Tables...")
        sql = """CREATE TABLE IF NOT EXISTS VIDEO
                  (
                  id INT,
                  season_id INT,
                  episode_no INT,
                  episode_url VARCHAR(255),
                  duration INT,
                  PRIMARY KEY(id)
                  )"""
        cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS SHOW
                (
                id INT,
                name VARCHAR(255),
                video_url VARCHAR(255),
                PRIMARY KEY(id)
                )"""
        cursor.execute(sql)

        sql = """ CREATE TABLE IF NOT EXISTS DIALOGUE
                  (
                  id INT,
                  character_id INT,
                  video_id INT,
                  raw_text VARCHAR(255),
                  keyword VARCHAR(255),
                  start_time INT,
                  end_time INT,
                  url VARCHAR(255),
                  FULLTEXT (raw_text, keyword),
                  PRIMARY KEY(id),
                  FOREIGN KEY(character_id) REFERENCES CHARACTER(id),
                  FOREIGN KEY(video_id) REFERENCES VIDEO(id)
                  )"""
        cursor.execute(sql)

        sql = """ CREATE TABLE IF NOT EXISTS CHARACTER
                  (
                  id INT,
                  name VARCHAR(255),
                  show_id INT,
                  actor_id INT,
                  PRIMARY KEY(id),
                  FOREIGN KEY (show_id) REFERENCES SHOW(id),
                  FOREIGN KEY (actor_id) REFERENCES ACTOR(id)
                  )"""
        cursor.execute(sql)

        sql = """ CREATE TABLE IF NOT EXISTS ACTOR
                  (
                  id INT,
                  name VARCHAR(255),
                  photo_url VARCHAR(255),
                  PRIMARY KEY(id)
                  )"""
        cursor.execute(sql)

        sql = """CREATE TABLE IF NOT EXISTS REQUEST
                  (
                  id INT,
                  request LONGTEXT,
                  status VARCHAR(255),
                  PRIMARY KEY(id)
                  )
                  """
        cursor.execute(sql)

    def insertVideos(self, cursor,id, season_id, episode_no,episode_url,duration):
        sql = "INSERT INTO VIDEOS VALUES(%d, %d, %d, '%s', %d)" % (id,season_id, episode_no,episode_url,duration)
        cursor.execute(sql)

    def insertShows(self,cursor, id, name, video_url):
        sql = "INSERT INTO SHOWS VALUES(%d, '%s', '%s')" %(id, name, video_url)
        cursor.execute(sql)

    def insertDialogues(self, cursor, id, character_id, video_id, raw_text,keyword, start_time, end_time, url):
        sql = "INSERT INTO DIALOGUES VALUES(%d, %d, %d, '%s', '%s', %d, %d, '%s')" % (id, character_id, video_id, raw_text, keyword, start_time, end_time, url)
        cursor.execute(sql)

    def insertCharacters(self, cursor, id, name, show_id, actor_id):
        sql = "INSERT INTO CHARACTERS VALUES(%d, '%s', %d, %d)" % (id, name, show_id, actor_id)
        cursor.execute(sql)

    def insertActors(self, cursor, id, actor_name, photo_url):
        sql = "INSERT INTO ACTORS VALUES(%d, '%s', '%s')" % (id, actor_name, photo_url)
        cursor.execute(sql)


    def insertRequests(self,cursor, id, request, status):
        sql = "INSERT INTO REQUESTS VALUES(%d,'%s', '%s')" % (id, request, status)
        cursor.execute(sql)


def main():
    obj = DataManipulation()
    connObj = obj.connectToDatabase()
    cursor = connObj.cursor()
    obj.createTables()
    connObj.commit()
    cursor.close()

if __name__ == "__main__":
    main()
