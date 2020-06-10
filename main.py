
import os
import discord
import pokemon
from discord.ext import commands
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT = commands.Bot(command_prefix='rp!', description='Bot that handles pokemon combat.')
BOT.remove_command('help')


@BOT.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == BOT.user:
        return
    if not message.author.bot:
        await BOT.process_commands(message)
        return
    raw = [pos for pos, char in enumerate(message.content) if char == '[']
    raw2 = [pos for pos, char in enumerate(message.content) if char == ']']
    if len(raw) != 0 and len(raw) == len(raw2):
        for i in range(len(raw)):
            move = str(message.content[raw[i]+1:raw2[i]]
                       ).replace(' ', '-').lower()
            print(move)
            await message.channel.send(embed=pokemon.move(move))

# Function to load stats
@BOT.command(pass_context=True)
async def stats(ctx, mon, lvl=100):
    await ctx.send(embed=pokemon.stats(mon, lvl))

# Function to calculate battle moves against species
@BOT.command(pass_context=True)
async def battle(ctx, mon_a: str, mon_b: str, move: str, multiplier=1.0):
    embeds = pokemon.battle(mon_a, mon_b, move, multiplier)
    for embed in embeds:
        await ctx.send(embed=embed)

# Function to calculate battle moves
@BOT.command(pass_context=True)
async def move(ctx, move: str):
    await ctx.send(embed=pokemon.move(move))

# Function to get commands information
@BOT.command(pass_context=True)
async def help(ctx, args=''):
    print(ctx.message.author)
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_author(name='Help')
    embed.add_field(
        name='{}Help'.format(BOT.command_prefix),
        value='Main Help command, 3 pages.'
    )
    if args == '1':
        embed.add_field(
            name='{}register <name>'.format(BOT.command_prefix),
            value='It adds an OC.'
        )
        embed.add_field(
            name='{}select <name>'.format(BOT.command_prefix),
            value='Selects an OC for commands usage.'
        )
        embed.add_field(
            name='{}?'.format(BOT.command_prefix),
            value='Displays the selected OC\'s name'
        )
        embed.add_field(
            name='{}data'.format(BOT.command_prefix),
            value='Shows the required fields for the selected OC.'
        )
    if args == '2':
        embed.add_field(
            name='{}data <field>'.format(BOT.command_prefix),
            value='It shows the <field> information for the selected OC.'
        )
        embed.add_field(
            name='{}add <field> <text>'.format(BOT.command_prefix),
            value='It allows to add the <field> selected OC\'s <text> information.'
        )
        embed.add_field(
            name='{}moves'.format(BOT.command_prefix),
            value='Displays the selected OC\'s moveset.',
        )
        embed.add_field(
            name='{}moves <name>'.format(BOT.command_prefix),
            value='Replaces/Adds <name> move to the selected OC\'s moveset.'
        )
    if args == '3':
        embed.add_field(
            name='{}read <user> <name>'.format(BOT.command_prefix),
            value='It allows to read an user\'s OC information.'
        )

    embed.set_footer(text='use {}help <page>'.format(BOT.command_prefix))
    await ctx.send(embed=embed)


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    print('------')

BOT.run(DISCORD_TOKEN)
