import sqlite3
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_cursor():
  print os.path.join(ROOT_DIR, 'ThruLineDjango/db.sqlite3')
  conn = sqlite3.connect(os.path.join(ROOT_DIR, 'ThruLineDjango/db.sqlite3'))
  conn.row_factory = sqlite3.Row
  return conn.cursor()

def update_episode_urls():
  c = get_cursor()
  c.execute('SELECT * FROM ThruLine_episode')
  episodes = c.fetchall()
  for ep in episodes:
    c.execute(
      'UPDATE ThruLine_episode SET episode_url=? WHERE id=?',
      (transform_episode_url(ep['episode_url']), ep['id']),
    )
  c.connection.commit()
  c.close()

def transform_episode_url(url):
  return url.replace('~/Dropbox/VideoInventory/', '/Volumes/Seagate Hard Disk/TV Series/')


if __name__ == '__main__':
  update_episode_urls()
