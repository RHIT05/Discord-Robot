import json
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import time


# spin off of reactions that makes announcements on bercopolis server

class AudreyAnnouncement(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rules = {}
        # Load config
        with open('modules/AudreyAnnouncement/config.json', 'r') as f:
            self.rules = json.load(f)

    @commands.command(help='Creates new announcement for DfBot to make')
    async def announce(self, context, phrase):

        p = phrase.replace('_', ' ')
        server = context.message.guild
        channel = discord.utils.find(lambda c: "announce" in c.name or "reminder" in c.name, server.text_channels)
        self.rules[channel.name.lower()] = p
        if phrase == "":
            await context.send(f'No longer making an announcement in  \'{channel.guild.name}\'!')
        else:
            await context.send(f'Making announcement \'{p}\' in \'{channel.guild.name}\' starting at 7am EST tomorrow!')
        self.save()
        return


    def save(self):
        storage = self.rules
        with open('modules/AudreyAnnouncement/config.json', 'w+') as f2:
            json.dump(storage, f2)
        with open('modules/AudreyAnnouncement/config.json', 'r') as f:
            self.rules = json.load(f)


def setup(client):
    client.add_cog(AudreyAnnouncement(client))
