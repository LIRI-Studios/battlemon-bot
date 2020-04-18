# settings.py
import settings
import os
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_TOKEN =  os.getenv("GUILD_ID")

bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')
bot.remove_command('help')

def damage():
    pass

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member, guild):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to {guild.name}')

@bot.event
async def on_member_leave(member, guild):
    print(f'{member} has left the server')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_member_leave(member, guild):
    print(f'{member} has left the server')

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command(pass_context=True)
async def help(ctx, args=''):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.dark_red()
    )
    embed.set_author(name='Help')
    embed.add_field(name='{}Help'.format(bot.command_prefix), value='Main Help command, 3 pages.', inline=False)
    if args == '1':
        embed.add_field(
            name='{}register <name>'.format(bot.command_prefix),
            value='It adds an OC.',
            inline=False)
        embed.add_field(
            name='{}select <name>'.format(bot.command_prefix),
            value='Selects an OC for commands usage.',
            inline=False)
        embed.add_field(
            name='{}?'.format(bot.command_prefix),
            value='Displays the selected OC\'s name',
            inline=False)
        embed.add_field(
            name='{}data'.format(bot.command_prefix),
            value='Shows the required fields for the selected OC.',
            inline=False)
    if args == '2':
        embed.add_field(
            name='{}data <field>'.format(bot.command_prefix),
            value='It shows the <field> information for the selected OC.',
            inline=False)
        embed.add_field(
            name='{}add <field> <text>'.format(bot.command_prefix),
            value='It allows to add the <field> selected OC\'s <text> information.',
            inline=False)
        embed.add_field(
            name='{}moves'.format(bot.command_prefix),
            value='Displays the selected OC\'s moveset.',
            inline=False)
        embed.add_field(
            name='{}moves <name>'.format(bot.command_prefix),
            value='Replaces/Adds <name> move to the selected OC\'s moveset.',
            inline=False)
    if args == '3':
        embed.add_field(
            name='{}read <user> <name>'.format(bot.command_prefix),
            value='It allows to read an user\'s OC information.',
            inline=False
        )

    embed.set_footer(text='use {}help <page>'.format(bot.command_prefix))
    await ctx.send(embed=embed)


bot.run(DISCORD_TOKEN)
