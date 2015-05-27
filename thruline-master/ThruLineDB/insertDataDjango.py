__author__ = 'keertisekharsahoo'
import sys
from django.db import models

class Video(models.Model):
    season_id = models.IntegerField()
    episode_no = models.IntegerField()
    episode_url = models.CharField(max_length=90)
    duration = models.IntegerField()
    def __unicode__(self):
        return self.name


class Show(models.Model):
    name = models.CharField(max_length=30)
    video_url = models.CharField(max_length=90)
    def __unicode__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=30)
    photo_url = models.CharField(max_length=90)
    def __unicode__(self):
        return self.name

class Request(models.Model):
    request = models.TextField()
    status = models.CharField(max_length=20)
    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=30)
    show_id = models.ForeignKey(Show)
    actor_id = models.ForeignKey(Actor)
    def __unicode__(self):
        return self.name

class Dialogue(models.Model):
    character_id = models.ForeignKey(Character)
    video_id = models.ForeignKey(Video)
    raw_text = models.TextField(max_length=100)
    keyword = models.TextField(max_length=30)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    url = models.CharField(max_length=90)
    def __unicode__(self):
        return self.name

def insertVideos(id,season_id, episode_no,episode_url,duration):
    v = Video(id= id,season_id = season_id, episode_no = episode_no,episode_url = episode_url,duration = duration)
    v.save()

def insertShows(id, show_name, video_url):
    s = Show(id = id, show_name = show_name, video_url = video_url)
    s.save()

def insertDialogues(id, raw_text,keyword, start_time, end_time):
    d = Dialogue(id = id, raw_text = raw_text,keyword = keyword, start_time = start_time, end_time = end_time)
    d.save()

def insertCharacters(id, character_name, show_id, actor_id):
    c = Character(id = id, character_name = character_name, show_id = show_id, actor_id = actor_id)
    c.save()

def insertActors(id, actor_name, photo_url):
    a = Actor(id = id, actor_name = actor_name, photo_url = photo_url)
    a.save()

def insertRequests(id, keyword, episode, season, characters):
    r = Request(id = id, keyword = keyword, episode = episode, season = season, characters = characters)
    r.save()



