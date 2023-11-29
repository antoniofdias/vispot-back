import pandas
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from matplotlib import colors
import matplotlib.pyplot as plt

COLUMNS_TO_SELECT = ["duration_ms", "danceability", "energy", "loudness", 
                     "speechiness", "acousticness", "instrumentalness", 
                     "liveness", "valence", "tempo"]

PALETTE_ARRAY = ['viridis', 'cividis', 'jet', 'hot', 'Oranges']

tsne = TSNE(n_components=2, random_state=0)

def increment_with_tsne_data(playlist_info):
  incremented_playlist_info = []
  color_array = ['#4CAF50', '#75485E', '#CB904D', '#255F85', '#FFCAE9']
  playlist_colors = {}

  playlist_dataframe = pandas.DataFrame.from_records(playlist_info)
  playlist_dataframe = playlist_dataframe[COLUMNS_TO_SELECT]

  scaler = StandardScaler()

  standardized_data = scaler.fit_transform(playlist_dataframe)
  standardized_dataframe = pandas.DataFrame(standardized_data, columns=playlist_dataframe.columns)

  tsne_data = tsne.fit_transform(standardized_dataframe)

  for index, data in enumerate(tsne_data):
    track_info = playlist_info[index]
    track_info["x"] = float(data[0])
    track_info["y"] = float(data[1])

    if track_info["playlist"] not in playlist_colors:
      playlist_colors[track_info["playlist"]] = color_array[0]
      color_array.pop(0)

    colors = {}
    for palette in PALETTE_ARRAY:
      lowercase_palette = palette.lower()
      colors[lowercase_palette] = {} 
      for column in COLUMNS_TO_SELECT:
        min_val = playlist_dataframe[column].min()
        max_val = playlist_dataframe[column].max()
        normalized_value = (playlist_dataframe.at[index, column] - min_val) / (max_val - min_val)
        colors[lowercase_palette][column] = map_to_color(normalized_value, palette)
      colors[lowercase_palette]["playlist"] = playlist_colors[track_info["playlist"]]
    track_info["colors"] = colors

    incremented_playlist_info.append(track_info)

  return incremented_playlist_info

def map_to_color(value, palette):
  norm = colors.Normalize(vmin=0, vmax=1)
  cmap = plt.get_cmap(palette)
  color = cmap(norm(value))
  hex_code = colors.rgb2hex(color)

  return hex_code