import Control.config as config

class HappinessDisplay(object):
    def __init__(self):
        super(HappinessDisplay, self).__init__()

    def display_happiness_level(self, wav_filename="", level=config.HAPPINESS_MAX_LEVEL):
        raise NotImplementedError()

class PseudoDisplay(HappinessDisplay):
    """
    A displayer of happiness level that just the level to the screen.
    MAY BE DELETED
    """

    def __init__(self):
        super(PseudoDisplay, self).__init__()

    def display_happiness_level(self, wav_filename, level):
        print "[HAPPINESS DISPLAY|PSEUDO DISPLAY] %s happiness is level %s" % (wav_filename, level, )
