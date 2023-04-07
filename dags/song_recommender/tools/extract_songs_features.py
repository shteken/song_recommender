from functools import partial
from pathlib import Path
import pandas as pd
from tools.spotipy_client import sp, LIMIT_SONGS_PER_REQUEST, LIMIT_SONGS_PER_REQUEST_FOR_FEATURES, send_requests_to_spotify


def extract_and_save_songs_features(playlist, output_file_path):
    number_of_songs = get_number_of_songs(playlist)
    get_songs_to_analyze_partial = partial(get_playlist_songs, playlist)
    songs_to_analyze = send_requests_to_spotify(get_songs_to_analyze_partial, number_of_songs, LIMIT_SONGS_PER_REQUEST)
    get_songs_features_partial = partial(get_songs_features, songs_to_analyze)
    songs_features = send_requests_to_spotify(get_songs_features_partial, number_of_songs, LIMIT_SONGS_PER_REQUEST_FOR_FEATURES)
    songs_features_df = transform_features_into_df(songs_features)
    save_features_in_file(songs_features_df, output_file_path)

def get_number_of_songs(playlist):
    return sp.playlist_tracks(playlist_id=playlist, fields="total")["total"]

def get_playlist_songs(playlist, request_number, limit_items_per_request):
    songs_in_page = sp.playlist_tracks(playlist_id=playlist, offset=(request_number-1)*limit_items_per_request, limit=limit_items_per_request, fields="items(track(id))")["items"]
    songs_ids_in_page = [song_info["track"]["id"] for song_info in songs_in_page]
    return songs_ids_in_page

def get_songs_features(songs_ids, request_number, limit_items_per_request):
    songs_features_in_page = sp.audio_features(songs_ids[(request_number-1)*limit_items_per_request:request_number * limit_items_per_request])
    return songs_features_in_page

def transform_features_into_df(songs_features):
    return pd.DataFrame(songs_features)

def save_features_in_file(songs_features, output_file_path):
    filepath = Path.home() / output_file_path
    filepath.parent.mkdir(parents=True, exist_ok=True)
    songs_features.to_csv(filepath) 
