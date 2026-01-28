from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from dotenv import load_dotenv
import asyncio

load_dotenv()

from mocks.loader import (
  get_tracks_by_playlist,
  get_playlist_name_from_csv,
)

from tsne import increment_with_tsne_data
from tfidf import calculate_correlation_matrix

app = Sanic("tcc_api")
app.config.CORS_ORIGINS = "*"
Extend(app)

@app.get("/playlist_name")
async def playlist_name(request):
  playlist = request.args.get("playlist")

  if not playlist:
    return json({"error": "playlist is required"}, status=400)

  return json({
    "name": get_playlist_name_from_csv(playlist)
  })


@app.get("/mock")
async def mock_playlist(request):
  playlists = request.args.get("playlist")

  if not playlists:
    return json({"error": "playlist is required"}, status=400)

  playlist_array = playlists.split("+")

  tracks_info = get_tracks_by_playlist(playlist_array)

  if not tracks_info:
    return json({
      "songs": [],
      "correlation": []
    })

  loop = asyncio.get_running_loop()

  tracks_info = await loop.run_in_executor(
    None,
    increment_with_tsne_data,
    tracks_info
  )

  lyrics = [track.get("lyrics", "") for track in tracks_info]

  correlation_matrix = await loop.run_in_executor(
    None,
    calculate_correlation_matrix,
    lyrics
  )

  return json({
    "songs": tracks_info,
    "correlation": correlation_matrix
  })


@app.get("/playlists")
async def list_playlists(request):
  from mocks.loader import load_tracks_from_csv

  tracks = load_tracks_from_csv()
  playlists = sorted({track["playlist"] for track in tracks})

  return json(playlists)


if __name__ == "__main__":
  app.run(
    host="0.0.0.0",
    port=1337,
    workers=4,
    auto_reload=True,
  )
