from bisect import bisect_left
from parsers import SRTParser

class Subtitle(object):
  """
  Provides high level access to subtitle data, such as searching by
  keyword, or finding a piece of subtitle at a specific point in time.
  """

  def __init__(self, filename):
    self.indexer = TextIndexer()
    self.pieces = []
    self.end_times = []
    for piece in SRTParser.parse(filename):
      self.indexer.add(piece['keywords'], piece)
      self.pieces.append(piece)
      self.end_times.append(piece['end'])

  def at(self, time):
    """
    This does a binary search to find the piece at a specific time.
    """
    index = bisect_left(self.end_times, time)
    piece = self.pieces[index]
    if piece['start'] <= time <= piece['end']:
      return piece

  def search(self, keyword):
    return self.indexer.find(keyword)

  def get_pieces(self):
    return self.pieces



class TextIndexer(object):
  """
  Simple text indexer.
  """

  def __init__(self):
    self.index = {}

  def add(self, keywords, entry):
    for keyword in set(keywords.split()):
      keyword = keyword.lower()
      if keyword not in self.index:
        self.index[keyword] = []
      self.index[keyword].append(entry)

  def find(self, keyword):
    return self.index.get(keyword.lower(), [])



#### FOR TESTING ####
## python subtitles.py <filename> <keyword>
## python subtitles.py homeland.srt obama

if __name__ == '__main__':
  import sys
  filename = sys.argv[1]
  keyword = sys.argv[2]
  sub = Subtitle(filename)
  # print sub.at(SRTParser.parse_time('00:00:11'))
  for x in sub.search(keyword):
    print
    print x

