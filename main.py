#UC Bot v.1.2.1
#Author: Triparadox C.
#Version changelog: Added user_name into database, and improved bot's Check Balance output using Discord Embed.


#Import important scripts and plugins
import os
import time
import json
import discord
from discord.ext import commands
import requests
import config
from config import *
import pymongo
from pymongo import MongoClient
import dns
import utils.json
from keep_alive import keep_alive


#Secret Environment Variables
bot_Token = os.environ['Bot Token']
password = os.environ['MongoDB']


#URLs
mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"


#Bot prefix and initialization
bot = commands.Bot(command_prefix = "$", intent = discord.Intents.all())
#Bot will ignore $help command to display custom help page instead
bot.remove_command('help')
#Bot cog files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


#Starting Discord Bot and loads all cog files
@bot.event
async def on_ready():
    print("UC Bot is starting...\n")

    #Checking connection to database
    try:
        print("Initializing database...")
        time.sleep(3)
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]
        print("Database connection is successful.\n")
    except:
        print("Failed connecting to database\nProceeding without database access...\n")
        time.sleep(5)

    finally:
        print("Now attempting to run all cog files under cogs directory...")
        time.sleep(3)


#Run Discord Bot
keep_alive()
bot.run(bot_Token)