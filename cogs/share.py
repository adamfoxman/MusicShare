from nextcord.ext import commands
import nextcord

debug_guild = [967448609677266944]


class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        guild_ids=debug_guild
    )
    async def hello(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(
            title="Hello",
            description="Hello, world!",
            color=0x00FF00
        )
        await interaction.send(embed=embed)


def setup(bot):
    print("Loading share.py...")
    bot.add_cog(Share(bot))