from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from dotenv import load_dotenv

load_dotenv()

from tsne import increment_with_tsne_data
from tfidf import calculate_correlation_matrix

from mocks.loader import (
  load_tracks_from_csv,
  get_tracks_by_playlist,
  get_playlist_name_from_csv
)

app = Sanic("tcc_api")
app.config.CORS_ORIGINS = "*"
Extend(app)

@app.get("/playlist_name")
async def playlist_name(request):
  playlist = request.args.get("playlist", "mock_playlist")

  return json({
    "name": get_playlist_name_from_csv(playlist)
  })

@app.get("/playlist")
async def playlist_info(request):
  playlists = request.args.get("playlist")

  if not playlists:
    return json({"error": "playlist is required"}, status=400)

  playlist_array = playlists.split("+")

  tracks_info = get_tracks_by_playlist(playlist_array)

  tracks_info = increment_with_tsne_data(tracks_info)

  lyrics = [track["lyrics"] for track in tracks_info]
  correlation_matrix = calculate_correlation_matrix(lyrics)

  return json({
    "songs": tracks_info,
    "correlation": correlation_matrix
  })

def get_tracks_info(playlist_url, current_index):
  if playlist_url is None:
    return json({})

  tracks_info = get_playlist_info(playlist_url, current_index)
  return tracks_info

def get_correlation_matrix(tracks_info):
  lyrics = request_lyrics_per_track(tracks_info)
  correlation_matrix = calculate_correlation_matrix(lyrics)

  return correlation_matrix

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1337, workers=4)