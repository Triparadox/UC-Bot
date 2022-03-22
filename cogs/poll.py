import time
import discord
from discord.ext import commands

class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Poll system is online.")
        time.sleep(0.25)

    @commands.command(pass_context = True)
    async def poll(self, ctx):
        #The author of the command.
        author = ctx.author
        avatar_url = str(ctx.author.avatar_url)
        #Method to make sure the bot only recognizes the same user during the interaction.
        def checkAuthor(m):
            return m.author == author

        #Method to print the poll options.
        def printMethod(option_content):
            sentence = ''
            i = 1
            for x in option_content:
                sentence = sentence + str(i) + ')\t' + x + '\n'
                i = i + 1
            return sentence
        #Message record array for deletion.
        msg_history = []
        
        msg_history.append(ctx.message)

        #Getting poll title.
        titleRequest = await ctx.send('Please enter the title of the poll:')
        msg_history.append(titleRequest)
        titleAnswer = await self.client.wait_for('message', timeout = 60.0, check = checkAuthor)
        msg_history.append(titleAnswer)
        poll_title = titleAnswer.content

        #Getting poll content.
        pollContentRequest = await ctx.send('Please enter the content of the poll: ')
        msg_history.append(pollContentRequest)
        pollContentAnswer = await self.client.wait_for('message', timeout = 60.0, check = checkAuthor)
        poll_content = pollContentAnswer.content
        msg_history.append(pollContentAnswer)

        #Getting number of options (max is 9).
        optionCountRequest = await ctx.send('Please send how many options there will be (2 to 9 only):')
        msg_history.append(optionCountRequest)
        optionCountAnswer = await self.client.wait_for('message', timeout = 60.0, check = checkAuthor)
        msg_history.append(optionCountAnswer)
        try:
            num = int(optionCountAnswer.content)
            if(num < 1 or num > 9):
                await ctx.send('It needs to be between 2 to 9.')
        except:
            await ctx.send('It needs to be a number between 2 to 9.')
            return
        option_count = int(optionCountAnswer.content)

        #Getting each option description.
        option_description = []
        option_symbol = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        i = 0
        while(i < option_count):
            optionDescriptionRequest = await ctx.send('Please enter the content of option #{0}'.format(str(i+1)))
            msg_history.append(optionDescriptionRequest)
            optionDescriptionAnswer = await self.client.wait_for('message', timeout = 60.0, check = checkAuthor)
            option_description.append(optionDescriptionAnswer.content)
            msg_history.append(optionDescriptionAnswer)
            i = i + 1

        #Composing embed for poll.
        PollMsg = discord.Embed(title = '__{0} by {1}__'.format(poll_title, str(author)[:-5]), description = '', color = 0x97FEEF)
        PollMsg.set_thumbnail(url=str(avatar_url))
        PollMsg.add_field(name = '\u200b', value = '{0}'.format(poll_content), inline = False)
        PollMsg.add_field(name = '\u200b', value = '{0}'.format(printMethod(option_description)), inline = False)
        poll_msg = await ctx.send(embed = PollMsg)

        #Adding emoji to the poll.
        i = 0
        while(i < option_count):
            await poll_msg.add_reaction('{0}'.format(option_symbol[i]))
            i = i + 1

        #Deleting all conversation history.
        i = 0
        while (i < len(msg_history)):
            await msg_history[i].delete()
            i = i + 1
        print('Messages deleted.')

def setup(client):
    client.add_cog(Poll(client))