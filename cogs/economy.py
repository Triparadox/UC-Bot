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

        #Author's Identity
        author_id = ctx.author.id
        
        #Currency symbol
        currency_symbol = discord.utils.get(self.client.emojis, name='Cash')

        #Looking up author's database profile
        userData = collection.find_one({"user_id": author_id})
        
        #UserData has user_point
        if "user_point" in userData:
            outputMsg = "You have {0} {1}".format(userData["user_point"], currency_symbol)
            await ctx.send(outputMsg)
        #UserData do not have user_point
        else:
            await ctx.send("You have nothing. Perhaps try using $daily command to earn some.")
            
    
    @commands.command(pass_context = True)
    async def daily(self, ctx):
        #Establishing MongoDB connection
        password = os.environ['MongoDB']
        mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]

        #Author's Identity
        author_id = ctx.author.id
        
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
        userData = collection.find_one({"user_id": author_id})
        #UserData exists
        if (userData):
            #UserData has user_point
            if "user_point" in userData:
                #UserData has user_daily_time
                if "user_daily_time" in userData:
                    #Request Denied: user has claimed reward today
                    
                    if(userData["user_daily_time"] == currentTime):
                        await ctx.send("You may only claim daily reward once per day.")
                    #Request Approved: user has not claimed reward today
                    else:
                        collection.update_one({"user_id": author_id}, {"$set":{"user_daily_time":currentTime}, "$inc":{"user_point":gain}})
                        outputMsg = "You have been granted {0} {1}.".format(gain, currency_symbol)
                        await ctx.send(outputMsg)
                #UserData does not have user_daily_time
                else:
                    collection.update_one({"user_id":author_id}, {"$set":{"user_daily_time":currentTime}, "$inc":{"user_point":gain}})
                    outputMsg = "You have been granted {0} {1}.".format(gain, currency_symbol)
                    await ctx.send(outputMsg)
            #UserData does not have user_point
            else:
                collection.update_one({"user_id":author_id}, {"$set":{"user_daily_time":currentTime}})
                collection.update_one({"user_id":author_id}, {"$set":{"user_point":gain}})
                outputMsg = "You have been granted {0} {1}.".format(gain, currency_symbol)
                await ctx.send(outputMsg)
        #UserData does not exist
        else:
            await ctx.send("Please send at least one message first.")
                

def setup(client):
    client.add_cog(Economy(client))