from discord.ext import commands
import discord


class Share(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('amogus')

    @discord.slash_command(description='amogus')
    async def hello(self, ctx):
        await ctx.send('no siema!')
