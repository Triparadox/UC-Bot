"""
UCBot version 2.0.0

A completely revamped UCBot script for self-host purposes. This is a bot
designed to serve UC Group Discord server.
"""
# Importing modules
import discord
from discord.ext import commands
import os
from database_manager import database_manager


# Starting bot scripts
print('Starting UCBot...')


# Secret variables
BOT_TOKEN = '****************************'


# Color constants
RED = "\033[1;31m"
BLUE = "\033[1;34m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


class UCBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)

    async def setup_hook(self) -> None:
        # Loads cog files
        print('\nLoading cog files...')
        for filename in os.listdir('.\\cogs'):
            file_name, file_extension = os.path.splitext(filename)
            if file_extension == '.py':
                await self.load_extension(f'cogs.{file_name}')
                print(f'{file_name} file has been loaded.')

        # Creating database manager object to establish connection
        print('\nConnecting to database...')
        try:
            db = database_manager.get_database_manager()
            print('Database connection successful.')
        except (TypeError, ConnectionError) as error:
            print(RED + 'Database connection failed.')
            print(RED + '\t' + str(error) + RESET)

    async def on_ready(self):
        print('\nUCBot is up and running.')


bot = UCBot()
bot.run(BOT_TOKEN)