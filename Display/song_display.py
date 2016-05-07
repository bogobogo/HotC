import os
import os.path
import subprocess
import time

import Control.config
import happiness_display

HAPPINESS_MIN_LEVEL_TO_SONG = { 0: "badad.mp3",
        0.2: "fallen_angel.mp3",
        0.4: "hotel_california.mp3",
        0.6: "feel_good_inc.mp3",
        0.8: "happy.mp3" }


class HappinessDependantSongDisplay(happiness_display.HappinessDisplay):

    def __init__(self, songs_dir="./Songs/"):
        self._songs_dir = songs_dir

    def _get_song_path(self, song_name):
        return os.path.join(self._songs_dir, song_name)

    def display_happiness_level(self, wav_filename, level):
        print "[Display|Song Display] wav name \"%s\" is level %s" % (wav_filename, level, )
        normalized_level = round((5* level) - 0.5) / 5
        if not Control.config.HAPPINESS_MIN_LEVEL <= level <= Control.config.HAPPINESS_MAX_LEVEL:
            raise ValueError("Happiness level not in range (%s)" % (level, ))

        chosen_song = self._get_song_path(HAPPINESS_MIN_LEVEL_TO_SONG[normalized_level])
        print "[Display|Song Display] Playing song at %s" % (chosen_song, )

        play_song(chosen_song)

def play_song(song_path):
    if os.name == "nt":
        first_argument = "start"
    elif os.name == "posix":
        first_argument = "mpg321"

    song_process = subprocess.Popen([first_argument, song_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
    print 'playing song'

    try:
        time.sleep(15)

    finally:
        song_process.kill()
        song_process.wait()

