import math
import json
import os
import textwrap


SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')

class Calc:
        
    @staticmethod
    def hp_stat(_base, _lvl=100, _ivs=31, _evs=252):
        # return 204+math.floor(2*_num)
        return 10 + math.floor( _lvl * (_base/50 + _evs/400 + _ivs/100 + 1) )
    
    @staticmethod
    def stat(_base, _lvl=100, _ivs=31, _evs=252, _nat=1.1):
        # return math.floor(1.1 * math.floor(2*_base) + 0.9) + 108
        return math.floor(_nat * (5 + math.floor( _lvl * (_base/50 + _evs/400 + _ivs/100 + 1) )))

    @staticmethod
    def attackCalc(_atk, _def, _pwr, _lvl=100, _crit=False, _mul=1):
        if _crit:
            _lvl = _lvl*2
        return math.floor( (2 + (_atk * _lvl * _pwr)/(125 * _def) + (_atk * _pwr)/(25 * _def) ) * _mul)

with open(FILE_PATH, 'r') as f:
    DISTROS_DICT = json.load(f)

# DISTROS_DICT = DISTROS_DICT['Pokemon']['delphox']['base stats']

class Character:
    def __init__(self):
        self._name = 'Steve'
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

class Pokemon:
    def __init__(self, name, hp, attack, defense, sp_attack, sp_defense, speed, abilities, types, height, weight):
        self._name = name
        self._hp = Calc.hp_stat(hp)
        self._attack = Calc.stat(attack)
        self._defense = Calc.stat(defense)
        self._sp_attack = Calc.stat(sp_attack)
        self._sp_defense = Calc.stat(sp_defense)
        self._speed = Calc.stat(speed)
        self._abilities = abilities
        self._types = types
        self._height = int(height)
        self._weight = int(weight)
    def __repr__(self):
        return(
            '\n-----{}-----'.format(self._name)
            +'\nHP: {}'.format(self._hp)
            +'\nATK: {}'.format(self._attack)
            +'\nDEF: {}'.format(self._defense)
            +'\nSP. ATK: {}'.format(self._sp_attack)
            +'\nSP. DEF: {}'.format(self._sp_defense)
            +'\nSPEED: {}'.format(self._speed)
            +'\nABILITIES: {}'.format(", ".join(self._abilities))
            +'\nTYPES: {}'.format(", ".join(self._types))
            +'\nWEIGHT: {}'.format(self._weight)
            +'\nHEIGHT: {}'.format(self._height)
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
            self._weight,
            self._height
        )

class ListPokemon:
    def __init__(self):
        self.ocs = []
    def add_oc(self, name):
        AUX = DISTROS_DICT['Pokemon'][name]
        character = Pokemon(
            name,
            AUX['base stats']['HP'],
            AUX['base stats']['Attack'],
            AUX['base stats']['Defense'],
            AUX['base stats']['Sp. Attack'],
            AUX['base stats']['Sp. Defense'],
            AUX['base stats']['Speed'],
            AUX['abilities'],
            AUX['types'],
            AUX['weight'],
            AUX['height']
        )
        self.ocs.append(character)

    def view_inventory(self):
        for character in self.ocs:
            print(character)

A = DISTROS_DICT['Pokemon']['axew']['base stats']
LA = 5
HP = Calc.hp_stat(A['HP'], LA)
ATK = Calc.stat(A['Attack'], LA)
DEF = Calc.stat(A['Defense'], LA)

B = DISTROS_DICT['Pokemon']['delphox']['base stats']
LB = 100
HP2 = Calc.hp_stat(B['HP'], LB)
ATK2 = Calc.stat(B['Attack'], LB)
DEF2 = Calc.stat(B['Defense'], LB)

print(ATK)
print(DEF)
print(ATK2)
print(DEF2)

print('HP: {}'.format(HP))
print('HP-: {}'.format(Calc.attackCalc(ATK2, DEF, 40, LB, False, 1.3*2)))
print('HP: {}'.format(HP2))
print('HP-: {}'.format(Calc.attackCalc(ATK, DEF2, 40, LA, False, 0.5*1.3)))

#LIST = ListPokemon()

#for POKEMON in DISTROS_DICT['Pokemon']:
    #LIST.add_oc(POKEMON)

#file = open('data.csv','w')
#for OC in LIST.ocs:
#    file.write(str(OC)+'\n')

#file.close