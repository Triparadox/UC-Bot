import os
import time
import typing
import random
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy system is online.")
        time.sleep(0.25)
    
    @commands.command(pass_context = True)
    async def balance(self, ctx):
        #Establishing MongoDB connection
        password = os.environ['MongoDB']
        mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]
        await ctx.send('Your balance is $0')
    
    @commands.command(pass_context = True)
    async def daily(self, ctx):
        #Establishing MongoDB connection
        password = os.environ['MongoDB']
        mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]
        currency_symbol = discord.utils.get(self.client.emojis, name='Cash')
        gain = random.randrange(1,5)
        outputMsg = 'You earned {0} {1} today! Check in again tomorrow for more.'.format(gain, currency_symbol)
        await ctx.send(outputMsg)


def setup(client):
    client.add_cog(Economy(client))