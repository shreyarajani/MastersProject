__author__ = 'keertisekharsahoo'
import os
import sys
import subprocess
import re
import json
videoDictionary = {}

class VideoFilePreprocessor():

    def videoFilePreprocessor(self, base):

        showNames = os.listdir(base)
        for show in showNames:
            if(os.path.isdir(base + "/" + show)):
                seasonsList = os.listdir(base + "/" + show)
                for season in seasonsList:
                    if(os.path.isdir(base +"/"+ show+"/"+season)):
                        episodesList = os.listdir(base +"/"+ show+"/"+season)
                        for episode in episodesList:
                            if ((episode.endswith('.mkv'))):
                                showID = 1 # for friends
                                episodeURL = base +"/"+ show+"/"+season + "/" +episode
                                episodeNo = episode.split(' ')[0]
                                list = [showID, season, episodeNo, episodeURL, self.getDuration(episodeURL)]
                                videoDictionary[episode] = list;

    def getDuration(self,episodeURL):
        try:
            process = subprocess.Popen(['/usr/bin/ffmpeg',  '-i', episodeURL], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = process.communicate()
            matches = re.search(r"Duration:\s{1}(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", stdout, re.DOTALL).groupdict()
        except Exception:
            pass
        return 0

def main():
    obj = VideoFilePreprocessor()
    basePath = "/Users/keertisekharsahoo/Documents/Masters Project/Video Inventory"
    obj.videoFilePreprocessor(basePath)

if __name__ == "__main__":
    main()