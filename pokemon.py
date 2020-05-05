import math
import textwrap
from random import randint, random
import discord
import pokebase as pb


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


def battle(mon_a: str, mon_b: str, move: str, multiplier=1.0, level_a=100, level_b=100):
    aux1 = pb.pokemon(mon_a.lower())
    aux2 = pb.pokemon(mon_b.lower())
    aux3 = pb.move(move.lower())
    types1 = []
    types2 = []
    _embeds = []
    for item in aux1.types:
        types1.append(item.type.name)
    for item in aux2.types:
        types2.append(item.type.name)
    hp_value = hp_stat(aux2.stats[5].base_stat, level_b)
    immune = False
    multiplier *= type_effectiveness(
        types1, aux3.type.name, types2)
    if aux3.damage_class.name == 'special':
        atk_value = stat(aux1.stats[2].base_stat, level_a)
        if move.lower() in ['psyshock', 'psystrike', 'secret-sword']:
            def_value = stat(aux2.stats[3].base_stat, level_b)
        else:
            def_value = stat(aux2.stats[1].base_stat, level_b)
    if aux3.damage_class.name == 'physical':
        atk_value = stat(aux1.stats[4].base_stat, level_a)
        def_value = stat(aux2.stats[3].base_stat, level_b)

    min_value = aux3.meta.min_hits if aux3.meta.min_hits is not None else 1
    max_value = aux3.meta.max_hits if aux3.meta.min_hits is not None else 1
    for i in range(randint(min_value, max_value)):
        random_value = randint(85, 100)/100
        embed = discord.Embed(colour=discord.Colour.dark_red())
        embed.set_author(name=move.lower())
        embed.add_field(
            name='{}: {}'.format(move.lower(), i),
            value='{}'.format(aux3.effect_entries[0].short_effect).replace(
                '$effect_chance%', '{}%'.format(aux3.effect_chance)
            ),
            inline=False
        )
        if immune:
            embed.add_field(
                name='Type',
                value='{} is immune often.'.format(mon_b),
                inline=False
            )
        if aux3.damage_class.name != 'status' and aux3.meta.category.name != 'ohko':
            dmg_value_a = attack_calc(
                atk_value, def_value, aux3.power, level_a, multiplier*random_value, False)
            dmg_value_b = attack_calc(
                atk_value, def_value, aux3.power, level_a, multiplier*random_value, True)
            embed.add_field(
                name='Acc roll',
                value='{}\n{}'.format(acc_value(aux3.accuracy), crit_value()),
                inline=False
            )
            embed.add_field(
                name='Damage',
                value='{} = {}%'.format(
                    dmg_value_a, round(dmg_value_a * 100 / hp_value, 2)
                ),
                inline=False
            )
            embed.add_field(
                name='Crit. hit. damage',
                value='{} = {}%'.format(
                    dmg_value_b, round(dmg_value_b * 100 / hp_value, 2)
                ),
                inline=False
            )
        else:
            embed.add_field(
                name='Acc roll',
                value='{}'.format(acc_value(aux3.accuracy)),
                inline=False
            )

        if aux3.meta.ailment_chance != 0 and random() <= aux3.meta.ailment_chance/100:
            embed.add_field(
                name='Effect Roll',
                value='{} got [{}] unless prevented'.format(
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
            embed.add_field(
                name='Healed HP',
                value='+{}.'.format(round(hp_value / 100 *aux3.meta.healing, 2)),
                inline=False
            )

        if aux3.meta.flinch_chance != 0 and random() <= aux3.meta.flinch_chance/100:
            embed.add_field(
                name='Flinch',
                value='{} has flinched'.format(mon_b),
                inline=False
            )

        embed.set_footer(text='{}►{} | {}% | {}x'.format(
            mon_a, mon_b, round(random_value*100, 2), multiplier))
        _embeds.append(embed)
    return _embeds


def acc_value(acc):
    if acc == 'None':
        return 'Can\'t miss.'
    acc = int(acc)
    num = random()*100
    for i in range(9, 2, -1):
        if 3*acc/i >= num:
            return 'It hits. Dodgeable at +{}'.format(i-2)
    return 'It misses.'  # Dodgeable at +0


def crit_value():
    num = randint(1, 16)
    if num == 1:
        return 'Critical Hit.'
    for i in range(1, 5):
        if num <= 2*i:
            return 'Critical Hit at +{}.'.format(i)
    return 'Not critical Hit.'


def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
    print('HP: {}'.format(10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))
    return 10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))


