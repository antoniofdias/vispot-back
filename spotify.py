import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

API = "https://api.spotify.com"
CID = os.getenv("SPOTIFY_CID")
SECRET = os.getenv("SPOTIFY_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=CID, 
    client_secret=SECRET
)

spotify_api = spotipy.Spotify(
    client_credentials_manager = client_credentials_manager
)

def get_playlist_info(playlist_url):
    return spotify_api.album_tracks(playlist_url)
