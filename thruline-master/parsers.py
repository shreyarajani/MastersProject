import re

class AbstractParser(object):

  @classmethod
  def parse(cls, filename):
    with open(filename) as f:
      while True:
        piece = cls._parse_piece(f)
        if not piece:
          break
        yield piece

  @staticmethod
  def _clean_text(text):
    no_html = re.sub('<[^<]+?>', ' ', text)
    return re.sub('[^A-Za-z0-9]+', ' ', no_html).strip()


class SRTParser(AbstractParser):
  """
  Utilities to help parse .srt files
  """

  @classmethod
  def _parse_piece(cls, file):
    """
    The format of each piece looks like:

    7
    00:02:02,513 --> 00:02:05,688
    Scientists say maybe it
    is two billion or more.
    """
    number = file.readline().strip()
    # Check if we reached the end of the file
    if number == '':
      return None
    (start, end) = cls.parse_time_range(file.readline().strip())
    text = '\n'.join(cls._read_block(file))
    return {
      'start': start,
      'end': end,
      'raw_text': text,
      'keywords': cls._clean_text(text),
    }

  @classmethod
  def parse_time_range(cls, range):
    (start, end) = range.split('-->')
    return (
      cls.parse_time(start.strip()),
      cls.parse_time(end.lstrip().split(' ')[0]),
    )

  @staticmethod
  def parse_time(str):
    hours, minutes, seconds = str.split(':')
    seconds = seconds.replace(',', '.')
    return 3600000 * int(hours) + 60000 * int(minutes) + 1000 * float(seconds)

  @staticmethod
  def _read_block(file):
    lines = []
    while True:
      line = file.readline().strip()
      if not line:
        break
      lines.append(line)
    return lines


# This isn't tested yet
class SUBParser(AbstractParser):
  """
  Utilities to help parse .sub files
  """

  @classmethod
  def _parse_piece(cls, f):
    """
    The format of each piece looks like:
    {544}{601}Rach, he just saw us.
    """
    line = f.readline().strip()
    start, end, text = re.search('\{(.+)\}\{(.+)\}(.+)', line).groups()
    return {
      'start': int(start),
      'end': int(end),
      'raw_text': text,
      'keywords': cls._clean_text(text),
    }

