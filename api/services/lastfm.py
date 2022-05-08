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
            if song is not None:
                # get top 5 tags as strings
                tags = [tag.item.get_name() for tag in song.get_top_tags(limit=5) if tag is not None]
                return {
                    'artist': song.get_artist().get_name(),
                    'track': song.get_name(),
                    'album': song.get_album().get_name() if song.get_album() is not None else 'unknown album',
                    'tags': tags,
                    'image': song.get_cover_image() if song.get_cover_image() is not None else '',
                    'summary': song.get_wiki_summary() if song.get_wiki_summary() is not None else '',
                }
            else:
                return {
                    'artist': artist,
                    'track': track,
                    'album': 'unknown album',
                    'tags': [],
                    'image': '',
                    'summary': '',
                }
        except Exception as e:
            logging.error(e)
            return {
                'artist': artist,
                'track': track,
                'album': 'unknown album',
                'tags': [],
                'image': '',
                'summary': '',
            }
