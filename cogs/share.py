import os

from nextcord.ext import commands
import nextcord
import logging
from api.getter import Getter
from api.embeds import (
    generate_lite_embed,
    generate_embed,
)

debug_guild = list(map(int, os.getenv("DEBUG_GUILDS").split(",")))


class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.getter = Getter()

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
        logging.info(f"{interaction.user.name} is sharing {song_link}")
        try:
            artist, title, cover_art, song_info, links = self.getter.get_song_info(song_link)
        except Exception as e:
            await interaction.send(f"Error: {e}")
            raise e
        if len(links) == 0:
            await interaction.send(embed=generate_lite_embed(artist, title, cover_art, song_link))
            return
        await interaction.send(embed=generate_embed(artist, title, cover_art, song_info, links))


def setup(bot):
    print("Loading share.py cog")
    logging.info("Loading share.py cog")
    bot.add_cog(Share(bot))
