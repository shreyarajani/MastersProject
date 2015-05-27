import subprocess
from moviepy.editor import *
import util

class Operations(object):
  """
  Provides easy-to-use methods to do operations on videos
  such as cutting, merging, etc.
  """

  def __init__(self, filename):
    self.video = VideoFileClip(filename)
    self.ranges = []

  def slice(self, rng):
    self.ranges.append(rng)
    return self

  def merge_slices(self, slices):
    """
    If any slices are adjacent, they will be merged into one slice.
    """
    if not slices:
      return []

    merged = [slices.pop(0)]
    while slices:
      curr = slices.pop(0)
      last = merged[-1]
      if util.is_overlapping(curr, last):
        last['end'] = curr['end']
      else:
        merged.append(curr)
    return merged

  def has_slices(self):
    return len(self.ranges) > 0

  def save(self, filename):
    clips = []
    for rng in self.merge_slices(self.ranges):
      clips.append(self.video.subclip(rng['start'] / 1000, rng['end'] / 1000))
    final = concatenate_videoclips(clips)
    final.write_videofile(filename)
    self.result_file = filename
    return self

  def open(self):
    if self.result_file:
      subprocess.call(['xdg-open', self.result_file])
    else:
      print 'You have to save before you can open the file.'


class MultiFileOperations(object):

  def __init__(self):
    self.ranges = []

  def slice(self, filename, start, end):
    self.ranges.append({'file': filename, 'start': start, 'end': end})
    return self

  def merge_slices(self, slices):
    if not slices:
      return []

    merged = [slices.pop(0)]
    while slices:
      curr = slices.pop(0)
      last = merged[-1]
      if curr['file'] == last['file'] and util.is_overlapping(curr, last):
        last['end'] = curr['end']
      else:
        merged.append(curr)
    return merged

  def save(self, filename):
    clips = []
    curr_file = None
    video = None
    for rng in self.merge_slices(self.ranges):
      if rng['file'] != curr_file:
        curr_file = rng['file']
        video = VideoFileClip(rng['file'])
      print 'Adding clip from %s: %d --> %d' % (rng['file'], rng['start'], rng['end'])
      clip = video.subclip(rng['start'] / 1000, rng['end'] / 1000)
      clips.append(clip)
    print
    final = concatenate_videoclips(clips, method="compose")
    final.fps = video.fps
    final.write_videofile(filename)
    return self



#### FOR TESTING ####
## python videos.py <movie_file> <start_time> <end_time>
## python videos.py homeland.mp4 00:08:38,000 00:08:45,000

def multi_op_test():
  MultiFileOperations()\
  .slice('/Users/mouad/Dropbox/VideoInventory/Friends/S01/01 The One where Monica gets a Roommate.mkv', 131131.0, 135090.0)\
  .slice('/Users/mouad/Dropbox/VideoInventory/Friends/S01/03 The One with the Thumb.mkv', 779411.0, 781936.0)\
  .slice('/Users/mouad/Dropbox/VideoInventory/Friends/S01/07 The One with the Blackout.mkv', 407073.0, 409405.0)\
  .save('result_woohoo.mp4')

if __name__ == '__main__':
  # multi_op_test()
  import sys, os
  from parsers import SRTParser

  filename = sys.argv[1]
  basename, ext = os.path.splitext(filename)
  slice = {
    'start': SRTParser.parse_time(sys.argv[2]),
    'end': SRTParser.parse_time(sys.argv[3]),
  }
  Operations(filename).slice(slice).save(basename + '.test.mp4').open()
