import os
import time
from datetime import datetime
import typing
import random
import discord
from discord.ext import commands
from discord.ext import tasks
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

        #Currency symbol
        currency_symbol = discord.utils.get(self.client.emojis, name='Cash')

        #Looking up author's database profile
        author_id = ctx.author.id
        
        #user_point = false
        if(collection.find({"user_id": author_id}, {"user_daily_time": {"$exist": True}}) is False):
            collection.update_one({"user_id": author_id}, {"$set": {"user_point": 0}}, False, True)
            userData = collection.find({"user_id": author_id})
            point_balance = userData["user_point"]
            outputMsg = "Available balance: {0}{1}".format(point_balance, currency_symbol)
            await ctx.send(outputMsg)
        #user_point = true
        else:
            userData = collection.find({"user_id": author_id})
            point_balance = userData["user_point"]
            outputMsg = "Available balance: {0}{1}".format(point_balance, currency_symbol)
            await ctx.send(outputMsg)
    
    @commands.command(pass_context = True)
    async def daily(self, ctx):
        #Establishing MongoDB connection
        password = os.environ['MongoDB']
        mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]

        #Currency symbol
        currency_symbol = discord.utils.get(self.client.emojis, name='Cash')

        #Earning daily reward
        gain = random.randrange(1,5)

        #Generating current time for validity
        currentTime = datetime.now()
        currentDay = currentTime.day
        currentMonth = currentTime.month
        currentYear = currentTime.year
        currentDay = str(currentDay)
        currentMonth = str(currentMonth)
        currentYear = str(currentYear)
        currentTime = str(currentDay + currentMonth + currentYear)

        #Looking up author's database profile
        author_id = ctx.author.id
        
        #user_profile = false
        if (collection.find({"user_id": author_id}) is False):
            userData = {"user_id": author_id, "user_point": gain, "user_daily_time": currentTime}
            collection.insert_one(userData)
            outputMsg = 'You have been awarded {0}.'.format(gain, currency_symbol)
            await ctx.send(outputMsg)
        #user_profile = true
        else:
            #user_daily_time = false
            if(collection.find({"user_id": author_id}, {"user_daily_time": {"$exist": True}}) is False):
                #user_point = false
                if(collection.find({"user_id": author_id}, {"user_point": {"$exist": True}}) is False):
                    collection.update_one({"user_id": author_id}, {"$set": {"user_point": gain}}, False, True)
                    collection.update_one({"user_id": author_id}, {"$set": {"user_daily_time": currentTime}}, False, True)
                    outputMsg = 'You have been awarded {0} {1}.'.format(gain, currency_symbol)
                    await ctx.send(outputMsg)
                    await ctx.send("Here again")
                #user_point = true
                else:
                    collection.update_one({"user_id": author_id}, {"$inc": {"user_point": gain}}, False, True)
                    collection.update_one({"user_id": author_id}, {"$set": {"user_daily_time": currentTime}}, False, True)
            #user_daily_time = true
            else:
                #User has claimed daily reward recently. Reward is not generated
                if(collection.find({"user_id": author_id}, {"user_daily_time": currentTime})):
                    await ctx.send("You may only claim reward once every day.")
                #User has not claimed daily reward recently. Reward is generated
                else:
                    collection.update_one({"user_id": author_id}, {"$inc": {"user_point": gain}})
                    collection.update_one({"user_id": author_id}, {"$set": {"user_daily_time": currentTime}}, False, True)
                    outputMsg = 'You have been awarded {0} {1}.'.format(gain, currency_symbol)
                    await ctx.send(outputMsg)


def setup(client):
    client.add_cog(Economy(client))