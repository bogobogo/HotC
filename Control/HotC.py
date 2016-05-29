"""
HotC controller.
"""

import time
import sys
sys.path.append("..")

import Machine_Learning
import Machine_Learning.dominant_freqs_learner
import Display.song_display
import Control.recorder as recorder
import Control.config as config
import random #Only used for pseudo brain. #TODO: Delete in integration

class PseudoBrain(object):
    """
    A happiness detector of WAV file that always returns random number
    This class emulates Lellouch's extra fine PyBrain object and can be deleted safely at integration
    """
    def __init__(self):
        super(PseudoBrain, self).__init__()
        self.network = Machine_Learning.dominant_freqs_learner.DominantFreqsLearner(6, 1)
        self.network.load_network('dfl2.xml')

    def run(self, wav_filename):
        print "[BRAIN|PSEUDO BRAIN] Analyzing WAV..."
        time.sleep(1.2)
        print "[BRAIN|PSEUDO BRAIN] Finished analyzing"
        return config.HAPPINESS_MIN_LEVEL + (
                self.analize_wav(wav_filename)/ (config.HAPPINESS_MAX_LEVEL - config.HAPPINESS_MIN_LEVEL)
                )

    def analize_wav(self, wav_filename):
        return self.network.calculate_file(wav_filename)


class HotC(object):
    """
    Happiness of the Crowd main class
    """

    def __init__(self):
        super(HotC, self).__init__()
        self._happiness_display = Display.song_display.HappinessDependantSongDisplay()
        self._happiness_brain = PseudoBrain() #TODO: Replace with Lellouch's brain

    def handle_person(self):
        """
        Handle a single person from the crowd.
        Consists of 3 stages:
            1. Record the person
            2. Process its happiness
            3. Display the result
        """

        # 1. Record
        record_filename = self._generate_wav_filename()
        print "[HotC] Recording crowd to file \"%s\"..." % (record_filename, )
        recorder.record_to_file(record_filename, 1)
        print "[HotC] Done"

        # 2. Process
        print "[HotC] Processing happiness..."
        #TODO: Change "run" accordingly to Lellouch interface
        happiness_level = self._happiness_brain.run(record_filename)
        print "[HotC] Done"

        # 3. Display
        print "[HotC] Displaying happiness level..."
        self._happiness_display.display_happiness_level(record_filename, happiness_level)
        print "[HotC] Done"

    def serve_forever(self):
        while True:
            self.handle_person()

    def _generate_wav_filename(self):
        timestamp = time.strftime(config.TIMESTAMP_FORMAT)
        wav_filename = config.RECORD_PATH_TEMPLATE % (timestamp, )
        return wav_filename
