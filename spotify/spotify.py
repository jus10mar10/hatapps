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
scope = 'user-read-currently-playing'

# Get access token
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

# Create Spotify client
sp = spotipy.Spotify(auth=token)

def now_playing():
    try:
        current_track = sp.current_user_playing_track()
    except:
        # token expired?
        # Set up scope (permissions)
        scope = 'user-read-currently-playing'

        # Get access token
        token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

        # Create Spotify client
        sp = spotipy.Spotify(auth=token)

        current_track = sp.current_user_playing_track()
    if current_track is not None:
        track_name = current_track['item']['name']
        artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
        return f"{track_name} by {artists}"
    else:
        return "No track currently playing."