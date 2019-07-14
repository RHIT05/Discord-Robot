import asyncio
import urllib.request
import urllib.parse
import re
import youtube_dl
import discord
from discord.ext import commands, tasks


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.vcs = {}
        self.songs = asyncio.Queue()
        self.play_next = asyncio.Event()
        self.ydl_opts = {'format': 'bestaudio/best',
                         'postprocessors': [
                             {'key': 'FFmpegExtractAudio',
                                 'preferredcodec': 'mp3',
                                 'preferredquality': '192'
                              }
                         ]
                         }

    async def search(self, query):
        query_string = urllib.parse.urlencode({'search_query': query})
        html_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(
            'href=\\"\\/watch\\?v=(.{11})', html_content.read().decode())
        return 'http://www.youtube.com/watch?v=' + search_results[0]

    async def queue_url(self, context, url):
        self.songs.put(url)
        await context.send(f"Queuing {url}")
        if not self.vcs[context.guild.id].is_playing():
            await self.play_url(context, self.songs.get())

    async def play_url(self, context, url):
        self.ydl_opts['outtmpl'] = f"/tmp/robot_{url}.mp3"
        with youtube_dl.YoutubeDL(self.ydl_opts) as (ydl):
            ydl.download([url])
            self.vcs[context.guild.id].play(
                discord.FFmpegPCMAudio(f"/tmp/robot_{url}.mp3"))

    @commands.command()
    async def summon(self, context):
        channel = context.message.author.voice.channel
        server = context.guild.id
        if server in self.vcs:
            if self.vcs[server].channel.id != channel.id:
                await self.vcs[server].disconnect()
                self.vcs[context.guild.id] = await(channel.connect())
        if server not in self.vcs:
            self.vcs[context.guild.id] = await(channel.connect())

    @commands.command()
    async def leave(self, context):
        channel = context.message.author.voice.channel
        server = context.guild.id
        if server in self.vcs:
            if self.vcs[server].channel.id == channel.id:
                await self.vcs[server].disconnect()
                self.vcs.pop(server, None)

    @commands.command()
    async def play(self, context, *, request):
        if request[0:4].lower() == 'http':
            await self.play_url(context, request)
        else:
            url = await(self.search(request))
            await self.play_url(context, url)

    @commands.command()
    async def pause(self, context):
        if context.guild.id in self.vcs:
            self.vcs[context.guild.id].pause()

    @commands.command()
    async def resume(self, context):
        if context.guild.id in self.vcs:
            self.vcs[context.guild.id].resume()

    @commands.command()
    async def stop(self, context):
        if context.guild.id in self.vcs:
            self.vcs[context.guild.id].stop()


def setup(client):
    client.add_cog(Music(client))
