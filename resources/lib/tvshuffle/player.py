import xbmc
from .utils import log


class Player(xbmc.Player):
    def __init__(self, *args):
        xbmc.Player.__init__(self, *args)
        self.mediaStarted = False
        self.mediaEnded = False
        self.scriptStopped = False
        self.playlist = None
        log("Player initialized")

    def onPlayBackStarted(self):
        self._toggle_false()
        self.mediaStarted = True
        log("Playback started")

    def onPlayBackEnded(self):
        self._toggle_false()
        self.mediaEnded = True
        log("Playback ended")
	
    def onPlayBackStopped(self):
        self._toggle_false
        self.scriptStopped = True
        log("Playback stopped")
	
    def load_playlist(self, playlist):


    def _toggle_false(self):
        self.mediaStarted = False
        self.mediaEnded = False
        self.scriptStopped = False