import time
import datetime
import discord
from discord.ext import commands


class Utilities(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, context):
        await context.send(f":ping_pong:Pong! **{round(self.client.latency * 1000)}ms**")

    @commands.command()
    async def uptime(self, context):
        s = time.time() - self.client.start_time
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        await context.send(f"Uptime: {round(d)} days, {round(h)} hours, {round(m)} minutes, and {round(s)} seconds.")

    @commands.command()
    async def id(self, context):
        await context.send(f"Your id is {context.message.author.id} {context.message.author.mention}")


def setup(client):
    client.add_cog(Utilities(client))
