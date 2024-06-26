import spotipy
import spotipy.util as util
import time
from dotenv import load_dotenv
import os

load_dotenv()

# Set up your Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = 'http://localhost:8080/callback'
username = os.getenv('SPOTIFY_USERNAME')

# Set up scope (permissions)
scope = 'user-read-currently-playing user-modify-playback-state streaming user-read-playback-state'

# Get access token
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Create Spotify client
sp = spotipy.Spotify(auth=token)

def refresh_token():
    # token expired? refresh it
    # Get access token
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

    # Create Spotify client
    sp = spotipy.Spotify(auth=token)

    return sp

def now_playing():
    try:
        current_track = sp.current_user_playing_track()
    except:
        sp = refresh_token()
        current_track = sp.current_user_playing_track()

    if current_track is not None:
        track_name = current_track['item']['name']
        artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
        return f"{track_name} by {artists}"
    else:
        return "No track currently playing."
    
def skip_song():
    try:
        sp.next_track()
    except:
        sp = refresh_token()
        sp.next_track()

def toggle_playback():
    try:
        current_playback = sp.current_playback()
        if current_playback["is_playing"]:
            sp.pause_playback()
        else:
            sp.start_playback()
    except:
        sp = refresh_token()
        current_playback = sp.current_playback()
        if current_playback["is_playing"]:
            sp.pause_playback()
        else:
            sp.start_playback()