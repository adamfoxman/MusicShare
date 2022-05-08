from api.services.songlink import SongLink
from api.services.lastfm import Lastfm


class Getter:
    def __init__(self):
        self.songlink = SongLink()
        self.lastfm = Lastfm()

    def get_song_info(self, song_url: str) -> (str, str, str, dict, dict):
        artist, title, cover_art, links = self.songlink.get_song(song_url)
        song_info = self.lastfm.get_song_info(artist, title)
        return artist, title, cover_art, song_info, links
