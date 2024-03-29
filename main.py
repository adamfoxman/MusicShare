import os
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename="main.log",
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO
)


def main():
    logging.info("Starting...")
    intents = nextcord.Intents().all()
    bot = commands.Bot(intents=intents)
    bot.load_extension('cogs.share')
    bot.load_extension('cogs.spotify')

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
