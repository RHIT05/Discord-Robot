import json
import asyncio
import sqlite3

import discord
from discord.ext import commands
from discord.ext.commands.errors import *
import time

DB = 'AudreyAnnouncement.db'


# spin off of permissions that makes announcements at time given in RoBot.py

class AudreyAnnouncement(commands.Cog):

    def __init__(self, client):
        client.permission_authority = self
        self.client = client
        self.cwd = client.config['Bot']['modules_dir'] + 'AudreyAnnouncement/'
        conn = sqlite3.connect(self.cwd + DB)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS announcements(server int, channel int, announcement text)')
        conn.commit()
        conn.close()

    @commands.command(help='Clears the announcements of this server')
    async def clearannounce(self, context):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            conn = sqlite3.connect(self.cwd + DB)
            server = context.message.guild
            c = conn.cursor()
            c.execute('DELETE FROM announcements WHERE server=?', (server,))
            conn.commit()
            conn.close()
            await context.send(f'Announcements cleared for {server.name}.')
        else:
            await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')

    @commands.command(help="list this server's current announcements")
    async def listannounce(self, context):
        conn = sqlite3.connect(self.cwd + DB)
        c = conn.cursor()
        results = c.execute('SELECT announcement FROM announcements WHERE server=?', (context.message.guild,)).fetchall()
        announcements = [''.join(row) for row in results]
        announce_string = '\n'.join(announcements)
        await context.send(
            f'Here are your current announcements for , {context.message.guild.name}\n```\n{announce_string}\n```')
        conn.close()

    @commands.command(help='Adds announcement to a server')
    async def addannounce(self, context, announcement, channel: discord.channel):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            conn = sqlite3.connect(self.cwd + DB)
            c = conn.cursor()
            if not channel:
                channel = discord.utils.find(lambda c: "announce" in c.name or "reminder" in c.name,
                                             context.message.guild.channels)
            c.execute('INSERT INTO announcements(server, channel, announcement) VALUES (?, ?, ?)',
                      (context.message.guild.id, channel.id, announcement))
            conn.commit()
            conn.close()
            await context.send(f'Will now announce \'{announcement}\' in {channel}.')
        else:
            await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


def setup(client):
    client.add_cog(AudreyAnnouncement(client))
