# Importing modules
import discord
from discord.ext import commands
from database_manager import database_manager

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Economy system is online.')

    # Give daily bonus check-in to user
    @commands.command(pass_context=True)
    async def daily(self, ctx):
        # Obtain user data
        author_id = ctx.author.id
        db = database_manager.get_database_manager()
        return_data = db.daily_bonus(author_id)

        status_code, amount = return_data

        match status_code:
            case 1:
                # Inform user the amount he has been rewarded
                await ctx.send(f'You have been awarded {amount} pts!')
                pass
            case 0:
                # Inform user daily bonus is granted once a day
                await ctx.send('You may only claim daily bonus once a day.')

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        # Obtain user data
        author_id = ctx.author.id
        db = database_manager.get_database_manager()
        query_result = db.get_balance(author_id)
        account_balance, = query_result

        # Obtain currency symbol
        currency = discord.utils.get(self.client.emojis, name='Cash')

        # Create embed message
        balance_info = discord.Embed(title=f'{ctx.author.name}\'s Wallet',
                                     color=0x97FEEF)
        balance_info.set_thumbnail(url=ctx.author.avatar)
        balance_info.add_field(name=f'Balance:\t{account_balance} {currency}',
                               value=f'\u200b')
        await ctx.send(embed=balance_info)

async def setup(client):
    await client.add_cog(Economy(client))