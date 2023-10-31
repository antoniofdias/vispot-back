import requests
import os
import concurrent.futures

MUSIXMATCH_KEY = os.getenv("MUSIXMATCH_KEY")

def request_lyrics_per_track(tracks):
  lyrics = []

  with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_track = { executor.submit(retrieve_from_api, track): track for track in tracks }

    for future in concurrent.futures.as_completed(future_to_track):
      track = future_to_track[future]
      try:
        lyric = future.result()
        lyrics.append(lyric)
      except Exception as e:
        print(f"Error retrieving lyric for track: {track}")
        print(str(e))

  return lyrics

def retrieve_from_api(track):
  artist = track["artist"]
  track_name = track["name"]
  url = f"https://api.musixmatch.com/ws/1.1/matcher.lyrics.get?apikey={MUSIXMATCH_KEY}&q_track={track_name}&q_artist={artist}"
  payload = {}

  response = requests.get(url, data=payload)
  try:
    lyric = response.json()["message"]["body"]["lyrics"]["lyrics_body"].replace("\n", " ").replace("******* This Lyrics is NOT for Commercial use *******", "").lower()
  except:
    lyric = ""

  return lyric
