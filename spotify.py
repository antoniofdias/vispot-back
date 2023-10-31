import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CID = os.getenv("SPOTIFY_CID")
SECRET = os.getenv("SPOTIFY_SECRET")

client_credentials_manager = SpotifyClientCredentials(
  client_id=CID, 
  client_secret=SECRET
)

spotify_api = spotipy.Spotify(
  client_credentials_manager = client_credentials_manager
)

def get_playlist_name(playlist_url):
  playlist_info = spotify_api.playlist(playlist_url)
  return playlist_info["name"]

def get_playlist_info(playlist_url, current_index):
  playlist_info = spotify_api.playlist(playlist_url)
  tracks_filtered = filter_playlist_tracks(playlist_info["tracks"], playlist_info["name"], current_index)
  tracks_detailed = retrieve_tracks_details(tracks_filtered)
  return tracks_detailed

def filter_playlist_tracks(playlist_info, playlist_name, current_index):
  items = playlist_info["items"]
  tracks_filtered = []

  for item_index, item in enumerate(items):
    track = item["track"]
    tracks_filtered.append(
      {
        "id": item_index + current_index + 1,
        "uri": track["uri"],
        "name": track["name"],
        "playlist": playlist_name,
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
        "artist": track["artists"][0]["name"]
      }
    )

  return tracks_filtered

def retrieve_tracks_details(tracks_filtered):
  tracks_detailed = []

  tracks_uri = map(lambda track_data: track_data["uri"], tracks_filtered)
  tracks_features = spotify_api.audio_features(tracks=tracks_uri)

  for track_index, track_features in enumerate(tracks_features):
    track_initial_data = tracks_filtered[track_index]
    track_detailed = retrieve_track_details(
      track_initial_data, 
      track_features
    )
    tracks_detailed.append(track_detailed)

  return tracks_detailed

def retrieve_track_details(track_initial_data, track_features):
  track_details = track_initial_data.copy()

  track_details["danceability"] = track_features["danceability"]
  track_details["energy"] = track_features["energy"]
  track_details["key"] = track_features["key"]
  track_details["loudness"] = track_features["loudness"]
  track_details["speechiness"] = track_features["speechiness"]
  track_details["acousticness"] = track_features["acousticness"]
  track_details["instrumentalness"] = track_features["instrumentalness"]
  track_details["liveness"] = track_features["liveness"]
  track_details["valence"] = track_features["valence"]
  track_details["tempo"] = track_features["tempo"]

  return track_details
