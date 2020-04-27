import math
import json
import os
import textwrap
import csv
import sys

# SCRIPT_DIR = os.path.dirname(__file__)
#  FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')

class Calc:
    @staticmethod
    def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
        # return 204+math.floor(2*_num)
        return 10 + math.floor(_lvl * (_base/50 + _evs/400 + _ivs/100 + 1) )
    @staticmethod
    def stat(_base, _lvl=100, _ivs=31, _evs=252, _nat=1.1):
        # return math.floor(1.1 * math.floor(2*_base) + 0.9) + 108
        return math.floor(_nat * (5 + math.floor( _lvl * (_base/50 + _evs/400 + _ivs/100 + 1) )))
    @staticmethod
    def attackCalc(_atk, _def, _pwr, _lvl=100, _mul=1, _crit=False):
        if _crit:
            _lvl = _lvl*2
        return math.floor((2 + (_atk * _lvl * _pwr)/(125 * _def) + (_atk * _pwr)/(25 * _def) ) * _mul)

# with open(FILE_PATH, 'r') as f:
    # DISTROS_DICT = json.load(f)

# DISTROS_DICT = DISTROS_DICT['Pokemon']['delphox']['base stats']

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
            +'\nSpecies: {0}'.format(', '.join(self._species))
            +'\nGender: {}'.format(self._gender)
            +'\nName: {}'.format(self._name)
            +'\nType: {}'.format(', '.join(self._types))
            +'\nAge: {}'.format(self._age)
            +'\nPersonality: {}'.format(wrapper.fill(self._personality))
            +'\n\nOccupation: {}'.format(wrapper.fill(self._occupation))
            +'\n\nLikes: {}'.format(wrapper.fill(self._likes))
            +'\n\nDislikes: {}'.format(wrapper.fill(self._dislikes))
            +'\n\n-----   -----   -----'
            +'\nHeight: {}'.format(self._height)
            +'\nWeight: {}'.format(self._weight)
            +'\n-----   -----   -----'
            +'\nStrenghts: {}'.format(wrapper.fill(self._strenghts))
            +'\n\nWeaknesses: {}'.format(wrapper.fill(self._weaknesses))
            +'\n\n|----- × ----- × ----- × -----|'
            +'\nAbility: {}'.format(', '.join(self._abilities))
            +'\n\nSpecial Ability: {}'.format(wrapper.fill(self._species))
            +'\n-----   -----   -----'
            +'\nBackstory: {}'.format(wrapper.fill(self._backstory))
            +'\n-----   -----   -----Image:-----   -----   -----'
            +'\n{}'.format(self._image)
        )

csv_file = csv.reader(open('data.csv','r'),delimiter=';')

for data in csv_file:
    if data[0] == 'delphox':
        HP = int(data[1])
        ATK = int(data[2])
        DEF = int(data[3])
    if data[0] == 'axew':
        HP2 = int(data[1])
        ATK2 = int(data[2])
        DEF2 = int(data[3])

print(HP)
print(ATK)
print(DEF)
print(HP2)
print(ATK2)
print(DEF2)

print('HP: {}'.format(HP))
print('HP-: {}'.format(Calc.attackCalc(ATK2, DEF, 40, 100, 1.3*0.5)))
print('HP: {}'.format(HP2))
print('HP-: {}'.format(Calc.attackCalc(ATK, DEF2, 40, 100, 1.3*2*1.5)))

#LIST = ListPokemon()

#for POKEMON in DISTROS_DICT['Pokemon']:
    #LIST.add_oc(POKEMON)

#file = open('data.csv','w')
#for OC in LIST.ocs:
#    file.write(str(OC)+'\n')

#file.close