# -*- coding: utf-8 -*-
import math
import textwrap
import discord
import pokebase as pb
from random import randint, random


def index_2d(_data, _search):
    for i, value in enumerate(_data):
        try:
            return i, value.index(_search)
        except ValueError:
            pass
    raise ValueError('{} is not in list'.format(repr(_search)))


def stats(mon, lvl=100):
    aux_value = pb.pokemon(mon)
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.add_field(
        name='HP',
        value='{}'.format(hp_stat(aux_value.stats[5].base_stat, lvl))
    )
    embed.add_field(
        name='Attack',
        value='{}'.format(stat(aux_value.stats[4].base_stat, lvl))
    )
    embed.add_field(
        name='Defense',
        value='{}'.format(stat(aux_value.stats[3].base_stat, lvl))
    )
    embed.add_field(
        name='Sp. Attack',
        value='{}'.format(stat(aux_value.stats[2].base_stat, lvl))
    )
    embed.add_field(
        name='Sp. Defense',
        value='{}'.format(stat(aux_value.stats[1].base_stat, lvl))
    )
    embed.add_field(
        name='Speed',
        value='{}'.format(stat(aux_value.stats[0].base_stat, lvl))
    )
    embed.set_footer(text='{} | Max IVs | Favourable Nature'.format(mon))
    return embed


def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
    print('HP: {}'.format(10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))
    return 10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))


def stat(_base, _lvl=100, _ivs=31, _evs=255, _nat=1.1):
    print('STAT: {}'.format(math.floor(
        _nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))))
    return math.floor(_nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))


def attack_calc(_atk_value, _def_value, _pwr=None, _mul=1, _crit=False, _lvl=100):
    if _crit:
        _lvl *= 2
    if _pwr is None:
        return 0
    else:
        return math.floor(_mul * (math.floor(math.floor(math.floor(2 * _lvl / 5 + 2) * _pwr * _atk_value / _def_value) / 50) + 2))


def type_effectiveness(_name='typeless', _defense=['typeless'], _ignore_immune=False):
    types = [
        'normal',   'fire',     'water',    'electric', 'grass',    'ice',  'fighting',
        'poison',   'ground',   'flying',   'psychic',  'bug',      'rock', 'ghost',
        'dragon',   'dark',     'steel',    'fairy',    'typeless', 'shadow'
    ]
    chart = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1/2, 0, 1, 1, 1/2, 1, 1, 1/2],
        [1, 1/2, 1/2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1/2, 1, 1/2, 1, 2, 1, 1, 1/2],
        [1, 2, 1/2, 1, 1/2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1/2, 1, 1, 1, 1, 1/2],
        [1, 1, 2, 1/2, 1/2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1/2, 1, 1, 1, 1, 1/2],
        [1, 1/2, 2, 1, 1/2, 1, 1, 1/2, 2, 1/2, 1, 1/2, 2, 1, 1/2, 1, 1/2, 1, 1, 1/2],
        [1, 1/2, 1/2, 1, 2, 1/2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1, 1/2],
        [2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1/2, 1/2, 1/2, 2, 0, 1, 2, 2, 1/2, 1, 1/2],
        [1, 1, 1, 1, 2, 1, 1, 1/2, 1/2, 1, 1, 1, 1/2, 1/2, 1, 1, 0, 2, 1, 1/2],
        [1, 2, 1, 2, 1/2, 1, 1, 2, 1, 0, 1, 1/2, 2, 1, 1, 1, 2, 1, 1, 1/2],
        [1, 1, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1/2, 1, 1, 1/2],
        [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1/2, 1, 1, 1, 1, 0, 1/2, 1, 1, 1/2],
        [1, 1/2, 1, 1, 2, 1, 1/2, 1/2, 1, 1/2, 2, 1, 1, 1/2, 1, 2, 1/2, 1/2, 1, 1/2],
        [1, 2, 1, 1, 1, 2, 1/2, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 1/2, 1, 1, 1/2],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1, 1, 1/2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1/2, 0, 1, 1/2],
        [1, 1, 1, 1, 1, 1, 1/2, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1/2, 1, 1/2],
        [1, 1/2, 1/2, 1/2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1/2, 2, 1, 1/2],
        [1, 1/2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1, 1, 1, 2, 2, 1/2, 1, 1, 1/2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1]
    ]
    val = 1
    for _type in _defense:
        if _name in types and _type in types:
            aux = chart[types.index(_name)][types.index(_type)]
            val *= aux if aux != 0 else _ignore_immune
    return val


