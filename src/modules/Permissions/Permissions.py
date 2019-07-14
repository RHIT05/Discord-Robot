import sqlite3
import discord
from discord.ext import commands
from discord.ext.commands.errors import *
DB = 'permissions.db'


class Permissions(commands.Cog):

    def __init__(self, client):
        client.permission_authority = self
        self.client = client
        self.cwd = client.config['Bot']['modules_dir'] + 'Permissions/'
        conn = sqlite3.connect(self.cwd + DB)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS permissions(user int, permission text)')
        conn.commit()
        conn.close()

    @commands.command()
    async def perms(self, context):
        conn = sqlite3.connect(self.cwd + DB)
        c = conn.cursor()
        perms = await(c.execute(
            'SELECT permission FROM permissions WHERE user=?', context.message.author.id))
        conn.commit()
        conn.close()
        print(perms)

    @commands.command()
    async def giveperm(self, context, permission, member: discord.Member):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            conn = sqlite3.connect(self.cwd + DB)
            c = conn.cursor()
            c.execute('INSERT INTO permissions(user, permission) VALUES (?, ?)', (
                member.id, permission))
            conn.commit()
            conn.close()
            await context.send(f"Gave permission '{permission}' to {member.name}.")
        else:
            await context.send(f"You do not have permission to do that. Ask for the role {mod_role}.")

    @commands.command()
    async def takeperm(self, context, permission, member: discord.Member):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            conn = sqlite3.connect(self.cwd + DB)
            c = conn.cursor()
            c.execute('DELETE FROM permissions WHERE user=? AND permission=?', (
                member.id, permission))
            conn.commit()
            conn.close()
            await context.send(f"Revoked permission '{permission}' from {member.name}.")
        else:
            await context.send(f"You do not have permission to do that. Ask for the role {mod_role}.")

    @commands.command()
    async def mod(self, context, member: discord.Member):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            await member.add_roles(discord.utils.get((member.guild.roles), name=mod_role))
            await context.send(f"{member.name} is now a mod.")
        else:
            await context.send(f"You do not have permission to do that. Ask for the role {mod_role}.")

    @commands.command()
    async def unmod(self, context, member: discord.Member):
        mod_role = self.client.config['Bot']['mod_role']
        if mod_role in [role.name.lower() for role in context.message.author.roles]:
            await member.remove_roles(discord.utils.get((member.guild.roles), name=mod_role))
            await context.send(f"{member.name} is no longer a mod.")
        else:
            await context.send(f"You do not have permission to do that. Ask for the role {mod_role}.")

    def hasperm(self, permission, member: discord.Member):
        conn = sqlite3.connect(self.cwd + DB)
        c = conn.cursor()
        hasperm = len(c.execute('SELECT * FROM permissions WHERE user=? AND permission=?', (
            member.id, permission))) > 0
        conn.commit()
        conn.close()
        return hasperm


def setup(client):
    client.add_cog(Permissions(client))
