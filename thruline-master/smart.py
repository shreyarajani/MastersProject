from videos import Operations
import util

# The min distance in milliseconds. This is distance we will
# use to decide whether 2 subtitles are far apart or not.
MIN_DISTANCE_TO_SPLIT = 500

def distance(sub1, sub2):
  """
  Calculate the distance between 2 subtitles.
  """
  return min(abs(sub1['end_time'] - sub2['start_time']), abs(sub2['end_time'] - sub1['start_time']))


class DialogueAdjuster(object):

  def __init__(self, all_dialogues):
    self.all_dialogues = all_dialogues

  def adjust(self, matching_dialogues):
    for dial in matching_dialogues:
      self.adjust_dialogue(dial)

  def adjust_dialogue(self, dial):
    """
    Get the optimal segment for the given subtitle.
    """
    beginning = self.find_dialogue_edge(dial, -1)
    ending = self.find_dialogue_edge(dial, 1)
    dial['start_time'] = beginning['start_time']
    dial['end_time'] = ending['end_time']

  def find_index_of_dialogue(self, dial, dialogues):
    for i, d in enumerate(dialogues):
      if d['id'] == dial['id']:
        return i

  def find_dialogue_edge(self, dial, dir):
    """
    Find the subtitle where the dialog starts or ends.
    `dir` can either be +1 or -1 to determine which direction we are looking for.
    """
    index = self.find_index_of_dialogue(dial, self.all_dialogues)
    while index > 0 and index < len(self.all_dialogues) - 1:
      curr = self.all_dialogues[index]
      next = self.all_dialogues[index + dir]
      if distance(curr, next) >= MIN_DISTANCE_TO_SPLIT:
        return self.get_fade(curr, next)
      index += dir
    return self.all_dialogues[index]

  def get_fade(self, curr_sub, next_sub):
    fade_before = fade_after = 0
    fade_after = 0
    if curr_sub['start_time'] < next_sub['start_time']:
      fade_after = min(next_sub['start_time'] - curr_sub['end_time'], MIN_DISTANCE_TO_SPLIT)
    else:
      fade_before = min(curr_sub['start_time'] - next_sub['end_time'], MIN_DISTANCE_TO_SPLIT)
    return {
      'start_time': curr_sub['start_time'] - fade_before / 3,
      'end_time': curr_sub['end_time'] + fade_after / 3,
    }


class CutterBySubtitle(object):

  is_mute = True

  def __init__(self, video_file, all_subtitles, requested_subtitles):
    self.video_file = video_file
    self.all_subtitles = all_subtitles
    self.requested_subtitles = requested_subtitles

  def mute(self, is_mute=True):
    self.is_mute = is_mute
    return self

  def cut(self, operations, open_video=False):
    segments = []
    for sub in self.requested_subtitles:
      self.print_sub(sub)
      op.slice(self.get_segment_for_subtitle(sub))

    self.maybe_print('-' * 25)
    if op.has_slices():
      op.save(result_file)
      if open_video:
        op.open()
      return True
    else:
      return False

  def cut_save(self, result_file, open_video=False):
    segments = []
    op = Operations(self.video_file)
    for sub in self.requested_subtitles:
      self.print_sub(sub)
      op.slice(self.get_segment_for_subtitle(sub))

    self.maybe_print('-' * 25)
    if op.has_slices():
      op.save(result_file)
      if open_video:
        op.open()
      return True
    else:
      return False

  def get_segment_for_subtitle(self, sub):
    """
    Get the optimal segment for the given subtitle.
    """
    beginning = self.find_dialog_edge(sub, -1)
    ending = self.find_dialog_edge(sub, 1)
    return {
      'start': beginning['start'],
      'end': ending['end'],
    }

  def find_dialog_edge(self, sub, dir):
    """
    Find the subtitle where the dialog starts or ends.
    `dir` can either be +1 or -1 to determine which direction we are looking for.
    """
    index = self.all_subtitles.index(sub)
    while index > 0 and index < len(self.all_subtitles) - 1:
      curr = self.all_subtitles[index]
      next = self.all_subtitles[index + dir]
      if distance(curr, next) >= MIN_DISTANCE_TO_SPLIT:
        return self.get_fade(curr, next)
      index += dir
    return self.all_subtitles[index]

  def get_fade(self, curr_sub, next_sub):
    fade_before = fade_after = 0
    fade_after = 0
    if curr_sub['start'] < next_sub['start']:
      fade_after = min(next_sub['start'] - curr_sub['end'], MIN_DISTANCE_TO_SPLIT)
    else:
      fade_before = min(curr_sub['start'] - next_sub['end'], MIN_DISTANCE_TO_SPLIT)
    return {
      'start': curr_sub['start'] - fade_before / 3,
      'end': curr_sub['end'] + fade_after / 3,
    }

  def print_sub(self, sub):
    self.maybe_print('[%(start)d --> %(end)d]\n%(raw_text)s' % sub)
    self.maybe_print()

  def maybe_print(self, msg=''):
    if self.is_mute:
      return
    print msg

### FOR TESTING ###
# python smart.py <video_file> <keyword>
# python smart.py friends101.avi love
#
# There must be a .srt subtitle file with the same name as the video

if __name__ == '__main__':
  import os, sys, subprocess
  from subtitles import Subtitle

  video_file = sys.argv[1]
  basename, ext = os.path.splitext(video_file)
  srt_file = basename + '.srt'
  keyword = sys.argv[2]

  if not os.path.isfile(video_file):
    print 'The file %s does not exist!' % video_file
    exit(-1)

  if not os.path.isfile(srt_file):
    print 'There is no subtitle named %s' % srt_file
    exit(-1)

  sub = Subtitle(srt_file)
  cutter = CutterBySubtitle(
    video_file,
    sub.get_pieces(),
    sub.search(keyword),
  ).mute(False)

  output_name = '%s_%s_smart.mp4' % (basename, keyword)
  if cutter.cut_save(output_name, open_video=True):
    pass
  else:
    print 'Sorry, no matches were found for "%s"' % keyword
