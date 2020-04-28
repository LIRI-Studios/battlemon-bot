# settings.py
import os
import json
import settings
import discord
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_TOKEN = os.getenv("GUILD_ID")
SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/users.json')

with open(FILE_PATH, 'r') as f:
    DISTROS_DICT = json.load(f)

BOT = commands.Bot(command_prefix='$',
                   description='A bot that greets the user back.')
BOT.remove_command('help')

def write_json(data, filename=FILE_PATH): 
    with open(filename,'w') as json_file: 
        json.dump(data, json_file, indent=4) 


@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.id)
    print('------')
    activity = discord.Game(name="$help 1")
    await BOT.change_presence(status=discord.Status.online, activity=activity)


@BOT.event
async def on_member_join(member, guild):
    await member.create_dm()
    await member.dm_channel.send(f'Hi {member.name}, welcome to {guild.name}')


@BOT.event
async def on_member_leave(member, guild):
    print(f'{member} has left the server')


@BOT.command()
async def select(ctx, args=''):
    if ctx.message.guild.id in DISTROS_DICT:
        if ctx.message.author.id in DISTROS_DICT[ctx.message.guild.id]:
            if args in DISTROS_DICT[ctx.message.guild.id][ctx.message.guild.id]['OCs']:
                with open(FILE_PATH) as json_file:
                    data = json.load(json_file)
                    data['{}'.format(ctx.message.guild.id)]['{}'.format(ctx.message.author.id)] = args
                write_json(data)
                await ctx.send('Character |{}| is Selected'.format(args))
            else:
                await ctx.send('Character |{}| isn\'t registered'.format(args))
        else: # User not registered
            await ctx.send('Try registering an OC. Use {}register {}'.format(BOT.command_prefix, args))
    else: # Guild not registered
        await ctx.send('Try registering an OC. Use {}register {}'.format(BOT.command_prefix, args))

@BOT.command()
async def register(ctx, args=''):
    with open(FILE_PATH) as json_file:
        data = json.load(json_file)
        temp = data['Servers']
        Flag1 = True
        for server in temp:
            if server['ID'] == ctx.message.guild.id:
                Flag1 = False
                Flag2 = True
                for user in server['Users']:
                    if user['ID'] == ctx.message.user.id:
                        Flag2 = False
                        Flag3 = True
                        for oc in user['OCS']:
                            if oc['Name'] == args:
                                Flag3 = False
                                await ctx.send('Character |{}| is registered already'.format(args))
                                return
                        if Flag3:
                            user['OCS'].append({"Name": args})
                            await ctx.send('Character |{}| was registered'.format(args))
                            return
                if Flag2:
                    server['Users'].append(
                        {
                            "ID":ctx.message.user.id,
                            "Selected":0,
                            "OCS":[{"Name": args}]
                        }
                    )
        if Flag1:
            temp.append(
                {
                    "ID": ctx.message.guild.id,
                    "Users":[
                        {
                            "ID":ctx.message.user.id,
                            "Selected":0,
                            "OCS":[{"Name": args}]
                        }
                    ]
                }
            )
    write_json(data)

    await ctx.send('Character |{}| is registered already'.format(args))

@BOT.command()
async def add(ctx, a: int, b: int):
    print(ctx.message.id)
    await ctx.send(a+b)


@BOT.command(pass_context=True)
async def help(ctx, args=''):
    print(ctx.message.author)
    embed = discord.Embed(
        colour=discord.Colour.dark_red()
    )
    embed.set_author(name='Help')
    embed.add_field(name='{}Help'.format(BOT.command_prefix),
                    value='Main Help command, 3 pages.', inline=False)
    if args == '1':
        embed.add_field(
            name='{}register <name>'.format(BOT.command_prefix),
            value='It adds an OC.',
            inline=False)
        embed.add_field(
            name='{}select <name>'.format(BOT.command_prefix),
            value='Selects an OC for commands usage.',
            inline=False)
        embed.add_field(
            name='{}?'.format(BOT.command_prefix),
            value='Displays the selected OC\'s name',
            inline=False)
        embed.add_field(
            name='{}data'.format(BOT.command_prefix),
            value='Shows the required fields for the selected OC.',
            inline=False)
    if args == '2':
        embed.add_field(
            name='{}data <field>'.format(BOT.command_prefix),
            value='It shows the <field> information for the selected OC.',
            inline=False)
        embed.add_field(
            name='{}add <field> <text>'.format(BOT.command_prefix),
            value='It allows to add the <field> selected OC\'s <text> information.',
            inline=False)
        embed.add_field(
            name='{}moves'.format(BOT.command_prefix),
            value='Displays the selected OC\'s moveset.',
            inline=False)
        embed.add_field(
            name='{}moves <name>'.format(BOT.command_prefix),
            value='Replaces/Adds <name> move to the selected OC\'s moveset.',
            inline=False)
    if args == '3':
        embed.add_field(
            name='{}read <user> <name>'.format(BOT.command_prefix),
            value='It allows to read an user\'s OC information.',
            inline=False
        )

    embed.set_footer(text='use {}help <page>'.format(BOT.command_prefix))
    await ctx.send(embed=embed)

BOT.run(DISCORD_TOKEN)