def stat(_base, _lvl=100, _ivs=31, _evs=252, _nat=1.1):
    print('STAT: {}'.format(math.floor(
        _nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))))
    return math.floor(_nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))


def attack_calc(_atk_value, _def_value, _pwr, _lvl=100, _mul=1, _crit=False):
    if _crit:
        _lvl *= 2
    return math.floor(
        _mul * (math.floor(math.floor(math.floor(2 * _lvl / 5 + 2)
                                      * _pwr * _atk_value / _def_value) / 50) + 2)
    )


def type_effectiveness(_attack=None, _name='typeless', _def_valueense=None):
    if _attack is None:
        _attack = ['typeless']
    if _def_valueense is None:
        _def_valueense = ['typeless']
    result = 1
    types = [
        'normal', 'fire', 'water', 'electric', 'grass',
        'ice', 'fighting', 'poison', 'ground', 'flying',
        'psychic', 'bug', 'rock', 'ghost', 'dragon',
        'dark', 'steel', 'fairy', 'typeless'
    ]
    chart = [
        [1, 1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	0.5,	0,	1,	1,	0.5,	1],
        [1, 0.5,	0.5,	1,	2,	2,	1,	1,	1,	1,	1,	2,	0.5,	1,	0.5,	1,	2,	1],
        [1, 2,	0.5,	1,	0.5,	1,	1,	1,	2,	1,	1,	1,	2,	1,	0.5,	1,	1,	1],
        [1, 1,	2,	0.5,	0.5,	1,	1,	1,	0,	2,	1,	1,	1,	1,	0.5,	1,	1,	1],
        [1, 0.5,	2,	1,	0.5,	1,	1,	0.5,	2,	0.5,	1,	0.5,	2,	1,	0.5,	1,	0.5,	1],
        [1, 0.5,	0.5,	1,	2,	0.5,	1,	1,	2,	2,	1,	1,	1,	1,	2,	1,	0.5,	1],
        [2, 1,	1,	1,	1,	2,	1,	0.5,	1,	0.5,	0.5,	0.5,	2,	0,	1,	2,	2,	0.5],
        [1, 1,	1,	1,	2,	1,	1,	0.5,	0.5,	1,	1,	1,	0.5,	0.5,	1,	1,	0,	2],
        [1, 2,	1,	2,	0.5,	1,	1,	2,	1,	0,	1,	0.5,	2,	1,	1,	1,	2,	1],
        [1, 1,	1,	0.5,	2,	1,	2,	1,	1,	1,	1,	2,	0.5,	1,	1,	1,	0.5,	1],
        [1, 1,	1,	1,	1,	1,	2,	2,	1,	1,	0.5,	1,	1,	1,	1,	0,	0.5,	1],
        [1, 0.5,	1,	1,	2,	1,	0.5,	0.5,	1,	0.5,	2,	1,	1,	0.5,	1,	2,	0.5,	0.5],
        [1, 2,	1,	1,	1,	2,	0.5,	1,	0.5,	2,	1,	2,	1,	1,	1,	1,	0.5,	1],
        [0, 1,	1,	1,	1,	1,	1,	1,	1,	1,	2,	1,	1,	2,	1,	0.5,	1,	1],
        [1, 1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	2,	1,	0.5,	0],
        [1, 1,	1,	1,	1,	1,	0.5,	1,	1,	1,	2,	1,	1,	2,	1,	0.5,	1,	0.5],
        [1, 0.5,	0.5,	0.5,	1,	2,	1,	1,	1,	1,	1,	1,	2,	1,	1,	1,	0.5,	2],
        [1, 0.5,	1,	1,	1,	1,	2,	0.5,	1,	1,	1,	1,	1,	1,	2,	2,	0.5,	1],
        [1, 1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1,	1]
    ]
    for _type in _def_valueense:
        if _name in types and _type in types:
            val = chart[types.index(_name)][types.index(_type)]
            result *= val * 1.5 if _name in _attack else 1
    return result


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


