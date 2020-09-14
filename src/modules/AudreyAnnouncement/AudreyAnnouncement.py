import json
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
        server = context.message.guild()
        for channel in server.channels():
            if ("reminder" or "announcement") in channel.name():
                c = channel
                break
        self.rules[c.lower()] = p
        await context.send(f'Making announcement \'{p}\' in \'{c.guild.name()}\' starting... Now!')
        self.save()

    async def background_timer(self):
        await self.client.wait_until_ready()
        if time.gmtime()[3] == 0 and time.gmtime()[4] < 1 and time.gmtime == 0:
            for channel in self.rules:
                channel.send(self.rules[channel])

    def save(self):
        storage = self.rules
        with open('modules/AudreyAnnouncement/config.json', 'w+') as f2:
            json.dump(storage, f2)
        with open('modules/AudreyAnnouncement/config.json', 'r') as f:
            self.rules = json.load(f)


def setup(client):
    client.add_cog(AudreyAnnouncement(client))
