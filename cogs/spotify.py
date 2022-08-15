import os

from nextcord import Member
from nextcord.ext import commands
import nextcord
import logging

from api.getter import Getter
from api.embeds import (
    generate_lite_embed,
    generate_embed,
)

debug_guild = list(map(int, os.getenv("DEBUG_GUILDS").split(",")))


def get_member(bot, guild_id: int, user_id: int):
    guild = bot.get_guild(guild_id)
    return guild.get_member(user_id)


def get_spotify_activity(member: Member):
    return next((activity for activity in member.activities if activity.type == nextcord.Spotify), None)


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.getter = Getter()

    @nextcord.slash_command(
        guild_ids=debug_guild,
        name="nowplaying",
        description="Get the current song playing on Spotify and share it with others"
    )
    async def nowplaying(self,
                         interaction: nextcord.Interaction
                         ):
        await interaction.response.defer()
        logging.info(f"{interaction.user.name} is sharing the now playing song")
        try:
            user = interaction.user
            if user.is_on_mobile():
                await interaction.send(
                    "Sorry, but this command is only available on desktop. "
                    "Mobile Discord does not share the Spotify data."
                )
                return
            member = get_member(self.bot, interaction.guild.id, user.id)
            spotify_activity = get_spotify_activity(member)
            if spotify_activity is None or not isinstance(spotify_activity, nextcord.Spotify):
                await interaction.send(
                    f"{user.name} is not listening to Spotify right now"
                )
                return
            song_link = spotify_activity.track_url
            artist, title, cover_art, song_info, links = self.getter.get_song_info(song_link)
            if len(links) == 0:
                await interaction.send(embed=generate_lite_embed(artist, title, cover_art, song_link))
                return
            await interaction.send(embed=generate_embed(artist, title, cover_art, song_info, links))
        except Exception as e:
            await interaction.send(f"{e}")
            raise e


def setup(bot):
    print("Loading spotify.py cog")
    logging.info("Loading spotify.py cog")
    bot.add_cog(Spotify(bot))
