import json
import xbmc
from .utils import log
from .addon import ADDON


def create_playlist(included_shows) -> list:
    log("Addon Menu Start")

    playlist = []

    if ADDON.getSetting("IncludeAll") == "true":
        command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "id": 1}'
        all_shows = json.loads(xbmc.executeJSONRPC(command))
    
        if all_shows['result']['limits']['total'] > 0:
            for show in all_shows['result']['tvshows']:
                command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "tvshowid": %d, "properties": ["showtitle", "file", "playcount", "lastplayed", "resume"] }, "id": 1}' % (show['tvshowid'])
                all_episodes = json.loads(xbmc.executeJSONRPC(command))
            
                if all_episodes['result']['limits']['total'] > 0:
                    for episode in all_episodes['result']['episodes']:
                        if ADDON.getSetting("IncludeUnwatched") == "true" or episode['playcount'] > 0:
                            log("Added Episode: " + str(episode['episodeid']) + " -- " + episode['showtitle'] + " - " + episode['label'])
                            playlist.append({'episodeId': episode['episodeid'], 'episodeShow': episode['showtitle'], 'episodeName': episode['label'], 'episodeFile': episode['file'], 'playCount': episode['playcount'], 'lastPlayed': episode['lastplayed'], 'resume': episode['resume']})

    else:
        for included_show in map(int, included_shows.split(", ")):
            command = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "tvshowid": %d, "properties": ["showtitle", "file", "playcount", "lastplayed", "resume"] }, "id": 1}' % included_show
            all_episodes = json.loads(xbmc.executeJSONRPC(command))
            
            if all_episodes['result']['limits']['total'] > 0:
                for episode in all_episodes['result']['episodes']:
                    if ADDON.getSetting("IncludeUnwatched") == "true" or episode['playcount'] > 0:
                        log("Added Episode: " + str(episode['episodeid']) + " -- " + episode['showtitle'] + " - " + episode['label'])
                        playlist.append({'episodeId': episode['episodeid'], 'episodeShow': episode['showtitle'], 'episodeName': episode['label'], 'episodeFile': episode['file'], 'playCount': episode['playcount'], 'lastPlayed': episode['lastplayed'], 'resume': episode['resume']})
    
    return playlist