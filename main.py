import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from cogs.share import Share


def main():
    bot = discord.Bot()
    try:
        @bot.event
        async def on_ready():
            print(f"MusicShare bot started!\nUser: {bot.user}")
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Couldn't start MusicShare bot: {e}")
    bot.add_cog(Share(bot))


if __name__ == '__main__':
    load_dotenv()
    main()
