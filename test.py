
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


PLAYLIST = "0L0b49nWbU309wZDIHqOHX"
LIMIT_SONGS_PER_REQUEST = 50
# extend to multiple playlists


total_songs_in_playlist = sp.playlist_tracks(playlist_id=PLAYLIST, fields="total")
total_songs_in_playlist = total_songs_in_playlist["total"]
number_of_pages_to_request = total_songs_in_playlist//LIMIT_SONGS_PER_REQUEST + 1

all_track_ids = []

for page_number in range(1, number_of_pages_to_request+1):
    tracks_in_page = sp.playlist_tracks(playlist_id=PLAYLIST, offset=(page_number-1)*LIMIT_SONGS_PER_REQUEST, limit=LIMIT_SONGS_PER_REQUEST, fields="items(track(id))")["items"]
    track_ids_in_page = [track_info["track"]["id"] for track_info in tracks_in_page]
    all_track_ids.extend(track_ids_in_page)

print(all_track_ids)
print(len(all_track_ids))
