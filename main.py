# settings.py
import os
import json
import settings
import pokemon
import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from random import randint, random

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_TOKEN = os.getenv("GUILD_ID")
SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/users.json')

BOT = commands.Bot(command_prefix='$',
                   description='A bot that greets the user back.')
BOT.remove_command('help')


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

def acc_value(acc):
    if acc == "None":
        return "Can't miss."
    acc = int(acc)
    num = random()*100
    if acc*0.33 >= num:
        return "It hits. Undodgeable."
    if acc*0.36 >= num:
        return "It hits. Dodgeable at +6."
    if acc*0.43 >= num:
        return "It hits. Dodgeable at +5."
    if acc*0.5 >= num:
        return "It hits. Dodgeable at +4."
    if acc*0.6 >= num:
        return "It hits. Dodgeable at +3."
    if acc*0.75 >= num:
        return "It hits. Dodgeable at +2."
    if acc > num:
        return "It hits. Dodgeable at +1."
    return "It misses."

def crit_value():
    num = randint(1,16)
    if num == 1:
        return "Critical Hit."
    if num <= 2:
        return "Critical Hit at +1."
    if num <= 4:
        return "Critical Hit at +2."
    if num <= 6:
        return "Critical Hit at +3."
    if num <= 8:
        return "Critical Hit at +4."
    return "Not critical Hit"

@BOT.command(pass_context=True)
async def HP(ctx, Mon):
    ctx.send('{} has {} HP'.format(Mon, pokemon.Calc.hp_stat(pokemon.DISTROS_DICT['Pokemon'][MonB.lower()]['base stats']['HP'])))

@BOT.command(pass_context=True)
async def battle(ctx, MonA, MonB, Move, Multiplier=1.0, Level1=100, Level2=100):
    FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')
    with open(FILE_PATH, 'r') as f:
        DISTROS_DICT = json.load(f)
    Types = pokemon.DISTROS_DICT['Types']
    Aux1 = pokemon.DISTROS_DICT['Pokemon'][MonA.lower()]
    Aux2 = pokemon.DISTROS_DICT['Pokemon'][MonB.lower()]
    Aux3 = pokemon.DISTROS_DICT['Moves'][Move.lower()]
    HP = pokemon.Calc.hp_stat(Aux2['base stats']['HP'], Level2)
    Immune = False

    for t in Aux2['types']:
        if Types[t][Aux3['type']] == 0:
            Immune = True
        else:
            Multiplier *= Types[t][Aux3['type']]
    print(Multiplier)
    for t in Aux1['types']:
        if t == Aux3['type']:
            Multiplier *= 1.5

    if Aux3['category'] == 'special':
        ATK = pokemon.Calc.stat(Aux1['base stats']['Sp. Attack'], Level1)
        if Move.lower() in ['psyshock', 'psystrike', 'secret-sword']:
            DEF = pokemon.Calc.stat(Aux2['base stats']['Defense'], Level2)
        else:
            DEF = pokemon.Calc.stat(Aux2['base stats']['Sp. Defense'], Level2)
    if Aux3['category'] == 'physical':
        ATK = pokemon.Calc.stat(Aux1['base stats']['Attack'], Level1)
        DEF = pokemon.Calc.stat(Aux2['base stats']['Defense'], Level2)

    if Aux3['min hits'] != "None":
        Min = int(Aux3['min hits'])
        Max = int(Aux3['max hits'])
    else: 
        Min = 1
        Max = 1
    for i in range(randint(Min, Max)):
        print(i)
        RandomValue = randint(85, 100)/100
        Multiplier *= RandomValue
        embed = discord.Embed(
            colour=discord.Colour.dark_red()
        )
        embed.set_author(name=Move.lower())
        embed.add_field(name='{}: {}'.format(Move.lower(), i),
                        value='{}'.format(Aux3['description']).replace('$effect_chance%', '{}%'.format(Aux3['ailment chance'])),
                        inline=False)
        if Immune:
            embed.add_field(
                name='Type',
                value='{} is immune often.'.format(MonB),
                inline=False)
        if Aux3['category'] != 'status':
            DMG = pokemon.Calc.attack_calc(ATK, DEF, int(Aux3['power']), Level1, Multiplier, False)
            DMG2 = pokemon.Calc.attack_calc(ATK, DEF, int(Aux3['power']), Level1, Multiplier, True)
            embed.add_field(name='Acc roll',
                        value='{}\n{}'.format(acc_value(Aux3['accuracy']), crit_value()),
                        inline=False)
            embed.add_field(name='Damage', value='{} = {}%'.format(
                DMG, round(DMG * 100 / HP, 2)), inline=False)
            embed.add_field(name='Crit. hit. damage'.format(MonA, MonB, HP),
                            value='{} = {}%'.format(
                                DMG2, round(DMG2 * 100 / HP, 2)),
                            inline=False)
        else: 
            embed.add_field(name='Acc roll',
                        value='{}'.format(acc_value(Aux3['accuracy'])),
                        inline=False)
        if Aux3['ailment chance'] != "0" and random() <= int(Aux3['ailment chance'])/100:
            embed.add_field(name='Effect Roll',
                            value='{} got [{}] unless prevented'.format(
                                MonB, Aux3['ailment']),
                            inline=False)
        if Aux3['stat chance'] != "0" and random() <= int(Aux3['ailment chance'])/100:
            embed.add_field(name='Stat chance roll',
                            value='Check Description',
                            inline=False)
        if Aux3['critical rate'] != "0":
            embed.add_field(name='Crit. rate',
                            value='+{}'.format(Aux3['critical rate']),
                            inline=False)
        if Aux3['drain'] != "0":
            embed.add_field(name='Drained HP',
                            value='+{}. Crit. {}'.format(
                                round(DMG/100 * int(Aux3['drain']),2),
                                round(DMG2/100 * int(Aux3['drain'])),2),
                            inline=False)
        if Aux3['healing'] != "0":
            embed.add_field(name='Healed HP',
                            value='+{}.'.format(round(HP/100 * int(Aux3['healing'])),2),
                            inline=False)
        if Aux3['flinch chance'] != "0" and random() <= int(Aux3['flinch chance'])/100:
            embed.add_field(name='Flinch',
                            value='{} has flinched'.format(MonB),
                            inline=False)
        embed.set_footer(text='{}►{}'.format(MonA, MonB))
        await ctx.send(embed=embed)


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
