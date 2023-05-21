from sanic import Sanic
from sanic.response import json
from spotify import get_playlist_info
from tsne import increment_with_tsne_data
from lyrics import request_lyrics_per_track
from dotenv import load_dotenv

app = Sanic("tcc_api")

load_dotenv()

@app.get("/playlist")
async def playlist_info(request):
    tracks_info = get_tracks_info(request)
    correlation_matrix = get_correlation_matrix(tracks_info)
    return json({
        "songs": tracks_info,
        "correlation": correlation_matrix
    })

def get_tracks_info(request):
    playlist_url = request.args.get("playlist_url")

    if playlist_url is None:
        return json({})

    tracks_info = get_playlist_info(playlist_url)
    tracks_info = increment_with_tsne_data(tracks_info)
    return tracks_info

def get_correlation_matrix(tracks_info):
    lyrics = request_lyrics_per_track(tracks_info)

    return [[]]
