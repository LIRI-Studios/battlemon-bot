# settings.py
# import settings
import os
import pokemon
import discord
import pokebase as pb
from discord.ext import commands
from tinydb import TinyDB, Query
from random import randint, random

from os import getenv

# DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# GUILD_TOKEN = os.getenv("GUILD_ID")

BOT = commands.Bot(command_prefix='$', description='Bot that handles pokemon combat.')
BOT.remove_command('help')

@BOT.event
async def on_ready():
    print('Logged in as')
    print(BOT.user.id)
    print('------')
    activity = discord.Game(name='{}help'.format(BOT.command_prefix))
    await BOT.change_presence(status=discord.Status.online, activity=activity)

@BOT.event
async def on_member_join():
    pass

@BOT.event
async def on_member_leave(member, guild):
    print(f'{member} has left the server')

def acc_value(acc):
    if acc == 'None':
        return 'Can\'t miss.'
    acc = int(acc)
    num = random()*100
    for i in range(9, 2, -1):
        if 3*acc/i >= num:
            return 'It hits. Dodgeable at +{}'.format(i-2)
    return 'It misses.' # Dodgeable at +0

def crit_value():
    num = randint(1, 16)
    if num == 1:
        return 'Critical Hit.'
    for i in range(1, 5):
        if num <= 2*i:
            return 'Critical Hit at +{}.'.format(i)
    return 'Not critical Hit.'

@BOT.command(pass_context=True)
async def stats(ctx, Mon, Lvl=100):
    Aux1 = pb.pokemon(Mon)
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.add_field(name='HP', value='{}'.format(pokemon.Calc.hp_stat(Aux1.stats[5].base_stat, Lvl)))
    embed.add_field(name='Attack', value='{}'.format(pokemon.Calc.stat(Aux1.stats[4].base_stat, Lvl)))
    embed.add_field(name='Defense', value='{}'.format(pokemon.Calc.stat(Aux1.stats[3].base_stat, Lvl)))
    embed.add_field(name='Sp. Attack', value='{}'.format(pokemon.Calc.stat(Aux1.stats[2].base_stat, Lvl)))
    embed.add_field(name='Sp. Defense', value='{}'.format(pokemon.Calc.stat(Aux1.stats[1].base_stat, Lvl)))
    embed.add_field(name='Speed', value='{}'.format(pokemon.Calc.stat(Aux1.stats[0].base_stat, Lvl)))
    embed.set_footer(text='{} | Max IVs | Favourable Nature'.format(Mon))
    await ctx.send(embed=embed)

@BOT.command(pass_context=True)
async def setup(ctx, args=''):
    vals = args.split()
    pass

