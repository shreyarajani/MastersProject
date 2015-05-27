## USAGE ##
# python convert.py <video_file>
# python convert.py friends101.avi
#
# Converts any video file to mp4.

import sys, os
from moviepy.editor import *

video_file = sys.argv[1]
basename, ext = os.path.splitext(video_file)
if ext == '.mp4':
  exit(0)

video = VideoFileClip(video_file)
video.write_videofile(basename + '.mp4')