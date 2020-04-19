# settings.py
import settings
import os
import discord
from discord.ext import commands


class pokemon:
    num: 1
    name: "Bulbasaur"
    types: ["Grass", "Poison"]
    genderRatio: {
        "M": 0.875,
        "F": 0.125
    }
    baseStats: {
        "hp": 45,
        "atk": 49,
        "def": 49,
        "spa": 65,
        "spd": 65,
        "spe": 45,
    }
    abilities: {
        "0": "Overgrow",
        "H": "Chlorophyll"
    }
    heightm: 0.7
    weightkg: 6.9
    color: "Green"
    tier: "LC"

    def __init__(self):
        print("Species {}".format(self.name))


class OC:
    def __init__(self):
        self.name = "Null"
        self.species = pokemon()
        self.userID = 0
        self.finalStats: {
            "hp": 294,
            "atk": 216,
            "def": 216,
            "spa": 251,
            "spd": 251,
            "spe": 207
        }
        print("Registered OC")

    def __del__(self):
        print("Deleted OC", self.name)

    def __str__(self):
        return '{}'.format(self.name)

    # def __len__(self):
    #    return self.tiempo

    def register(self):
        self.name = "Registered"


class ListOC:
    OC = []

    def __init__(self, OC=[]):
        self.OC = OC

    def add(self, OC):
        self.OC.append(OC)


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_TOKEN = os.getenv("GUILD_ID")

bot = commands.Bot(command_prefix='$',
                   description='A bot that greets the user back.')
bot.remove_command('help')


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


@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)


@bot.command(pass_context=True)
async def help(ctx, args=''):
    print(ctx.message.author)
    embed = discord.Embed(
        colour=discord.Colour.dark_red()
    )
    embed.set_author(name='Help')
    embed.add_field(name='{}Help'.format(bot.command_prefix),
                    value='Main Help command, 3 pages.', inline=False)
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
