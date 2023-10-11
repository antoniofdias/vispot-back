from sanic import Sanic
from sanic.response import json
from sanic_ext import Extend
from dotenv import load_dotenv

load_dotenv()

from spotify import get_playlist_info
from tsne import increment_with_tsne_data
from lyrics import request_lyrics_per_track
from tfidf import calculate_correlation_matrix

app = Sanic("tcc_api")
app.config.CORS_ORIGINS = "*"
Extend(app)

@app.get("/playlist")
async def playlist_info(request):
  playlist_urls = request.args.get("playlist_url")
  playlist_url_array = playlist_urls.split("+")

  tracks_info = []
  for playlist_url in playlist_url_array:
    tracks_info += get_tracks_info(playlist_url)
  tracks_info = increment_with_tsne_data(tracks_info)
  correlation_matrix = get_correlation_matrix(tracks_info)
  
  return json({
    "songs": tracks_info,
    "correlation": correlation_matrix
  })

def get_tracks_info(playlist_url):
  if playlist_url is None:
    return json({})

  tracks_info = get_playlist_info(playlist_url)
  return tracks_info

def get_correlation_matrix(tracks_info):
  lyrics = request_lyrics_per_track(tracks_info)
  correlation_matrix = calculate_correlation_matrix(lyrics)

  return correlation_matrix

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=1337, workers=4)