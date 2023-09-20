import pandas
from sklearn.manifold import TSNE
from matplotlib import colors
import matplotlib.pyplot as plt

COLUMNS_TO_SELECT = ["duration_ms", "danceability", "energy", "loudness", 
                     "speechiness", "acousticness", "instrumentalness", 
                     "liveness", "valence", "tempo"]

PALETTE_ARRAY = ['viridis', 'cividis', 'jet', 'hot']

tsne = TSNE(n_components=2, random_state=0)

def increment_with_tsne_data(playlist_info):
  incremented_playlist_info = []

  playlist_dataframe = pandas.DataFrame.from_records(playlist_info)
  playlist_dataframe = playlist_dataframe[COLUMNS_TO_SELECT]

  tsne_data = tsne.fit_transform(playlist_dataframe)

  for index, data in enumerate(tsne_data):
    track_info = playlist_info[index]
    track_info["x"] = float(data[0])
    track_info["y"] = float(data[1])

    colors = {}
    for palette in PALETTE_ARRAY:
      colors[palette] = {} 
      for column in COLUMNS_TO_SELECT:
        min_val = playlist_dataframe[column].min()
        max_val = playlist_dataframe[column].max()
        normalized_value = (playlist_dataframe.at[index, column] - min_val) / (max_val - min_val)
        colors[palette][column] = map_to_color(normalized_value, palette)
    track_info["colors"] = colors

    incremented_playlist_info.append(track_info)

  return incremented_playlist_info

def map_to_color(value, palette):
  norm = colors.Normalize(vmin=0, vmax=1)
  cmap = plt.get_cmap(palette)
  color = cmap(norm(value))
  hex_code = colors.rgb2hex(color)

  return hex_code