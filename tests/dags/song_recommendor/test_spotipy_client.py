import pytest
from unittest.mock import Mock, call

from song_recommender.dags.song_recommender.tools.spotipy_client import send_requests_to_spotify

@pytest.fixture
def total_number_of_items():
    return 42

@pytest.fixture
def limit_items_per_request():
    return 10


def test_send_requests_to_spotify(total_number_of_items, limit_items_per_request):
    api_call = Mock(return_value={'key':'value'})
    send_requests_to_spotify(api_call, total_number_of_items, limit_items_per_request)
    api_call.assert_has_calls(calls =[call(1, 10), call(2, 10), call(3, 10), call(4, 10), call(5, 10)])
