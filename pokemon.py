import math
import textwrap
import os
import pokebase as pb

def index_2d(_data, _search):
    for i, value in enumerate(_data):
        try:
            return i, value.index(_search)
        except ValueError:
            pass
    raise ValueError('{} is not in list'.format(repr(_search)))

class Calc:
    @staticmethod
    def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
        print('HP: {}'.format(10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))
        return 10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))

    @staticmethod
    def stat(_base, _lvl=100, _ivs=31, _evs=252, _nat=1.1):
        print('STAT: {}'.format(math.floor(_nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))))
        return math.floor(_nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))

    @staticmethod
    def attack_calc(_atk, _def, _pwr, _lvl=100, _mul=1, _crit=False):
        if _crit:
            _lvl *= 2
        return math.floor(_mul * (math.floor(math.floor(math.floor(2 * _lvl / 5 + 2) * _pwr * _atk / _def) / 50) + 2))
       
    @staticmethod
    def type_effectiveness(_attack=[], _name='typeless', _defense=[]):
        result = 1
        types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy', 'typeless']
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
        for _type in _defense:
            if _name in types and _type in types:
                val = chart[types.index(_name)][types.index(_type)]
                result *= val * 1.5 if _name in _attack else 1
        return result
    
    @staticmethod
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
        self._hp = Calc.hp_stat(data.stats[5].base_stat, _lvl, _ivs[0], _evs[0])
        self._attack = Calc.stat(data.stats[4].base_stat, _lvl, _ivs[1], _evs[1], _nature[0])
        self._defense = Calc.stat(data.stats[3].base_stat, _lvl, _ivs[2], _evs[2], _nature[1])
        self._sp_attack = Calc.stat(data.stats[2].base_stat, _lvl, _ivs[3], _evs[3], _nature[2])
        self._sp_defense = Calc.stat(data.stats[1].base_stat, _lvl, _ivs[4], _evs[4], _nature[3])
        self._speed = Calc.stat(data.stats[0].base_stat, _lvl, _ivs[5], _evs[5], _nature[4])
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
            + '\nATK: {}'.format(self._attack)
            + '\nDEF: {}'.format(self._defense)
            + '\nSP. ATK: {}'.format(self._sp_attack)
            + '\nSP. DEF: {}'.format(self._sp_defense)
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