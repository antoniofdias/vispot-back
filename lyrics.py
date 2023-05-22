import requests
import os

VAGALUME_KEY = os.getenv("VAGALUME_KEY")

def request_lyrics_per_track(tracks):
    lyrics = []

    for track in tracks:
        artist_name = track["artist"]
        song_name = track["name"]

        lyric = retrieve_from_api(artist_name, song_name)
        lyrics.append(lyric)

    return lyrics

def retrieve_from_api(artist, song):
    url = f"https://api.vagalume.com.br/search.php?art={artist}&mus={song}&apikey={VAGALUME_KEY}"
    payload = {}

    response = requests.post(url, data=payload)
    try:
        lyric = response.json()["mus"][0]["text"].replace("\n", " ").lower()
    except:
        lyric = ""

    return lyric
