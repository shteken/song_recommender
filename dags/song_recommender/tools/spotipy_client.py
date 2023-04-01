import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


LIMIT_SONGS_PER_REQUEST = 50
LIMIT_SONGS_PER_REQUEST_FOR_FEATURES = 100


def send_requests_to_spotify(api_call, total_number_of_items, limit_items_per_request):
    all_responses = []
    total_number_of_requests = total_number_of_items // limit_items_per_request + 1
    for request_number in range(1, total_number_of_requests+1):
        response = api_call(request_number, limit_items_per_request)
        all_responses.extend(response)
    return all_responses
