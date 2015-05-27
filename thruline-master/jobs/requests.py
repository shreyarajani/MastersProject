import json
import sqlite3
import os
from query import DataFinder
from videos import MultiFileOperations

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVE_FILES_PATH = '/Library/WebServer/Documents/'

def get_cursor():
  conn = sqlite3.connect(os.path.join(ROOT_DIR, 'ThruLineDjango/db.sqlite3'))
  conn.row_factory = sqlite3.Row
  return conn.cursor()

def get_pending_requests():
  c = get_cursor()
  c.execute('SELECT * FROM ThruLine_request WHERE status="pending"')
  requests = c.fetchall()
  c.close()
  return requests

def update_request_status(request, status, video):
  c = get_cursor()
  id = request['id']
  c.execute('UPDATE ThruLine_request SET status=?, result_path=? WHERE id=?', (status, video, id))
  c.close()
  c.connection.commit()

def get_matching_dialogues(keyword, episodes):
  finderObj = DataFinder()
  return finderObj.getDialogueAndTimeStamps(keyword, episodes)

def get_episodes(episode_ids):
  c = get_cursor()
  c.execute(
    'SELECT * FROM ThruLine_episode WHERE id IN (%s)' % ','.join('?' * len(episode_ids)),
    episode_ids,
  )
  episodes = c.fetchall()
  c.close()
  return episodes

def cut_clips(dialogues, result_file):
  op = MultiFileOperations()
  url = None
  for d in dialogues:
    if url != d['episode_url']:
      url = d['episode_url']
    op.slice(d['episode_url'], d['start_time'], d['end_time'])
  op.save(result_file)

def process_request(request):
  data = json.loads(request['request'])
  episode_ids = data['episodes']
  print 'Processing request #%d' % request['id']
  print 'Keyword: "%s"' % data['keyword']
  print 'Episodes: %s' % str(episode_ids)
  print

  episodes = get_episodes(episode_ids)

  matching_dialogues = get_matching_dialogues(data['keyword'], episode_ids)
  if not matching_dialogues:
    print 'No results were found for this request'
    update_request_status(request, 'no results', '')
    return

  result_path = os.path.join(SAVE_FILES_PATH, 'jobs/requests/%d.mp4' % request['id'])
  cut_clips(matching_dialogues, result_path)

  update_request_status(request, 'complete', result_path)

def main():
  requests = get_pending_requests()
  for r in requests:
    process_request(r)
    print '-' * 20


if __name__ == '__main__':
  main()