@BOT.command(pass_context=True)
async def battle(ctx, MonA: str, MonB: str, Move: str, Multiplier=1.0, Level1=100, Level2=100):
    Aux1 = pb.pokemon(MonA.lower())
    Aux2 = pb.pokemon(MonB.lower())
    Aux3 = pb.move(Move.lower())
    types1 = []
    types2 = []
    for item in Aux1.types:
        types1.append(item.type.name)
    for item in Aux2.types:
        types2.append(item.type.name)
    HP = pokemon.Calc.hp_stat(Aux2.stats[5].base_stat, Level2)
    Immune = False
    Multiplier *= pokemon.Calc.type_effectiveness(types1, Aux3.type.name, types2)
    if Aux3.damage_class.name == 'special':
        ATK = pokemon.Calc.stat(Aux1.stats[2].base_stat, Level1)
        if Move.lower() in ['psyshock', 'psystrike', 'secret-sword']:
            DEF = pokemon.Calc.stat(Aux2.stats[3].base_stat, Level2)
        else:
            DEF = pokemon.Calc.stat(Aux2.stats[1].base_stat, Level2)
    if Aux3.damage_class.name == 'physical':
        ATK = pokemon.Calc.stat(Aux1.stats[4].base_stat, Level1)
        DEF = pokemon.Calc.stat(Aux2.stats[3].base_stat, Level2)

    Min = Aux3.meta.min_hits if Aux3.meta.min_hits is not None else 1
    Max = Aux3.meta.max_hits if Aux3.meta.min_hits is not None else 1
    for i in range(randint(Min, Max)):
        RandomValue = randint(85, 100)/100
        embed = discord.Embed(colour=discord.Colour.dark_red())
        embed.set_author(name=Move.lower())
        embed.add_field(name='{}: {}'.format(Move.lower(), i), value='{}'.format(Aux3.effect_entries[0].short_effect).replace('$effect_chance%','{}%'.format(Aux3.effect_chance)), inline=False)
        if Immune:
            embed.add_field(name='Type', value='{} is immune often.'.format(MonB), inline=False)
        if Aux3.damage_class.name != 'status' and Aux3.meta.category.name != 'ohko':
            DMG = pokemon.Calc.attack_calc(ATK, DEF, Aux3.power, Level1, Multiplier*RandomValue, False)
            DMG2 = pokemon.Calc.attack_calc(ATK, DEF, Aux3.power, Level1, Multiplier*RandomValue, True)
            embed.add_field(name='Acc roll', value='{}\n{}'.format(acc_value(Aux3.accuracy), crit_value()), inline=False)
            embed.add_field(name='Damage', value='{} = {}%'.format(DMG, round(DMG * 100 / HP, 2)), inline=False)
            embed.add_field(name='Crit. hit. damage'.format(MonA, MonB, HP),value='{} = {}%'.format(DMG2, round(DMG2 * 100 / HP, 2)), inline=False)
        else: 
            embed.add_field(name='Acc roll', value='{}'.format(acc_value(Aux3.accuracy)), inline=False)
        
        if Aux3.meta.ailment_chance != 0 and random() <= Aux3.meta.ailment_chance/100:
            embed.add_field(name='Effect Roll', value='{} got [{}] unless prevented'.format(MonB, Aux3.meta.ailment.name), inline=False)
        
        if Aux3.meta.stat_chance != 0 and random() <= Aux3.meta.ailment_chance/100:
            embed.add_field(name='Stat chance roll', value='Check Description', inline=False)
        
        if Aux3.meta.crit_rate != 0:
            embed.add_field(name='Crit. rate', value='+{}'.format(Aux3.meta.crit_rate), inline=False)

        if Aux3.meta.drain != 0:
            embed.add_field(name='Drained HP', value='+{}. Crit. {}'.format(round(DMG/100 * Aux3.meta.drain, 2), round(DMG2/100 * Aux3.meta.drain, 2)), inline=False)

        if Aux3.meta.healing != 0:
            embed.add_field(name='Healed HP', value='+{}.'.format(round(HP/100 * Aux3.meta.healing, 2)), inline=False)

        if Aux3.meta.flinch_chance != 0 and random() <= Aux3.meta.flinch_chance/100:
            embed.add_field(name='Flinch', value='{} has flinched'.format(MonB), inline=False)

        embed.set_footer(text='{}►{} | {}% | {}x'.format(MonA, MonB, round(RandomValue*100, 2), Multiplier))
        await ctx.send(embed=embed)

@BOT.command(pass_context=True)
async def help(ctx, args=''):
    print(ctx.message.author)
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_author(name='Help')
    embed.add_field(name='{}Help'.format(BOT.command_prefix),value='Main Help command, 3 pages.')
    if args == '1':
        embed.add_field(name='{}register <name>'.format(BOT.command_prefix),value='It adds an OC.')
        embed.add_field(name='{}select <name>'.format(BOT.command_prefix),value='Selects an OC for commands usage.')
        embed.add_field(name='{}?'.format(BOT.command_prefix),value='Displays the selected OC\'s name')
        embed.add_field(name='{}data'.format(BOT.command_prefix),value='Shows the required fields for the selected OC.')
    if args == '2':
        embed.add_field(name='{}data <field>'.format(BOT.command_prefix),value='It shows the <field> information for the selected OC.')
        embed.add_field(name='{}add <field> <text>'.format(BOT.command_prefix),value='It allows to add the <field> selected OC\'s <text> information.')
        embed.add_field(name='{}moves'.format(BOT.command_prefix),value='Displays the selected OC\'s moveset.',)
        embed.add_field(name='{}moves <name>'.format(BOT.command_prefix),value='Replaces/Adds <name> move to the selected OC\'s moveset.')
    if args == '3':
        embed.add_field(name='{}read <user> <name>'.format(BOT.command_prefix),value='It allows to read an user\'s OC information.')

    embed.set_footer(text='use {}help <page>'.format(BOT.command_prefix))
    await ctx.send(embed=embed)

# BOT.run(DISCORD_TOKEN)
