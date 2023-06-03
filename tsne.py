import pandas
from sklearn.manifold import TSNE

COLUMNS_TO_SELECT = ["duration_ms", "danceability", "energy", "loudness", 
           "speechiness", "acousticness", "instrumentalness", 
           "liveness", "valence", "tempo"]

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
    incremented_playlist_info.append(track_info)

  return incremented_playlist_info
