from tools.extract_songs_features import extract_and_save_songs_features


PLAYLIST = "0L0b49nWbU309wZDIHqOHX"
FILE_PATH = f"music_database/liked_songs_features/{PLAYLIST}.csv"

extract_and_save_songs_features(PLAYLIST, FILE_PATH)
