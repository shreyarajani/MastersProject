from videos import Operations
import util


class CutterByVoice(object):

  is_mute = True

  def __init__(self, video_file, subtitles, voice_segments):
  	self.video_file = video_file
  	self.subtitles = subtitles
  	self.voice_segments = voice_segments

  def mute(self, is_mute=True):
    self.is_mute = is_mute
    return self

  def cut(self, result_file, open_video=False):
    segments = []
    op = Operations(self.video_file)
    for sub in self.subtitles:
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
    segments = []
    for seg in self.voice_segments:
      if util.is_overlapping(sub, seg):
        segments.append(seg)
      elif segments:
        break

    if not segments:
      return sub
    return {
      'start': segments[0]['start'],
      'end': segments[-1]['end'],
    }

  def print_sub(self, sub):
    self.maybe_print('[%(start)d --> %(end)d]\n%(raw_text)s' % sub)
    self.maybe_print()

  def maybe_print(self, msg=''):
    if self.is_mute:
      return
    print msg

### FOR TESTING ###
# python voice.py <video_file> <keyword>
# python voice.py friends101.avi love
#
# There must be a .srt subtitle file with the same name as the video

if __name__ == '__main__':
  import os, sys, subprocess
  from subtitles import Subtitle
  from vad2 import VoiceDetector

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

  cutter = CutterByVoice(
    video_file,
    Subtitle(srt_file).search(keyword),
    VoiceDetector(video_file).get_segments(),
  ).mute(False)

  output_name = '%s_%s_voice.mp4' % (basename, keyword)
  if cutter.cut(output_name, open_video=True):
    pass
  else:
    print 'Sorry, no matches were found for "%s"' % keyword
