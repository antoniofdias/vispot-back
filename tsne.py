import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from matplotlib import colors as mpl_colors
import matplotlib.pyplot as plt

COLUMNS_TO_SELECT = [
    "duration_ms",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]

PALETTE_ARRAY = ["viridis", "cividis", "jet", "hot", "plasma", "copper"]


def increment_with_tsne_data(playlist_info):
    if not playlist_info:
        return []

    df = pd.DataFrame.from_records(playlist_info)
    df_features = df[COLUMNS_TO_SELECT]

    n_samples = len(df_features)

    # Handle very small datasets safely
    if n_samples < 3:
        for idx, track in enumerate(playlist_info, start=1):
            track["id"] = idx
            track["x"] = 0.0
            track["y"] = 0.0
            track["colors"] = {}
        return playlist_info

    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(df_features)

    perplexity = min(30, max(2, n_samples - 1))

    tsne = TSNE(
        n_components=2,
        random_state=0,
        perplexity=perplexity,
        init="random",
    )

    tsne_data = tsne.fit_transform(standardized_data)

    # Precompute min/max per column
    min_max = {
        column: (df_features[column].min(), df_features[column].max())
        for column in COLUMNS_TO_SELECT
    }

    base_color_array = [
        "#4CAF50",
        "#75485E",
        "#CB904D",
        "#255F85",
        "#FFCAE9",
    ]

    playlist_colors = {}

    for index, point in enumerate(tsne_data):
        track_info = playlist_info[index]

        # ✅ Numeric ascending ID (1-based)
        track_info["id"] = index + 1

        track_info["x"] = float(point[0])
        track_info["y"] = float(point[1])

        playlist_name = track_info.get("playlist", "default")

        if playlist_name not in playlist_colors:
            playlist_colors[playlist_name] = base_color_array[
                len(playlist_colors) % len(base_color_array)
            ]

        color_map = {}

        for palette in PALETTE_ARRAY:
            palette_colors = {}

            for column in COLUMNS_TO_SELECT:
                min_val, max_val = min_max[column]
                value = df_features.at[index, column]

                if max_val == min_val:
                    normalized = 0.0
                else:
                    normalized = (value - min_val) / (max_val - min_val)

                palette_colors[column] = map_to_color(normalized, palette)

            palette_colors["playlist"] = playlist_colors[playlist_name]
            color_map[palette] = palette_colors

        track_info["colors"] = color_map

    return playlist_info


def map_to_color(value, palette):
    norm = mpl_colors.Normalize(vmin=0, vmax=1)
    cmap = plt.get_cmap(palette)
    rgba = cmap(norm(value))
    return mpl_colors.rgb2hex(rgba)
