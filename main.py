import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import logging

debug_guild = [967448609677266944]

logging.basicConfig(
    filename="main.log",
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO
)


def main():
    logging.info("Starting...")
    bot = commands.Bot()
    bot.load_extension('cogs.share')

    try:
        @bot.event
        async def on_ready():
            logging.info(f"Logged in as {bot.user.name}")
            print(f"MusicShare bot started!\nUser: {bot.user}")
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print(f"Couldn't start MusicShare bot: {e}")
        logging.error(f"Couldn't start MusicShare bot: {e}")


if __name__ == '__main__':
    load_dotenv()
    main()
