from django.db import models
import json

class Season(models.Model):
    name = models.CharField(max_length=10)  # S1, S2....


class Episode(models.Model):
    name = models.CharField(max_length=10)  # E1, E2 ...
    season = models.ForeignKey(Season)  # 1, 2, 3...
    episode_url = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Request(models.Model):
    request = models.TextField()  # Json
    status = models.CharField(max_length=20)  # Pending, Processing, Completed
    result_path = models.CharField(max_length=200)

    def get_data(self):
        return json.loads(self.request)

    def get_keyword(self):
        return self.get_data()['keyword']

    def get_episodes(self):
        return self.get_data()['episodes']

    def __unicode__(self):
        return self.request

class Dialogue(models.Model):
    episode_id = models.ForeignKey(Episode)
    raw_text = models.TextField()
    start_time = models.TextField()
    end_time = models.TextField()

    def __unicode__(self):
        return self.raw_text