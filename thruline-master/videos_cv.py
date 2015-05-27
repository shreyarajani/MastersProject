import cv2


class Video(object):

  def __init__(self, filename):
    self.capture = cv2.VideoCapture(filename)

  def get_info(self):
    return {
      'width': int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
      'height': int(self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)),
      'count': self.capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT),
      'fps': self.capture.get(cv2.cv.CV_CAP_PROP_FPS),
      'fourcc': self.capture.get(cv2.cv.CV_CAP_PROP_FOURCC),
    }

  def get_fps(self):
    """
    Frames per second.
    """
    return self.capture.get(cv2.cv.CV_CAP_PROP_FPS)

  def _calc_frame_index(self, time):
    """
    Caculate frame index for a specific time in ms.
    """
    fps = self.get_fps()
    frames_per_ms = 1000.0 / fps
    return int(time // frames_per_ms)

  def get_frame_at(self, time):
    """
    Get the frame at a specific time (in milliseconds).
    """
    self.capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, self._calc_frame_index(time))
    ret, frame = self.capture.read()
    if ret:
      return frame

  def get_frame_range(self, start, end):
    """
    Returns a range of frames for the specified start and end time.
    """
    start_index = self._calc_frame_index(start)
    end_index = self._calc_frame_index(end)
    for i in range(start_index, end_index + 1):
      yield self.get_frame_at(i)


class Operations(object):
  """
  Provides easy-to-use methods to do operations on videos
  such as cutting, merging, etc.
  """

  def __init__(self, video):
    self.video = video
    self.ranges = []

  def _create_writer(self, filename):
    info = self.video.get_info()
    fourcc = cv2.cv.CV_FOURCC(*'MJPG')
    size = (info['width'], info['height'])
    return cv2.VideoWriter(filename, fourcc, info['fps'], size)

  def cut(self, start, end):
    self.ranges.append((start, end))
    return self

  def save(self, filename):
    writer = self._create_writer(filename)
    for (start, end) in self.ranges:
      for frame in self.video.get_frame_range(start, end):
        writer.write(frame)
    writer.release()



#### FOR TESTING ####
## python videos_cv.py <movie_file> <start_time> <end_time>
## python videos_cv.py homeland.mp4 00:08:38,000 00:08:45,000

if __name__ == '__main__':
  import sys
  from parsers import SRTParser

  filename = sys.argv[1]
  start = SRTParser.parse_time(sys.argv[2])
  end = SRTParser.parse_time(sys.argv[3])
  video = Video(filename)
  Operations(video).cut(start, end).save('test.mp4')
