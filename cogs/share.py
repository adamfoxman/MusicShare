from nextcord.ext import commands
import nextcord
import logging
from songlink.songlink import SongLink

debug_guild = [967448609677266944]

stream_platforms = {
    'spotify': 'Spotify',
    'deezer': 'Deezer',
    'soundcloud': 'SoundCloud',
    'appleMusic': 'Apple Music',
    'amazonMusic': 'Amazon Music',
    'tidal': 'Tidal',
    'youtubeMusic': 'YouTube Music',
}

buy_platforms = {
    'itunes': 'iTunes',
    'amazonStore': 'Amazon',
    'googleStore': 'Google Play Store',
}


class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.songlink = SongLink()

    @nextcord.slash_command(
        guild_ids=debug_guild,
        name="share",
        description="Share a song with your friends"
    )
    async def share(self,
                    interaction: nextcord.Interaction,
                    song_link: str = nextcord.SlashOption(description="Link to the song you want to share",
                                                          required=True)
                    ):
        await interaction.response.defer()
        try:
            artist, title, cover_art, links = self.songlink.get_song(song_link)
        except Exception as e:
            await interaction.send(f"Error: {e}")
            raise e
        if len(links) == 0:
            await interaction.send(embed=self._generate_lite_embed(artist, title, cover_art, song_link))
            return
        await interaction.send(embed=self._generate_embed(artist, title, cover_art, links))

    def _generate_lite_embed(self, artist: str, title: str, cover_art: str, url: str):
        embed = nextcord.Embed(
            title=f"{artist} - {title}",
            description=f"[Click here]({url}) to listen",
            color=0x00FF00
        )
        embed.set_thumbnail(url=cover_art)
        return embed

    def _generate_embed(self, artist: str, title: str, cover_art: str, links: dict):
        embed = nextcord.Embed(
            title=f"{artist} - {title}",
            description=f'Found {len(links)} links for this song',
            color=0x00FF00
        )
        embed.set_thumbnail(url=cover_art)
        for platform, link in links.items():
            if platform in stream_platforms:
                embed.add_field(name=stream_platforms[platform],
                                value=f"[Click here]({link}) to listen on {stream_platforms[platform]}",
                                inline=True)
            elif platform in buy_platforms:
                embed.add_field(name=buy_platforms[platform],
                                value=f"[Click here]({link}) to buy on {buy_platforms[platform]}",
                                inline=True)
            else:
                embed.add_field(name=platform.capitalize(),
                                value=f"[Click here]({link}) to watch on {platform.capitalize()}",
                                inline=True)

        return embed


def setup(bot):
    print("Loading share.py cog")
    logging.info("Loading share.py cog")
    bot.add_cog(Share(bot))