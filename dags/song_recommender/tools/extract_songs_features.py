from functools import partial
from pathlib import Path
import pandas as pd
from spotipy_client import sp, LIMIT_SONGS_PER_REQUEST, LIMIT_SONGS_PER_REQUEST_FOR_FEATURES, send_requests_to_spotify


PLAYLIST = "0L0b49nWbU309wZDIHqOHX" # this value should be parameterized
FILE_PATH = "music_database/features_songs_from_list/data.csv" # this value should be parameterized
total_songs_in_playlist = sp.playlist_tracks(playlist_id=PLAYLIST, fields="total")["total"]


def extract_songs_features():
    songs_to_analyze = send_requests_to_spotify(get_playlist_songs, total_songs_in_playlist, LIMIT_SONGS_PER_REQUEST)
    get_songs_features_partial = partial(get_songs_features, songs_to_analyze)
    songs_features = send_requests_to_spotify(get_songs_features_partial, total_songs_in_playlist, LIMIT_SONGS_PER_REQUEST_FOR_FEATURES)
    songs_features_df = transform_features_into_df(songs_features)
    save_features_in_file(songs_features_df)

def get_playlist_songs(request_number, limit_items_per_request):
    songs_in_page = sp.playlist_tracks(playlist_id=PLAYLIST, offset=(request_number-1)*limit_items_per_request, limit=limit_items_per_request, fields="items(track(id))")["items"]
    songs_ids_in_page = [song_info["track"]["id"] for song_info in songs_in_page]
    return songs_ids_in_page

def get_songs_features(songs_ids, request_number, limit_items_per_request):
    songs_features_in_page = sp.audio_features(songs_ids[(request_number-1)*limit_items_per_request:request_number * limit_items_per_request])
    return songs_features_in_page

def transform_features_into_df(songs_features):
    return pd.DataFrame(songs_features)

def save_features_in_file(songs_features):
    filepath = Path.home() / FILE_PATH
    filepath.parent.mkdir(parents=True, exist_ok=True)
    songs_features.to_csv(filepath) 


if __name__ == '__main__':
    extract_songs_features()
