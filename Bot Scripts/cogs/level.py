# Importing modules
import discord
from discord.ext import commands
from database_manager import database_manager

class Level(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Level system is online.')

    # Generate XP for a user when a message is sent
    @commands.Cog.listener()
    async def on_message(self, message):

        # Get message metadata
        author_id = message.author.id
        message_length = len(message.content)

        # Calculate earned XP
        xp_generated = self.calculate_xp(message_length)

        # Determine if there is XP generated or not
        if xp_generated >= 1:
            # Update the database
            db = database_manager.get_database_manager()
            db.increment_xp(account_id=author_id, xp_amount=xp_generated)
        else:
            # Skip
            pass

    # Get user profile and level data
    @commands.command(pass_context=True)
    async def rank(self, ctx):
        # Obtain user data
        author_id = ctx.author.id
        db = database_manager.get_database_manager()
        user_level, xp_progress, xp_requirement =db.check_level(author_id)

        # Create embed message
        profile_info = discord.Embed(title=f'{ctx.author.name}',
                                     color=0x97FEEF)
        profile_info.set_thumbnail(url=ctx.author.avatar)
        profile_info.add_field(name=f'Lv. {user_level}', value=f''
                                    f'{xp_progress}/{xp_requirement}')
        await ctx.send(embed=profile_info)

    # Static helper method to calculate xp generated
    @staticmethod
    def calculate_xp(message_length):
        xp_generated = message_length // 10
        return xp_generated


async def setup(client):
    await client.add_cog(Level(client))