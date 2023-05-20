from sanic import Sanic
from sanic.response import json
from spotify import get_playlist_info

app = Sanic("tcc_api")

@app.get("/playlist")
async def playlist_info(request):
    playlist_url = request.args.get("playlist_url")
    if playlist_url is None:
        return json({})
    playlist_info = get_playlist_info(playlist_url)
    return json(playlist_info)
