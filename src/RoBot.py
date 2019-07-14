#!/usr/bin/python3.6
import json
import random
import os
import sys
import time
import logging
import asyncio
import discord
from discord.ext import commands, tasks
from discord.ext.commands.errors import *


# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Create discord client and initialize starting values
client = commands.Bot(command_prefix=config['Bot']['prefix'])
client.start_time = time.time()
client.config = config

"""
Below we define the most basic level of functionality for RoBot. This includes all built in
commands, errors, and tasks which cannot be removed. 
"""
@tasks.loop(seconds=3600)
async def status_task():
    await client.change_presence(activity=discord.Game(random.choice(config['Bot']['games'])))


@client.event
async def on_ready():
    status_task.start()
    print_head(f'Bot is ready')


@client.event
async def on_member_join(member):
    pass


@client.event
async def on_member_remove(member):
    pass


@client.event
async def on_command_error(context, error):
    if isinstance(error, CommandNotFound):
        name = config['Admin']['name']
        account = config['Admin']['mention']
        email = config['Admin']['email']
        await context.send(
            f'That is not one of my commands :pensive: . '
            f'If you would like to see this command please contact my Human or type \'.request <command description>\'.\n'
            f'```Name: {name}\nAccount: {account}\nEmail: {email}```')


@client.command()
async def request(context, *, request):
    user = client.get_user(int(config['Admin']['id']))
    await user.send(f'FEATURE REQUEST: {request}')


@client.command()
async def load(context, module):
    mod_role = config['Bot']['mod_role']
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        try:
            module = next(mod for mod in client.config['Modules'] if mod['name'] == module)
        except:
            print_head_warn(f'Attempted to load and could not find module {module}')
            await context.send('That module doesn\'t seem to exist.')
        try:
            load_module(module)
        except ExtensionNotFound:
            print_subhead_warn(f'Module {module["name"]} not found')
            await context.send('That module doesn\'t seem to exist.')
            return
        except ExtensionAlreadyLoaded:
            print_subhead(f'Module {module["name"]} already loaded')
            await context.send(f'Module \'{module["name"]}\' is already loaded.')
            return
        await context.send(f'Module \'{module["name"]}\' loaded. Type \'.help {module["name"]}\' for more information.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@client.command()
async def unload(context, module):
    mod_role = config['Bot']['mod_role']
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        try:
            module = next(mod for mod in client.config['Modules'] if mod['name'] == module)
        except:
            print_head_warn(f'Attempted to unload and could not find module {module}')
            await context.send('That module doesn\'t seem to exist.')
        try:
            dependant = unload_module(module)
            if dependant:
                print_subhead_warn(f'Module {module["name"]} not unloaded')
                await context.send(f'\'{dependant["name"]}\' depends on {module["name"]}, not unloading.')
                return
        except ExtensionNotLoaded:
            print_subhead_warn(f'Module \'{module["name"]}\' not loaded')
            await context.send('That module doesn\'t seem to be loaded.')
            return
        await context.send(f'Module \'{module["name"]}\' unloaded.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@client.command()
async def reload(context, module):
    mod_role = config['Bot']['mod_role']
    if mod_role in [role.name.lower() for role in context.message.author.roles]:
        try:
            module = next(mod for mod in client.config['Modules'] if mod['name'] == module)
        except:
            print_head_warn(f'Attempted to reload and could not find module {module}')
            await context.send('That module doesn\'t seem to exist.')
        try:
            unload_module(module, force=True)
        except ExtensionNotLoaded:
            print_subhead_warn(f'Module \'{module["name"]}\' not loaded. Attempting to load.')
        try:
            load_module(module)
        except ExtensionNotFound:
            print_subhead_warn(f'Module \'{module["name"]}\' not found.')
            await context.send('That module doesn\'t seem to exist.')
            return
        await context.send(f'Module \'{module["name"]}\' reloaded. Type \'.help {module["name"]}\' for more information.')
    else:
        await context.send(f'You do not have permission to do that. Ask for the role {mod_role}.')


@load.error
@unload.error
@reload.error
async def ext_error(context, error):
    if isinstance(error, MissingRequiredArgument):
        await context.send('Please specify an module.')


def load_module(module):
    print_head(f'Loading module {module["name"]}')

    # Load any unloaded dependencies
    for dependency_name in module['depends']:
        print_subhead(f'Loading dependencies for {module["name"]}')
        dependency = next(mod for mod in client.config['Modules'] if mod['name'] == dependency_name)
        print_subhead(f'Loading dependency {dependency["name"]}')
        try:
            client.load_extension(f'modules.{dependency["load_with"]}')
            print_subhead(f'Dependency {dependency["name"]} loaded')
        except ExtensionAlreadyLoaded:
            print_subhead(f'Dependency {dependency["name"]} already loaded')

    client.load_extension(f'modules.{module["load_with"]}')
    print_subhead(f'Module {module["name"]} loaded')


def unload_module(module, force=False):
    print_head(f'Unloading module {module["name"]}')
    dependant = next((mod for mod in client.config['Modules'] if module['name'] in mod['depends']), False)
    if dependant and not force:
        print_subhead_warn(f'Module {dependant["name"]} depends on {module["name"]}')
        return dependant
    client.unload_extension(f'modules.{module["load_with"]}')
    print_subhead(f'Module {module["name"]} unloaded')
    return False


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_head(text):
    print(f'{bcolors.HEADER}{text}{bcolors.ENDC}')


def print_subhead(text):
    print(f'{bcolors.OKGREEN}--> {text}{bcolors.ENDC}')


def print_head_warn(text):
    print(f'{bcolors.WARNING}{text}{bcolors.ENDC}')


def print_subhead_warn(text):
    print(f'{bcolors.WARNING}--> {text}{bcolors.ENDC}')


if __name__ == '__main__':

    # Initialize logging
    logger = logging.getLogger('discord')
    level = logging.INFO
    if len(sys.argv) == 2 and sys.argv[1] == '--debug':
        level = logging.DEBUG
    logger.setLevel(level)
    handler = logging.FileHandler(filename='robot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    # Load default modules (i.e. modules listed as 'enabled' in config.json)
    for module in client.config['Modules']:
        if module['enabled']:
            load_module(module)

    client.run(config['Bot']['token'])
