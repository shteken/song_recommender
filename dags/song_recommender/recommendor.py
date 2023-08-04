import pandas as pd
import sklearn
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

def read_file(playlist, path):
    full_path = f"{path}/{playlist}.csv"
    return pd.read_csv(full_path, index_col=0)

def retain_relevant_columns(df):
    return df.select_dtypes(include=[float, int])

def normelize_matrix(df):
    "Each feature has different magnitude from each other. Especially duration_ms"
    return normalize(df, axis=0)

def power_and_sum_each_new_song_column(df):
    powered_df = df ** 2
    sum_each_column = powered_df.sum()
    square_rooted_df = sum_each_column ** 0.5
    return square_rooted_df.sort_values(ascending=False)

liked_songs = read_file("0L0b49nWbU309wZDIHqOHX", "/home/baruch/music_database/liked_songs_features")
new_songs = read_file("37i9dQZEVXbMDoHDwVN2tF", "/home/baruch/music_database/new_songs_features")



liked_songs_processed = retain_relevant_columns(liked_songs)
new_songs_processed = retain_relevant_columns(new_songs)

# print(liked_songs_processed)
# print(new_songs_processed)

normelized_liked_songs_processed = normelize_matrix(liked_songs_processed)
normelized_new_songs_processed = normelize_matrix(new_songs_processed)

# print(normelized_liked_songs_processed)
# print(normelized_new_songs_processed)


cosine_similarities = cosine_similarity(normelized_liked_songs_processed, normelized_new_songs_processed)
df = pd.DataFrame(cosine_similarities)
print(df)

final_df = power_and_sum_each_new_song_column(df)
print(final_df)
