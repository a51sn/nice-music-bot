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

def addTrack(trackURL, n):
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        sp.user_playlist_add_tracks(username, playlist_id, [trackURL], position=n)
    else:
        print("Can't get token for", username)
