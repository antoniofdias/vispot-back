import pandas as pd

COLUMNS_TO_SELECT = [
  "duration_ms", "danceability", "energy", "loudness",
  "speechiness", "acousticness", "instrumentalness",
  "liveness", "valence", "tempo"
]

def load_tracks_from_csv(path="mocks/emo_playlist_dataset.csv"):
  df = pd.read_csv(path)

  df = df.fillna("")

  tracks = []

  for _, row in df.iterrows():
    track = {
      "id": row.get("id"),
      "name": row.get("name"),
      "artist": row.get("artists_id"),
      "playlist": row.get("playlist"),
      "lyrics": str(row.get("lyrics", "")).lower(),
      "duration_ms": row.get("duration_ms"),
      "danceability": row.get("danceability"),
      "energy": row.get("energy"),
      "loudness": row.get("loudness"),
      "speechiness": row.get("speechiness"),
      "acousticness": row.get("acousticness"),
      "instrumentalness": row.get("instrumentalness"),
      "liveness": row.get("liveness"),
      "valence": row.get("valence"),
      "tempo": row.get("tempo"),
    }

    tracks.append(track)

  return tracks


def get_playlist_name_from_csv(playlist_name):
  return playlist_name


def get_tracks_by_playlist(playlists, csv_path="mocks/emo_playlist_dataset.csv"):
  df = pd.read_csv(csv_path)

  if isinstance(playlists, str):
    playlists = [playlists]

  df = df[df["playlist"].isin(playlists)]
  df = df.fillna("")

  return load_tracks_from_dataframe(df)


def load_tracks_from_dataframe(df):
  tracks = []

  for _, row in df.iterrows():
    tracks.append({
      "id": row["id"],
      "name": row["name"],
      "artist": row["artists_id"],
      "playlist": row["playlist"],
      "lyrics": str(row["lyrics"]).lower(),

      "duration_ms": row["duration_ms"],
      "danceability": row["danceability"],
      "energy": row["energy"],
      "loudness": row["loudness"],
      "speechiness": row["speechiness"],
      "acousticness": row["acousticness"],
      "instrumentalness": row["instrumentalness"],
      "liveness": row["liveness"],
      "valence": row["valence"],
      "tempo": row["tempo"],
    })

  return tracks
