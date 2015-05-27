import os
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB


class VoiceDetector(object):
  """
  A class to extract voice activity information from a video file. It
  uses VoiceID under the hood, and provides caching so that we don't 
  process the same video twice.
  """

  voiceid = None
  ready = False
  segments = None

  def __init__(self, filename=None, db_name='data/gmm_db'):
    db = GMMVoiceDB(db_name)
    basefile, ext = os.path.splitext(filename)
    json_file = basefile + '.json'
    if os.path.isfile(json_file):
      self.voiceid = Voiceid.from_json_file(db, json_file)
      self.ready = True
    elif filename:
      self.voiceid = Voiceid(db, filename, single=True)

  def process(self):
    """
    Do the actual processing to extract the voice activity info.
    """
    if self.ready:
      return self

    self.voiceid._to_wav()
    self.voiceid.diarization()
    self.voiceid._extract_clusters()
    self.voiceid.write_json()
    self.ready = True
    return self

  def get_segments(self):
    """
    Gets the list of segments of voice activity. Each segment is a dict:
    {'start': int, 'end': int}
    """
    if not self.segments:
      self.process()
      for key, cluster in self.voiceid.get_clusters().iteritems():
        self.segments = [self.make_segment(seg) for seg in cluster.get_segments()]
    return self.segments

  def make_segment(self, seg):
    return {
      'start': seg.get_start() * 10,
      'end': seg.get_end() * 10,
    }

  def print_all_segments(self):
    self.print_segments(self.get_segments())

  def print_segments_for_range(self, start, end):
    self.print_segments(self.get_segments_for_range(start, end))

  def print_segments(self, segments):
    for segment in segments:
      print "%(start)d --> %(end)d" % segment

  def cleanup(self):
    # TODO: remove all the generated files
    return self


#### FOR TESTING ####
## python vad2.py <movie_file>
## python vad2.py friends101.mp4

if __name__ == '__main__':
  import sys
  args = sys.argv[1:]
  filename = args[0]
  VoiceDetector(filename).print_all_segments()

