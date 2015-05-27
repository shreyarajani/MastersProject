## USAGE ##
# python main.py <video_file> <keyword>
# python main.py friends101.avi love
#
# There must be a subtitle file with the same name as the video
# having the extension .srt

import os, sys, subprocess
from subtitles import Subtitle
from videos import Operations

video_file = sys.argv[1]
basename, ext = os.path.splitext(video_file)
keyword = sys.argv[2]

if not os.path.isfile(video_file):
  print 'The file %s does not exist!' % video_file
  exit(-1)

op = Operations(video_file)
sub = Subtitle(basename + '.srt')
for sub_piece in sub.search(keyword):
  print '[%(start)d --> %(end)d]\n%(raw_text)s' % sub_piece
  print
  op.slice(sub_piece)

if op.has_slices():
  print '-' * 25
  output_name = basename + '_' + keyword + '_main.mp4'
  op.save(output_name).open()
else:
  print 'Sorry, no matches were found for "%s"' % keyword
