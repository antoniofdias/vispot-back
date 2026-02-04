import pandas as pd
from pathlib import Path

MOCKS_PATH = Path("mocks")

CSV_FILES = [
    "emo_playlist_dataset.csv",
    "punks_playlist_dataset.csv",
    "geeks_playlist_dataset.csv",
    "queer_playlist_dataset.csv",
    "hardcore_playlist_dataset.csv",
]

_cached_tracks = None


def _load_all_csvs():
    dataframes = []

    for csv_file in CSV_FILES:
        csv_path = MOCKS_PATH / csv_file

        if not csv_path.exists():
            raise FileNotFoundError(f"Mock CSV not found: {csv_path}")

        df = pd.read_csv(csv_path)
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    merged_df = merged_df.fillna("")

    return merged_df


def load_tracks_from_csv():
    """
    Loads and caches all mocked tracks from all CSV files.
    """
    global _cached_tracks

    if _cached_tracks is not None:
        return _cached_tracks

    df = _load_all_csvs()

    tracks = []

    for _, row in df.iterrows():
        track = {
            # NOTE: ID will be overridden later (tsne step)
            "id": None,

            "name": row.get("name"),
            "artist": row.get("artists_name"),
            "playlist": row.get("playlist"),
            "lyrics": str(row.get("lyrics", "")).lower(),

            # audio features
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

    _cached_tracks = tracks
    return tracks


def get_tracks_by_playlist(playlists):
    """
    Returns tracks filtered by one or more playlist names.
    """
    if isinstance(playlists, str):
        playlists = [playlists]

    playlists = set(playlists)

    all_tracks = load_tracks_from_csv()

    return [
        track for track in all_tracks
        if track.get("playlist") in playlists
    ]


def get_playlist_name_from_csv(playlist):
    """
    Keeps API compatibility with the old Spotify-based endpoint.
    """
    return playlist