class Character:
    def __init__(self, name):
        self._name = name
        self._species = []
        self._gender = ''
        self._types = []
        self._age = 0
        self._personality = ''
        self._occupation = ''
        self._likes = ''
        self._dislikes = ''
        self._height = 0
        self._weight = 0
        self._strenghts = ''
        self._weaknesses = ''
        self._abilities = []
        self._sp_ability = ''
        self._backstory = ''
        self._image = ''

    def __str__(self):
        wrapper = textwrap.TextWrapper(width=50)
        return(
            '|----- × ----- × ----- × -----|'
            + '\n**Species:** {0}'.format(', '.join(self._species))
            + '\n**Gender:** {}'.format(self._gender)
            + '\n**Name:** {}'.format(self._name)
            + '\n**Type:** {}'.format(', '.join(self._types))
            + '\n**Age:** {}'.format(self._age)
            + '\n**Personality:** {}'.format(wrapper.fill(self._personality))
            + '\n\n**Occupation:** {}'.format(wrapper.fill(self._occupation))
            + '\n\n**Likes:** {}'.format(wrapper.fill(self._likes))
            + '\n\n**Dislikes:** {}'.format(wrapper.fill(self._dislikes))
            + '\n\n**-----   -----   -----'
            + '\n**Height:** {}'.format(self._height)
            + '\n**Weight:** {}'.format(self._weight)
            + '\n-----   -----   -----'
            + '\n**Strenghts:** {}'.format(wrapper.fill(self._strenghts))
            + '\n\n**Weaknesses:** {}'.format(wrapper.fill(self._weaknesses))
            + '\n\n|----- × ----- × ----- × -----|'
            + '\n**Ability:** {}'.format(', '.join(self._abilities))
            + '\n\n**Special Ability:** {}'.format(wrapper.fill(self._species))
            + '\n-----   -----   -----'
            + '\n**Backstory:** {}'.format(wrapper.fill(self._backstory))
            + '\n-----   -----   -----Image:-----   -----   -----'
            + '\n{}'.format(self._image)
        )


class Pokemon:
    def __init__(self, _name, _lvl=100, _ivs=None, _evs=None, _nature=None):
        if _ivs is None:
            _ivs = [31]*6
        if _evs is None:
            _evs = [252]*6
        if _nature is None:
            _nature = [1.1]*5
        data = pb.pokemon(_name)
        self._name = _name
        self._hp = hp_stat(data.stats[5].base_stat, _lvl, _ivs[0], _evs[0])
        self._attack = stat(
            data.stats[4].base_stat, _lvl, _ivs[1], _evs[1], _nature[0])
        self._defense = stat(
            data.stats[3].base_stat, _lvl, _ivs[2], _evs[2], _nature[1])
        self._sp_attack = stat(
            data.stats[2].base_stat, _lvl, _ivs[3], _evs[3], _nature[2])
        self._sp_defense = stat(
            data.stats[1].base_stat, _lvl, _ivs[4], _evs[4], _nature[3])
        self._speed = stat(data.stats[0].base_stat,
                           _lvl, _ivs[5], _evs[5], _nature[4])
        self._abilities = []
        for item in data.abilities:
            self._abilities.append(item.ability.name)
        self._types = []
        for item in data.types:
            self._abilities.append(item.type.name)
        self._height = data.height
        self._weight = data.weight

    def __repr__(self):
        return(
            '\n-----{}-----'.format(self._name)
            + '\nHP: {}'.format(self._hp)
            + '\natk_value: {}'.format(self._attack)
            + '\ndef_value: {}'.format(self._defense)
            + '\nSP. atk_value: {}'.format(self._sp_attack)
            + '\nSP. def_value: {}'.format(self._sp_defense)
            + '\nSPEED: {}'.format(self._speed)
            + '\nABILITIES: {}'.format(', '.join(self._abilities))
            + '\nTYPES: {}'.format(', '.join(self._types))
            + '\nWEIGHT: {}'.format(self._weight)
            + '\nHEIGHT: {}'.format(self._height)
        )

    def __str__(self):
        return '{};{};{};{};{};{};{};{};{};{};{}'.format(
            self._name,
            self._hp,
            self._attack,
            self._defense,
            self._sp_attack,
            self._sp_defense,
            self._speed,
            '|'.join(self._abilities),
            '|'.join(self._types),
            self._height,
            self._weight,
        )


class ListPokemon:
    def __init__(self):
        self.ocs = []

    def add_oc(self, name):
        character = Pokemon(name)
        self.ocs.append(character)

    def view_inventory(self):
        for character in self.ocs:
            print(character)