def nature(_name):
    result = [1, 1, 1, 1, 1]
    natures = [
        ['Hardy', 'Lonely', 'Adamant', 'Naughty', 'Brave'],
        ['Bold', 'Docile', 'Impish', 'Lax', 'Relaxed'],
        ['Modest', 'Mild', 'Bashful', 'Rash', 'Quiet'],
        ['Calm', 'Gentle', 'Careful', 'Quirky', 'Sassy'],
        ['Timid', 'Hasty', 'Jolly', 'Naive', 'Serious'],
    ]
    coords = index_2d(natures, _name)
    result[coords[0]] -= 0.1
    result[coords[1]] += 0.1
    return result


def move(move: str):
    aux3 = pb.move(move.lower())
    random_value = randint(85, 100)/100
    embed = discord.Embed(colour=discord.Colour.dark_red())
    embed.set_author(name=move.lower())
    for item in aux3.flavor_text_entries:
        if item.language.name == 'en' and item.version_group.name == 'ultra-sun-ultra-moon':
            text = item.flavor_text
    embed.add_field(name=move.lower(), value=text, inline=False)
    embed.add_field(
        name='Acc. roll',
        value='{}'.format(acc_value(aux3.accuracy)),
        inline=False
    )
    if aux3.damage_class.name != 'status' and aux3.meta.category.name != 'ohko':
        def_value = 'By using a {} attack, it damages the '.format(
            aux3.damage_class.name)
        def_value += '' if aux3.damage_class.name == 'physical' or move.lower(
        ) in ['psyshock', 'psystrike', 'secret-sword'] else 'special ' + 'defense stat.'
        embed.add_field(
            name='{}-type attack with power: {}'.format(aux3.type.name, aux3.power),
            value='{}'.format(def_value),
            inline=False
        )
        embed.add_field(
            name='Critical hit roll',
            value='A Critical is {}'.format(crit_value()),
            inline=False
        )

    if aux3.meta.ailment_chance != 0 and random() <= aux3.meta.ailment_chance/100:
        embed.add_field(
            name='Effect Roll',
            value='Target/s got [{}] unless prevented.'.format(
                aux3.meta.ailment.name),
            inline=False
        )

    if aux3.meta.stat_chance != 0 and random() <= aux3.meta.ailment_chance/100:
        embed.add_field(
            name='Stat chance roll',
            value='Check Description',
            inline=False
        )

    if aux3.meta.crit_rate != 0:
        embed.add_field(
            name='Crit. rate',
            value='+{}'.format(aux3.meta.crit_rate),
            inline=False
        )

    if aux3.meta.drain != 0:
        embed.add_field(
            name='Drained HP (%)',
            value='{}'.format(aux3.meta.drain),
            inline=False
        )

    if aux3.meta.healing != 0:
        embed.add_field(
            name='Healed HP(%)',
            value='{}'.format(aux3.meta.healing),
            inline=False
        )

    if aux3.meta.flinch_chance != 0 and random() <= aux3.meta.flinch_chance/100:
        embed.add_field(
            name='Flinch',
            value='Target has flinched',
            inline=False
        )
    embed.set_footer(text='Gen 2 Crit. Hit. Chart')
    return embed


