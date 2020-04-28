import math
import json
import os
import textwrap
import csv

SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')


class Methods:
    @staticmethod
    def index_2d(_data, _search):
        for i, value in enumerate(_data):
            try:
                return i, value.index(_search)
            except ValueError:
                pass
        raise ValueError("{} is not in list".format(repr(_search)))


class Calc:
    @staticmethod
    def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
        return 10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))

    @staticmethod
    def stat(_base, _lvl=100, _ivs=31, _evs=252, _nat=1.1):
        return math.floor(_nat * (5 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1))))

    @staticmethod
    def attackCalc(_atk, _def, _pwr, _lvl=100, _mul=1, _crit=False):
        if _crit:
            _lvl *= 2
        return math.floor((2 + (_atk * _lvl * _pwr)/(125 * _def) + (_atk * _pwr)/(25 * _def)) * _mul)

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
        coords = Methods.index_2d(natures, _name)
        result[coords[0]] -= 0.1
        result[coords[1]] += 0.1
        return result


with open(FILE_PATH, 'r') as f:
    DISTROS_DICT = json.load(f)


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
        data = DISTROS_DICT['Pokemon'][_name]
        self._name = _name
        self._hp = Calc.hp_stat(
            data['base stats']['HP'], _lvl, _ivs[0], _evs[0])
        self._attack = Calc.stat(
            data['base stats']['Attack'], _lvl, _ivs[1], _evs[1], _nature[0])
        self._defense = Calc.stat(
            data['base stats']['Defense'], _lvl, _ivs[2], _evs[2], _nature[1])
        self._sp_attack = Calc.stat(
            data['base stats']['Sp. Attack'], _lvl, _ivs[3], _evs[3], _nature[2])
        self._sp_defense = Calc.stat(
            data['base stats']['Sp. Defense'], _lvl, _ivs[4], _evs[4], _nature[3])
        self._speed = Calc.stat(
            data['base stats']['Speed'], _lvl, _ivs[5], _evs[5], _nature[4])
        self._abilities = data['abilities']
        self._types = data['types']
        self._height = int(data['height'])
        self._weight = int(data['weight'])

    def __repr__(self):
        return(
            '\n-----{}-----'.format(self._name)
            + '\nHP: {}'.format(self._hp)
            + '\nATK: {}'.format(self._attack)
            + '\nDEF: {}'.format(self._defense)
            + '\nSP. ATK: {}'.format(self._sp_attack)
            + '\nSP. DEF: {}'.format(self._sp_defense)
            + '\nSPEED: {}'.format(self._speed)
            + '\nABILITIES: {}'.format(", ".join(self._abilities))
            + '\nTYPES: {}'.format(", ".join(self._types))
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


csv_file = csv.reader(open('data.csv', 'r'), delimiter=';')

# for data in csv_file:
# if data[0] == 'delphox':
# HP = int(data[1])
# ATK = int(data[2])
# DEF = int(data[3])
# # # SATK = int(data[4])
# SDEF = int(data[5])
# if data[0] == 'sylveon':
# HP2 = int(data[1])
# ATK2 = int(data[2])
# DEF2 = int(data[3])
# SATK2 = int(data[4])
# SDEF2 = int(data[5])

LIST = ListPokemon()
for POKEMON in DISTROS_DICT['Pokemon']:
    LIST.add_oc(POKEMON)

file = open('data.csv', 'w')
for OC in LIST.ocs:
    file.write(str(OC)+'\n')

file.close
