import xbmc
import xbmcgui
import json
import random
import threading
import sys
import time
import urllib
import urllib.parse
from .utils import log, busyDiag
from .settings import select_shows, list_items
from .addon import ADDON, ADDON_ICON, ADDON_NAME, ADDON_ID
from .core import create_playlist
from .player import Player

monitor = xbmc.Monitor()

playlist = []

INCLUDED_SHOWS = ADDON.getSetting("included_shows")
BACK_WINDOW = xbmcgui.Window()

def start():
    if len(sys.argv) > 1:
        if sys.argv[1] == "SelectShows":
            select_shows(INCLUDED_SHOWS)
        quit()
    
    if ADDON.getSetting("ShowNotifications") == "true": 
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(ADDON_NAME, ADDON.getLocalizedString(32007), 2000, ADDON_ICON))

    BACK_WINDOW.show()
    busyDiag.create()

    if hasattr(sys, 'listitem'):
        list_items(INCLUDED_SHOWS)
    else:
        playlist = create_playlist()

    if len(playlist) == 0:
        log("No episodes found. Please check your library.")
        xbmcgui.Dialog().ok(ADDON_NAME, ADDON.getLocalizedString(32008), ADDON.getLocalizedString(32009))
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % ADDON_ID)
        BACK_WINDOW.close()
        log("Stopping")
        log("-------------------------------------------------------------------------")
        quit()
    else:
        log("--------- Episodes Found")
        # Get Auto Stop Check Time - Current Time + Auto Stop Check Timer
        if ADDON.getSetting("AutoStop") == "true":
            log("-- Auto Stop Enabled")
            AutoStopCheckTime = int(time.time()) + (int(ADDON.getSetting("AutoStopTimer")) * 60)
            AutoStopWait = (int(ADDON.getSetting("AutoStopWait")) * 60)
            AutoStopDialog = xbmcgui.DialogProgress()
            log("-- Auto Stop Timer: " + str(AutoStopCheckTime))
            log("-- Auto Stop Wait: " + str(AutoStopWait))
        #

        # Initialize our Player
        player = Player()
        
        # Create Playlist
        myPlaylist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

        # Shuffle Episodes
        random.shuffle(playlist)
        
        # Build Playlist
        buildPlaylist(playlist)

        # Start Player
        player.play(item=myPlaylist)