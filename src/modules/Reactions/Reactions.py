import json
import discord
from discord.ext import commands
from discord.ext.commands.errors import *


class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rules = {}
        # Load config
        with open('modules/Reactions/config.json', 'r') as f:
            self.rules = json.load(f)

    @commands.command(help='Creates new reaction for DfBot to use')
    async def react(self, context, phrase, reaction):
        p = phrase.replace('_', ' ')
        r = reaction.replace('_', ' ')
        self.rules[p.lower()] = r
        await context.send(f'Reacting to \'{p}\' with \'{r}\' starting... Now!')
        self.save()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "df.react" in message.content.lower():
            return
        sent_message = message.content.lower()
        for trigger in self.rules:
            if trigger in sent_message:
                key = trigger
                a = sent_message.find(key)
                b = a + len(key)
                # print(a, b, key, len(sent_message))
                if a > 0:
                    if sent_message[a-1].isalpha():
                        break
                if b < len(sent_message):
                    if sent_message[b].isalpha():
                        break
                    # key = message.content.lower()
                if key in self.rules:
                    context = await self.client.get_context(message)
                    await context.send(self.rules[key])
                    break

    def save(self):
        storage = self.rules
        with open('modules/Reactions/config.json', 'w+') as f2:
            json.dump(storage, f2)
        with open('modules/Reactions/config.json', 'r') as f:
            self.rules = json.load(f)


def setup(client):
    client.add_cog(Reactions(client))
