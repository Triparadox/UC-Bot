import os
import time
import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient

#Database variables and connections
#mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
#cluster = MongoClient(mongodb_database_url)
#levelling = cluster["discord"]["level"]

#Discord channel IDs
bot_spam = 735955534192312356

class Level(commands.Cog):

    def __init__(self, client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Level system is online.")
        time.sleep(0.25)

    
    @commands.Cog.listener()
    async def on_message(self, message):
        #Establishing MongoDB connection
        password = os.environ['MongoDB']
        mongodb_database_url = "mongodb+srv://triparadox:" + password + "@cluster.l7sui.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        cluster = MongoClient(mongodb_database_url)
        db = cluster["UCBot"]
        collection = db["database"]

        #Obtaining information: author, length of message, and user name
        author_id = message.author.id
        msg_length = len(message.content)
        author_name = message.author.name

        #Calculating XP generated from message
        xp_generated = int(msg_length / 10)
        if xp_generated < 1:
            xp_generated = 1
        elif xp_generated > 30:
            xp_generated = 30;

        #Looking up author's database profile
        userData = collection.find_one({"user_id": author_id})
        #UserData exists
        if(userData):
            collection.update_one({"user_id":author_id}, {"$inc":{"user_xp":xp_generated}})
            collection.update_one({"user_id":author_id}, {"$set":{"user_name":author_name}})
        #UserData does not exist
        else:
            collection.insert_one({"user_id":author_id, "user_name":author_name, "user_xp":xp_generated})
        

def setup(client):
    client.add_cog(Level(client))