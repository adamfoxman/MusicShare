import pylast
import os
import logging


class Lastfm:
    def __init__(self):
        self.api_key = os.environ.get('LASTFM_API_KEY')
        self.api_secret = os.environ.get('LASTFM_API_SECRET')
        self.network = pylast.LastFMNetwork(
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    def get_song_info(self, artist, track):
        try:
            song = self.network.get_track(artist, track)
            return {
                'artist': song.get_artist().get_name(),
                'track': song.get_name(),
                'album': song.get_album().get_name(),
                'image': song.get_cover_image(),
                'summary': song.get_wiki_summary(),
            }
        except Exception as e:
            print(e)
            logging.error(e)
            return None
