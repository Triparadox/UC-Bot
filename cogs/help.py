import time
import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help system is online.")
        time.sleep(0.25)

    @commands.command(pass_context = True)
    async def help(self, ctx):
        HelpGuide = discord.Embed(title = 'Help Page' + '\n\u200b', color = discord.Color.orange())
        HelpGuide.add_field(name = '$poll', value = 'This command does not take any parameter. This command creates a poll after interacting with user.', inline = False)
        HelpGuide.add_field(name = '$weather', value = 'This command takes one location parameter and returns the weather information.', inline = False)
        HelpGuide.add_field(name = '$balance', value = 'This command will check user\'s server point accumulated through various means. It is currently a work in progress.', inline = False)
        HelpGuide.add_field(name = '$daily', value = 'This command will grant a user small amount of server point once every day. It is currently a work in progress.', inline = False)

        await ctx.send(embed = HelpGuide)


def setup(client):
    client.add_cog(Help(client))