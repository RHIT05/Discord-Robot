import random
import discord
from discord.ext import commands
from discord.ext.commands.errors import *


class Minigames(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='8ball')
    async def _8ball(self, context, *, question):
        responses = ['It is certain.',
                     'As I see it, yes.',
                     'It is decidedly so.',
                     'Most likely.',
                     'Without a doubt.',
                     'Outlook good.',
                     'Yes - definitely.',
                     'Yes.',
                     'You may rely on it.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Connot predict now.',
                     'Concentrate and ask again.',
                     "Don't count on it.",
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await context.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @_8ball.error
    async def _8ball_error(self, context, error):
        if isinstance(error, MissingRequiredArgument):
            await context.send('You need to ask me a question.')


def setup(client):
    client.add_cog(Minigames(client))
