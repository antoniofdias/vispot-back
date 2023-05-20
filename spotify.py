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
    playlist_info = spotify_api.playlist_tracks(playlist_url)
    return filter_playlist_tracks(playlist_info)

def filter_playlist_tracks(playlist_info):
    items = playlist_info["items"]
    tracks_filtered = []

    for item in items:
        track = item["track"]
        tracks_filtered.append(
            {
                "uri": track["uri"],
                "name": track["name"],
                "duration": track["duration_ms"],
                "explicit": track["explicit"],
                "artist": track["artists"][0]["name"]
            }
        )

    return tracks_filtered