def battle(mon_a: str, mon_b: str, move: str, multiplier=1.0):
    move = move.lower().replace(' ', '-')
    aux1 = pb.pokemon(mon_a.lower())
    aux2 = pb.pokemon(mon_b.lower())
    aux3 = pb.move(move.lower())
    types1 = [item.type.name for item in aux1.types]
    types2 = [item.type.name for item in aux2.types]
    hp_value = hp_stat(aux2.stats[5].base_stat)

    ignore_immune = type_effectiveness(aux3.type.name, types2) == 0

    if move.lower() in ['low-kick', 'grass-knot']:
        if 1 <= aux2.weight < 100:
            aux3.power = 20
        if 100 <= aux2.weight < 250:
            aux3.power = 40
        if 250 <= aux2.weight < 500:
            aux3.power = 60
        if 500 <= aux2.weight < 1000:
            aux3.power = 80
        if 1000 <= aux2.weight < 2000:
            aux3.power = 100
        if 2000 <= aux2.weight:
            aux3.power = 120

    if move.lower() == 'flying-press':
        multiplier *= type_effectiveness('flying', types2)

    if move.lower() == 'freeze-dry' and 'water' in types2:
        multiplier *= 2

    multiplier *= type_effectiveness(aux3.type.name, types2, ignore_immune)
    idx = 2 if aux3.damage_class.name == 'special' else 4
    idy = 1 if aux3.damage_class.name == 'special' else 3
    atk_value = stat(aux1.stats[idx].base_stat)
    def_value = stat(aux2.stats[3].base_stat) if move.lower() in ['psyshock', 'psystrike', 'secret-sword'] else stat(aux2.stats[idy].base_stat)

    if aux3.meta is None:
        min_value = 1
        max_value = 1
    else:
        min_value = aux3.meta.min_hits if aux3.meta.min_hits is not None else 1
        max_value = aux3.meta.max_hits if aux3.meta.min_hits is not None else 1

    _embeds = []
    for i in range(randint(min_value, max_value)):
        random_value = randint(85, 100)/100
        embed = discord.Embed(colour=discord.Colour.dark_red())
        embed.set_author(name=move.lower())
        embed.add_field(
            name='{}: {}'.format(move.lower(), i),
            value='{}'.format(aux3.effect_entries[0].short_effect).replace(
                '$effect_chance%', '{}%'.format(aux3.effect_chance)),
            inline=False
        )
        if ignore_immune:
            embed.add_field(
                name='Type Chart',
                value='{} pokemon are immune to {} often.'.format('/'.join(types2), move.replace('-', ' ')),
                inline=False
            )

        if aux3.damage_class.name != 'status' and aux3.meta.category.name != 'ohko':
            dmg_value_a = attack_calc(atk_value, def_value, aux3.power, multiplier*random_value)
            dmg_value_b = attack_calc(
                atk_value, def_value, aux3.power, multiplier*random_value, True)
            embed.add_field(
                name='Damage',
                value='{} = {}%'.format(dmg_value_a, round(dmg_value_a * 100 / hp_value, 2)),
                inline=False
            )
            embed.add_field(
                name='Crit. hit. damage',
                value='{} = {}%'.format(dmg_value_b, round(dmg_value_b * 100 / hp_value, 2)),
                inline=False
            )
            embed.add_field(
                name='Acc roll',
                value='{}\n Critical hit: {}'.format(acc_value(aux3.accuracy), crit_value()),
                inline=False
            )

        if aux3.meta.ailment_chance != 0 and random() <= aux3.meta.ailment_chance/100:
            embed.add_field(
                name='Effect Roll',
                value='{} got [{}] unless prevented.'.format(
                    mon_b, aux3.meta.ailment.name),
                inline=False
            )

        if aux3.meta.stat_chance != 0 and random() <= aux3.meta.ailment_chance/100:
            embed.add_field(
                name='Stat chance roll',
                value='Check Description',
                inline=False
            )

        if aux3.meta.crit_rate != 0:
            embed.add_field(
                name='Crit. rate',
                value='+{}'.format(aux3.meta.crit_rate),
                inline=False
            )

        if aux3.meta.drain != 0:
            embed.add_field(
                name='Drained HP',
                value='+{}. Crit. {}'.format(
                    round(dmg_value_a/100 * aux3.meta.drain, 2),
                    round(dmg_value_b/100 * aux3.meta.drain, 2)),
                inline=False
            )

        if aux3.meta.healing != 0:
            restored = int(hp_value * aux3.meta.healing / 100)
            hp_ref_value = int(restored/hp_stat(aux1.stats[5].base_stat))
            embed.add_field(
                name='Healed HP',
                value='+{} = +{}.'.format(restored, hp_ref_value),
                inline=False
            )

        if aux3.meta.flinch_chance != 0 and random() <= aux3.meta.flinch_chance/100:
            embed.add_field(
                name='Flinch',
                value='{} has flinched'.format(mon_b),
                inline=False
            )

        embed.set_footer(text='{}►{} | {}% | {}x | Gen 2 Crit. Hit'.format(
            mon_a, mon_b, round(random_value*100, 2), multiplier))
        _embeds.append(embed)
    return _embeds


def acc_value(acc):
    if acc == None:
        return 'Can\'t miss.'
    acc = int(acc)
    num = random()*100
    for i in range(9, 2, -1):
        if 3*acc/i >= num:
            return 'It hits. Dodgeable at +{}'.format(i-2)
    return 'It misses.'  # Dodgeable at +0


def crit_value():
    num = random()
    if num <= 1/16:
        return 'possible at +0.'
    elif num <= 1/8:
        return 'possible at +1.'
    elif num <= 1/4:
        return 'possible at +2.'
    elif num <= 1/3:
        return 'possible at +3.'
    elif num <= 1/2:
        return 'possible at +4.'
    else:
        return 'not possible in this turn.'
