from functools import partial
from pathlib import Path
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


PLAYLIST = "0L0b49nWbU309wZDIHqOHX"
LIMIT_SONGS_PER_REQUEST = 50
LIMIT_SONGS_PER_REQUEST_FOR_FEATURES = 100
FILE_PATH = "music_database/features_songs_from_list/data.csv"
total_songs_in_playlist = sp.playlist_tracks(playlist_id=PLAYLIST, fields="total")["total"]

def send_requests_to_spotify(api_call, total_number_of_items, limit_items_per_request):
    all_responses = []
    total_number_of_requests = total_number_of_items // limit_items_per_request + 1
    for request_number in range(1, total_number_of_requests+1):
        response = api_call(request_number, limit_items_per_request)
        all_responses.extend(response)
    return all_responses

def playlist_tracks_spotipy(request_number, limit_items_per_request):
    tracks_in_page = sp.playlist_tracks(playlist_id=PLAYLIST, offset=(request_number-1)*limit_items_per_request, limit=limit_items_per_request, fields="items(track(id))")["items"]
    track_ids_in_page = [track_info["track"]["id"] for track_info in tracks_in_page]
    return track_ids_in_page

def audio_features_spotipy(tracks_ids, request_number, limit_items_per_request):
    songs_features = sp.audio_features(tracks_ids[(request_number-1)*limit_items_per_request:request_number * limit_items_per_request])
    return songs_features

def transform_features_into_df(songs_features):
    return pd.DataFrame(songs_features)

def save_features_in_file(songs_features):
    filepath = Path.home() / FILE_PATH
    filepath.parent.mkdir(parents=True, exist_ok=True)
    songs_features.to_csv(filepath) 


songs_to_analyze = send_requests_to_spotify(playlist_tracks_spotipy, total_songs_in_playlist, LIMIT_SONGS_PER_REQUEST)

partial_audio_features_spotipy = partial(audio_features_spotipy, songs_to_analyze)

songs_features = send_requests_to_spotify(partial_audio_features_spotipy, total_songs_in_playlist, LIMIT_SONGS_PER_REQUEST_FOR_FEATURES)

songs_features_df = transform_features_into_df(songs_features)

save_features_in_file(songs_features_df)

# create classes for the process
# get features from new releases
