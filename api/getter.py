from api.services.songlink import SongLink


class Getter:
    def __init__(self):
        self.songlink = SongLink()

    def get_song_info(self, song_url: str) -> (str, str, str, dict):
        artist, title, cover_art, links = self.songlink.get_song(song_url)
        return artist, title, cover_art, links
