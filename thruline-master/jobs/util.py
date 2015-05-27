
def is_overlapping(seg1, seg2):
  """
  Check whether 2 segments overlap or not
  """
  return not (seg1['end'] < seg2['start'] or seg2['end'] < seg1['start'])