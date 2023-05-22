import requests
import os
import concurrent.futures

VAGALUME_KEY = os.getenv("VAGALUME_KEY")

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
    song = track["name"]
    url = f"https://api.vagalume.com.br/search.php?art={artist}&mus={song}&apikey={VAGALUME_KEY}"
    payload = {}

    response = requests.post(url, data=payload)
    try:
        lyric = response.json()["mus"][0]["text"].replace("\n", " ").lower()
    except:
        lyric = ""

    return lyric
