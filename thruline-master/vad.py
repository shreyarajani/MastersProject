import os
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB

class VoiceDetector(object):

  voiceid = None
  ready = False

  def __init__(self, filename, db_name='data/gmm_db'):
    db = GMMVoiceDB(db_name)
    self.voiceid = Voiceid(db, filename)

  def process(self):
    if self.ready:
      return self

    # This is the slow step:
    self.voiceid.extract_speakers()
    self.ready = True
    return self

  def get_segments(self):
    if not self.ready:
      raise 'You have to call process() first'

    segments = []
    for key, cluster in self.voiceid.get_clusters().iteritems():
      segments.extend(self.make_segment(seg) for seg in cluster.get_segments())
    return segments

  def make_segment(self, seg):
    return {
      'start': seg.get_start() * 10,
      'end': seg.get_end() * 10,
    }

  def print_segments(self):
    if not self.ready:
      raise 'You have to call process() first'

    for segment in self.get_segments():
      print "%(start)d --> %(end)d" % segment


#### FOR TESTING ####
## python vad.py <movie_file>
## python vad.py friends101.mp4

if __name__ == '__main__':
  import sys
  args = sys.argv[1:]
  filename = args[0]
  VoiceDetector(filename).process().print_segments()

