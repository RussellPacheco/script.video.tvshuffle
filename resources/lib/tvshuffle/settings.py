import json
import urllib
import sys
import xbmc
import xbmcgui
from .utils import log, busyDiag
from .addon import ADDON, ADDON_ID


def select_shows(included_shows):
    log("Settings - SelectShows")
    busyDiag.create()
    list_shows = []
    list_preselect = []
    list_post_select = []
    command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"sort": {"ignorearticle": true, "method": "label", "order": "ascending"}}, "id": 1}'
    all_shows = json.loads(xbmc.executeJSONRPC(command))
    if all_shows['result']['limits']['total'] > 0:
        for show in all_shows['result']['tvshows']:
            list_shows.append(show['label'])
            
            if not included_shows == "":
                if show['tvshowid'] in map(int, included_shows.split(", ")):
                    list_preselect.append(len(list_shows) - 1)

        
    busyDiag.close()
    selected_shows = xbmcgui.Dialog().multiselect(ADDON.getLocalizedString(32012), list_shows, preselect=list_preselect)

    
    if not selected_shows is None:
        for selected_show in selected_shows:
            list_post_select.append(all_shows['result']['tvshows'][selected_show]['tvshowid'])
        
        included_shows = ", ".join(str(i) for i in list_post_select)
        ADDON.setSetting("includedShows", included_shows)

    xbmc.executebuiltin('Addon.OpenSettings(%s)' % ADDON_ID)
    xbmc.executebuiltin('SetFocus(201)')


def list_items(included_shows) -> list:
    log("--------- Context Menu Selected")
    log("-- Item Label: " + sys.listitem.getLabel())

    selected_path = sys.listitem.getPath()
    log("-- Item Path: " + selected_path)

    if "favourites" in selected_path:
        log("-- Selected from Favourites")
        log("---- Decoded Path: " + urllib.parse.unquote(selected_path))
        embedded_path = urllib.parse.unquote(selected_path).split('"')[1]
        log("---- Embeddedd Path: " + embedded_path)
        selected_show = embedded_path.split('/')[4]
        selected_season = embedded_path.split('/')[5]
    elif "inprogresstvshows" in selected_path:
        log("-- Selected from In Progress")
        selected_show = selected_path.split('/')[3]
        selected_season = selected_path.split('/')[4]
    elif "tvshows" in selected_path:
        log("-- Selected from TV Shows")
        selected_show = selected_path.split('/')[4]
        selected_season = selected_path.split('/')[5]
    
    if selected_season == "": selected_season = "-1"
    selected_season = int(selected_season)
    selected_show = int(selected_show)
    
    log("-- Show ID: " + str(selected_show))
    log("-- Season: " + str(selected_season))
    
    if selected_season > 0:
        command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "tvshowid": %d, "season": %d, "properties": ["showtitle", "file", "playcount", "lastplayed", "resume"] }, "id": 1}' % (selected_show, selected_season)
    else:
        command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "tvshowid": %d, "properties": ["showtitle", "file", "playcount", "lastplayed", "resume"] }, "id": 1}' % selected_show
        
    returned_episodes = json.loads(xbmc.executeJSONRPC(command))
    
    my_episodes = []
    if returned_episodes['result']['limits']['total'] > 0:
        for episode in returned_episodes['result']['episodes']:
            if ADDON.getSetting("IncludeUnwatched") == "true" or episode['playcount'] > 0:
                log("Added Episode: " + str(episode['episodeid']) + " -- " + episode['showtitle'] + " - " + episode['label'])
                my_episodes.append({'episodeId': episode['episodeid'], 'episodeShow': episode['showtitle'], 'episodeName': episode['label'], 'episodeFile': episode['file'], 'playCount': episode['playcount'], 'lastPlayed': episode['lastplayed'], 'resume': episode['resume']})

    return my_episodes