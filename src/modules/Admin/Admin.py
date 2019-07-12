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
            await self.client.change_presence(activity=discord.Game(game))

    @commands.command()
    async def purge(self, context, amount=10):
        await context.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, context, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await context.send(f'Kicked {member.mention}. I wonder if it hurt...')

    @commands.command()
    async def ban(self, context, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await context.send(f'Banned {member.mention}. Good riddance!')

    @commands.command()
    async def unban(self, context, *, member):
        banned_users = await context.guild.bans()
        name, discriminator = member.split('#')

        for entry in banned_users:
            user = entry.user
            if (user.name, user.discriminator) == (name, discriminator):
                await context.guild.unban(user)
                await context.send(f'Unbanned {user.mention}. Welcome back!')
                return


def setup(client):
    client.add_cog(Admin(client))
