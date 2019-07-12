#!/usr/bin/python3.6
import configparser
import random
import os
import sys
import time
import logging
import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import *


config = configparser.RawConfigParser()
config.read('config.ini')
games = config.get('Bot', 'games').splitlines()

client = commands.Bot(command_prefix=config.get('Bot', 'prefix'))
client.start_time = time.time()
client.config = config


@tasks.loop(seconds=3600)
async def status_task():
    await client.change_presence(activity=discord.Game(random.choice(games)))


@client.event
async def on_ready():
    status_task.start()
    print('Bot is ready')


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')


@client.event
async def on_command_error(context, error):
    if isinstance(error, CommandNotFound):
        name = config.get('Admin', 'name')
        account = config.get('Admin', 'mention')
        email = config.get('Admin', 'email')
        await context.send(
            f'That is not one of my commands :pensive: . '
            f'If you would like to see this command please contact my Human or type \'.request <command description>\'.\n'
            f'```Name: {name}\nAccount: {account}\nEmail: {email}```')


@client.command()
async def request(context, *, request):
    user = client.get_user(int(config.get('Admin', 'id')))
    await user.send(f'FEATURE REQUEST: {request}')


@client.command()
async def load(context, extension):
    mod_role = config.get('Bot', 'mod_role')
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        print(f'Loading extension {extension}.')
        try:
            client.load_extension(f'modules.{extension}.{extension}')
        except ExtensionNotFound:
            print(f'Extension \'{extension}\' not found.')
            await context.send('That extension doesn\'t seem to exist.')
            return
        await context.send(f'Extension \'{extension}\' loaded. Type \'.help {extension}\' for more information.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@client.command()
async def unload(context, extension):
    mod_role = config.get('Bot', 'mod_role')
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        print(f'Unloading extension {extension}.')
        try:
            client.unload_extension(f'modules.{extension}.{extension}')
        except ExtensionNotLoaded:
            print(f'Extension \'{extension}\' not loaded.')
            await context.send('That extension doesn\'t seem to be loaded.')
            return
        await context.send(f'Extension \'{extension}\' unloaded.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@client.command()
async def reload(context, extension):
    mod_role = config.get('Bot', 'mod_role')
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        print(f'Reloading extension {extension}.')
        try:
            client.unload_extension(f'modules.{extension}.{extension}')
        except ExtensionNotLoaded:
            print(f'Extension \'{extension}\' not loaded. Attempting to load.')
        try:
            client.load_extension(f'modules.{extension}.{extension}')
        except ExtensionNotFound:
            print(f'Extension \'{extension}\' not found.')
            await context.send('That extension doesn\'t seem to exist.')
            return
        await context.send(f'Extension \'{extension}\' reloaded. Type \'.help {extension}\' for more information.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@load.error
@unload.error
@reload.error
async def ext_error(context, error):
    if isinstance(error, MissingRequiredArgument):
        await context.send('Please specify an extension.')


for filename in os.listdir('./modules'):
    if True:
        print(f'Loading extension {filename}')
        client.load_extension(f'modules.{filename}.{filename}')


logger = logging.getLogger('discord')
level = logging.INFO
if len(sys.argv) == 2 and sys.argv[1] == '--debug':
    level = logging.DEBUG
logger.setLevel(level)
handler = logging.FileHandler(
    filename='robot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client.run(config.get('Bot', 'token'))
