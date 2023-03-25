from pathlib import Path
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


PLAYLIST = "0L0b49nWbU309wZDIHqOHX"
LIMIT_SONGS_PER_REQUEST = 50
LIMIT_SONGS_PER_REQUEST_FOR_FEATURES = 100
# extend to multiple playlists

# get features from current lists
total_songs_in_playlist = sp.playlist_tracks(playlist_id=PLAYLIST, fields="total")
total_songs_in_playlist = total_songs_in_playlist["total"]
number_of_pages_to_request = total_songs_in_playlist//LIMIT_SONGS_PER_REQUEST + 1

all_track_ids = []

for page_number in range(1, number_of_pages_to_request+1):
    tracks_in_page = sp.playlist_tracks(playlist_id=PLAYLIST, offset=(page_number-1)*LIMIT_SONGS_PER_REQUEST, limit=LIMIT_SONGS_PER_REQUEST, fields="items(track(id))")["items"]
    track_ids_in_page = [track_info["track"]["id"] for track_info in tracks_in_page]
    all_track_ids.extend(track_ids_in_page)

# print(all_track_ids)
print(len(all_track_ids))

number_of_requests = total_songs_in_playlist//LIMIT_SONGS_PER_REQUEST_FOR_FEATURES + 1

# columns = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']
# songs_features = pd.DataFrame(columns=columns)
features_by_request = []
for song_group in range(1, number_of_requests+1):
    start_song = (song_group-1)*LIMIT_SONGS_PER_REQUEST_FOR_FEATURES
    end_song = song_group * LIMIT_SONGS_PER_REQUEST_FOR_FEATURES
    songs_features = sp.audio_features(all_track_ids[start_song:end_song])
    features_by_request.extend(songs_features)
all_songs_features = pd.DataFrame(features_by_request)
print(all_songs_features.describe(include="all"))
print(all_songs_features)


filepath = Path.home() / "music_database" / "features_songs_from_list" / "data.csv"
filepath.parent.mkdir(parents=True, exist_ok=True)
all_songs_features.to_csv(filepath)

# get features from new releases
# first need to create functions from the previous code and reuse them here
