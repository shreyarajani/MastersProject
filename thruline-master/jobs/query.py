__author__ = 'keertisekharsahoo'

import sqlite3
import os
import sys
from smart import DialogueAdjuster

def parse_time(str):
  hours, minutes, seconds = str.split(':')
  seconds = seconds.replace(',', '.')
  return 3600000 * int(hours) + 60000 * int(minutes) + 1000 * float(seconds)

class DataFinder():

    def getConnection(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        conn = sqlite3.connect(os.path.join(dir, 'ThruLineDjango/db.sqlite3'))
        conn.text_factory = str
        conn.row_factory = sqlite3.Row
        return conn
    #Regular full-text search of a phrase/keyword and list of episode ids
    def getDialogueAndTimeStamps(self, keyword, episodes):
        cursor = self.getConnection().cursor()
        outputList = []
        ep_len = len(episodes)
        cursor.execute('SELECT * FROM ThruLine_episode LIMIT 10')
        print cursor.fetchall()
        cursor.execute(
            "SELECT dialogue_id FROM indexed_dialogue WHERE indexed_dialogue MATCH ? AND episode_id IN (%s)" % ','.join('?'*ep_len),
            [keyword] + episodes,
        )
        dialogues = cursor.fetchall()

        cursor.execute(
            """
            SELECT d.id AS id, episode_id, start_time, end_time, name AS episode_name, episode_url
            FROM ThruLine_dialogue AS d JOIN ThruLine_episode AS e ON d.episode_id=e.id
            WHERE d.id IN (%s)
            ORDER BY episode_id
            """ % ','.join('?' * len(dialogues)),
            [d['dialogue_id'] for d in dialogues],
        )
        results = []
        for d in cursor.fetchall():
            results.append(self.transformDialogue(d))
        self.adjustDialogues(results)
        return results

    def getEpisodeDialogues(self, episode_id):
        cursor = self.getConnection().cursor()
        cursor.execute('SELECT * FROM ThruLine_dialogue WHERE episode_id=?', (episode_id,))
        dialogues = cursor.fetchall()
        cursor.close()
        return [self.transformDialogue(d) for d in dialogues]

    def adjustDialogues(self, dialogues):
        adjuster = None
        curr_episode_id = None
        curr_ep_dialogues = []
        for dial in dialogues:
            if dial['episode_id'] != curr_episode_id:
                if adjuster:
                    adjuster.adjust(curr_ep_dialogues)
                curr_episode_id = dial['episode_id']
                curr_ep_dialogues = []
                adjuster = DialogueAdjuster(self.getEpisodeDialogues(curr_episode_id))
            curr_ep_dialogues.append(dial)
        if curr_ep_dialogues:
            adjuster.adjust(curr_ep_dialogues)

    def transformDialogue(self, dial):
        new_dial = {
            'id': dial['id'],
            'start_time': parse_time(dial['start_time']),
            'end_time': parse_time(dial['end_time']),
        }
        try:
            new_dial['episode_id'] = dial['episode_id']
        except (KeyError, IndexError):
            pass
        try:
            new_dial['episode_name'] = dial['episode_name']
        except (KeyError, IndexError):
            pass
        try:
            new_dial['episode_url'] = os.path.expanduser(dial['episode_url'])
        except (KeyError, IndexError):
            pass
        return new_dial

    def getDialogueData(self,keyword, episodeIdList):
        dialogueIdList = []
        outputList = []
        cursor = self.getConnection().cursor()
        for episodeID in episodeIdList:
            cursor.execute("SELECT dialogue_id FROM indexed_dialogue WHERE raw_text MATCH ? AND episode_id = ? ",(keyword, episodeID))
            data = cursor.fetchall()
            dialogueIdList.append(data)
        for dialogue_id in dialogueIdList:
            for i in range(0,len(dialogue_id)):
                cursor.execute("SELECT raw_text, start_time, end_time FROM ThruLine_dialogue WHERE id = %d" % (dialogue_id[i][0]))
                dat = cursor.fetchall()
                outputList.append(dat)
        return outputList

    #Finds the occurrences of the phrase with no intervening terms between words
    def getExactDialogueAndTimeStamps(self, keyword, episodeIdList):
        dialogueIdList = []
        outputList = []
        cursor = self.getConnection().cursor()
        words = keyword.split(" ")
        noOfWords = len(words)
        phrase = ''
        for i in range(0,noOfWords):
            if not i==noOfWords-1:
                phrase += words[i] + ' ' + 'NEAR/0 '
            else:
                phrase += words[i]
        for episodeID in episodeIdList:
            cursor.execute("SELECT dialogue_id FROM indexed_dialogue WHERE raw_text MATCH ? AND episode_id = ? ",(phrase, episodeID))
            data = cursor.fetchall()
            dialogueIdList.append(data)
        for dialogue_id in dialogueIdList:
            for i in range(0,len(dialogue_id)):
                cursor.execute("SELECT raw_text, start_time, end_time FROM ThruLine_dialogue WHERE id = %d" % (dialogue_id[i][0]))
                dat = cursor.fetchall()
                outputList.append(dat)
        return outputList

    #Finds the occurrences of the phrase/keyword with specified no of intervening terms between words
    def getDialogueAndTimeStampsWithDefinedGap(self, keyword, allowedNoOfInterveningTerms, episodeIdList):
        dialogueIdList = []
        outputList = []
        cursor = self.getConnection().cursor()
        words = keyword.split(" ")
        noOfWords = len(words)
        nearQuery = 'NEAR/' + str(allowedNoOfInterveningTerms)
        phrase = ''
        for i in range(0,noOfWords):
            if not i==noOfWords-1:
                phrase += words[i] + ' ' + nearQuery + ' '
            else:
                phrase += words[i]
        for episodeID in episodeIdList:
            cursor.execute("SELECT dialogue_id FROM indexed_dialogue WHERE raw_text MATCH ? AND episode_id = ? ",(phrase, episodeID))
            data = cursor.fetchall()
            dialogueIdList.append(data)
        for dialogue_id in dialogueIdList:
            for i in range(0,len(dialogue_id)):
                cursor.execute("SELECT raw_text, start_time, end_time FROM ThruLine_dialogue WHERE id = %d" % (dialogue_id[i][0]))
                dat = cursor.fetchall()
                outputList.append(dat)
        return outputList


def main():
    finderObj = DataFinder()
    # episodeIdList = [174, 120, 135, 178,34,45,213,39,40,29,12,13,52,56,78,100,90,45,234,56,78,90,11,221,112,220,89,56,32,31,1,2,3,5,6]
    # data = finderObj.getDialogueAndTimeStamps('How you doing', episodeIdList)
    # data = finderObj.getEpisodeDialogues(120)
    # data = finderObj.getDialogueData('mom AND dad', episodeIdList)
    # data = finderObj.getExactDialogueAndTimeStamps('how you doing', episodeIdList)
    # data = finderObj.getDialogueAndTimeStampsWithDefinedGap('how you doing', 3, episodeIdList)

if __name__ == "__main__":
    main()

