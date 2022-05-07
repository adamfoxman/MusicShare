import requests
import logging

platforms = [
    'spotify',
    'itunes',
    'youtube',
    'deezer',
    'soundcloud',
    'appleMusic',
    'amazonStore',
    'amazonMusic',
    'googleStore',
    'tidal',
    'youtubeMusic'
]


class SongLink():
    def __init__(self, key: str = None):
        self.key = key

    def get_song(self, song_link: str):
        """
        Get the song from the song link
        :param song_link:
        :return:
        """
        response = self._get_from_api(song_link)
        links = self._get_song_links(response)
        artist, title, cover_art = self._get_song_info(response)
        return artist, title, cover_art, links

    def _get_from_api(self, song_link: str) -> dict:
        if self.key is None:
            logging.info('No token provided - using API without token')

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/80.0.3987.149 Safari/537.36 "
        }

        url = f"https://api.song.link/v1-alpha.1/links?url={song_link}&userCountry=PL"
        if self.key is not None:
            url = f"{url}&key={self.key}"

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ValueError("Invalid song link")

        return response.json()

    def _get_song_info(self, response: dict):
        """
        Get the song info from the song link
        :param song_link:
        :return:
        """
        entity_unique_id = response['entityUniqueId']
        artist = response['entitiesByUniqueId'][entity_unique_id]['artistName']
        title = response['entitiesByUniqueId'][entity_unique_id]['title']
        cover_art = response['entitiesByUniqueId'][entity_unique_id]['thumbnailUrl']
        return artist, title, cover_art


    def _get_song_links(self, response: dict) -> dict:
        """
        Get the song links from the song link
        :param song_link: The song link
        :return: The song links
        """

        links = {}
        for platform in platforms:
            if platform in response["linksByPlatform"] \
                    and response["linksByPlatform"][platform]["url"] is not None:
                links[platform] = response["linksByPlatform"][platform]["url"]

        return links

