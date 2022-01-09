import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

USER = os.getenv("USER")
PLAYLIST = os.getenv("PLAYLIST")


import spotipy
username = USER
scope = 'playlist-modify-public'
token = spotipy.util.prompt_for_user_token(username,
                           scope,
                           client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           redirect_uri='http://localhost/')

playlist_id =  PLAYLIST

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
else:
    print("Can't get token for", username)


def add_track(trackURL, i=0):
    sp.user_playlist_add_tracks(username, playlist_id, [trackURL], position=i)


def get_playlist_tracks():
    tracks = []
    total = sp.playlist_items(playlist_id, fields="total")['total']
    offset = 0
    while offset < total:
        tracks.extend(sp.playlist_items(playlist_id, fields="items(track(id))", offset=offset)['items'])
        offset += 100
    return tracks


def find_duplicate_tracks(tracks):
    seen = set()
    num_dups = 0
    dups = {}
    for i, item in enumerate(tracks):
        uri = item['track']['id']
        if item['track']['id'] in seen:
            num_dups += 1
            if uri in dups:
                dups[uri].append(i)
            else:
                dups[uri] = [i]
        else:
            seen.add(item['track']['id'])
    return dups, num_dups


def itemize_duplicates(duplicates):
    items = []
    for key in duplicates:
        items.append({"uri": key, "positions":duplicates[key]})
    return items


def remove_duplicates(items):
    sp.playlist_remove_specific_occurrences_of_items(playlist_id, items)