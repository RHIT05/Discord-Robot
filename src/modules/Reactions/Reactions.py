import json
import discord
from discord.ext import commands
from discord.ext.commands.errors import *


class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Load config
        with open('modules/Reactions/config.json', 'r') as f:
            self.rules = json.load(f)

    @commands.command(help='Creates new reaction for RoBot to use')
    async def react(self, context, phrase, reaction):
        p = phrase.replace('_', ' ')
        r = reaction.replace('_', ' ')
        self.rules[p.lower()] = r
        await context.send(f'I will now react to \'{p}\' with \'{r}\'')
        await context.send(f'json' + str(self.rules))

    @commands.Cog.listener()
    async def on_message(self, message):
        key = message.content.lower()
        if key in self.rules and not message.author.bot:
            context = await self.client.get_context(message)
            await context.send(self.rules[key])
        #dump json data to disk so rules are saved
        with open('modules/Reactions/config.json', 'w') as f:
            json.dump(self.rules, f)

def setup(client):
    client.add_cog(Reactions(client))
