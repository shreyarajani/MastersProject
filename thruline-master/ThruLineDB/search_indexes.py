__author__ = 'keertisekharsahoo'
from django.db import models
import haystack
from haystack import indexes
from ThruLine.models import Video
from ThruLine.models import Dialogue
from ThruLine.models import Character
from ThruLine.models import Show
from ThruLine.models import Actor
from ThruLine.models import Request


class DialogueIndex(indexes.SearchIndex, indexes.Indexable):
    raw_text = indexes.TextField(model_attr='raw_text')
    keyword = indexes.TextField(model_attr='keyword')

    def get_model(self):
        return Dialogue

    def index_queryset(self, using=None):
        return self.get_model().objects.all()



class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    episode_url = indexes.CharField(model_attr='episode_url')

    def get_model(self):
        return Video

    def index_query_set(self, using=None):
        return self.get_model().objects.all()


class CharacterIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Character

    def index_query_set(self, using=None):
        return self.get_model().objects.all()


class ShowIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')
    video_url = indexes.CharField(model_attr='video_url')

    def get_model(self):
        return Show

    def index_query_set(self, using = None):
        return self.get_model().objects.all()

class ActorIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Actor

    def index_query_set(self, using = None):
        return self.get_model().objects.all()


class RequestIndex(indexes.SearchIndex, indexes.Indexable):
    request = indexes.TextField(model_attr='request')

    def get_model(self):
        return Request

    def index_query_set(self, using= None):
        return self.get_model().objects.all()







