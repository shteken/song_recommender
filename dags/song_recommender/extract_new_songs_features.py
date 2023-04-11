from tools.extract_songs_features import extract_and_save_songs_features


PLAYLIST = "37i9dQZEVXbMDoHDwVN2tF"
FILE_PATH = f"music_database/new_songs_features/{PLAYLIST}.csv"

extract_and_save_songs_features(PLAYLIST, FILE_PATH)
