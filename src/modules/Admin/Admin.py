import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def game(self, context, *, game=None):
        if game is None:
            await context.send(f'My current game: {game.name for game in self.client.activities}')
        else:
            has_admin = self.client.permission_authority.hasperm('admin.*', context.message.author)
            has_game = self.client.permission_authority.hasperm('admin.game', context.message.author)
            if has_admin or has_game:
                await self.client.change_presence(activity=discord.Game(game))
            else:
                await self.no_perm(context, 'game')

    @commands.command()
    async def purge(self, context, amount=10):
        has_admin = self.client.permission_authority.hasperm('admin.*', context.message.author)
        has_purge = self.client.permission_authority.hasperm('admin.purge', context.message.author)
        if has_admin or has_purge:
            await context.channel.purge(limit=amount)
        else:
            await self.no_perm(context, 'purge')

    @commands.command()
    async def kick(self, context, member: discord.Member, *, reason=None):
        has_admin = self.client.permission_authority.hasperm('admin.*', context.message.author)
        has_kick = self.client.permission_authority.hasperm('admin.kick', context.message.author)
        if has_admin or has_kick:
            await member.kick(reason=reason)
            await context.send(f'Kicked {member.mention}. I wonder if it hurt...')
        else:
            await self.no_perm(context, 'kick')

    @commands.command()
    async def ban(self, context, member: discord.Member, *, reason=None):
        has_admin = self.client.permission_authority.hasperm('admin.*', context.message.author)
        has_ban = self.client.permission_authority.hasperm('admin.ban', context.message.author)
        if has_admin or has_ban:
            await member.ban(reason=reason)
            await context.send(f'Banned {member.mention}. Good riddance!')
        else:
            await self.no_perm(context, 'ban')

    @commands.command()
    async def unban(self, context, *, member):
        has_admin = self.client.permission_authority.hasperm('admin.*', context.message.author)
        has_unban = self.client.permission_authority.hasperm('admin.unban', context.message.author)
        if has_admin or has_unban:
            banned_users = await context.guild.bans()
            name, discriminator = member.split('#')

            for entry in banned_users:
                user = entry.user
                if (user.name, user.discriminator) == (name, discriminator):
                    await context.guild.unban(user)
                    await context.send(f'Unbanned {user.mention}. Welcome back!')
                    return
        else:
            await self.no_perm(context, 'unban')

    async def no_perm(self, context, perm):
        await context.send(f'You do not have permission \'admin.{perm}\'')


def setup(client):
    client.add_cog(Admin(client))
