from sanic import Sanic
from sanic.response import json
from spotify import get_playlist_info
from tsne import increment_with_tsne_data

app = Sanic("tcc_api")

@app.get("/playlist")
async def playlist_info(request):
    playlist_url = request.args.get("playlist_url")
    if playlist_url is None:
        return json({})
    playlist_info = get_playlist_info(playlist_url)
    playlist_info = increment_with_tsne_data(playlist_info)
    return json(playlist_info)

if __name__ == "__main__":
    app.run()
