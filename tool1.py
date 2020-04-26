import math
import json
import os
import textwrap


SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')

class Calc:
        
    @staticmethod
    def hp_stat(num=0):
        return 204+math.floor(2*num)
    
    @staticmethod
    def stat(num=0):
        return math.floor(1.1 * math.floor(2*num) + 0.9) + 108

with open(FILE_PATH, 'r') as f:
    DISTROS_DICT = json.load(f)

# DISTROS_DICT = DISTROS_DICT['Pokemon']['delphox']['base stats']

class Character:
    def __init__(self):
        self._name = 'Steve'
        self._species = ['']
        self._gender = ''
        self._types = ['']
        self._age = 0
        self._personality = ''
        self._occupation = ''
        self._likes = ''
        self._dislikes = ''
        self._height = 0
        self._weight = 0
        self._strenghts = ''
        self._weaknesses = ''
        self._sp_ability = ''
        self._image = ''

    def __str__(self):
        return """
        Species: {}
        Gender: {}
        Name: {}
        Type: {}
        Age: {}
        Personality: {}
        Occupation: {}
        Likes: {}
        Dislikes: {}
        -----   -----   -----
        Height: {}
        Weight: {}
        -----   -----   -----
        Strenghts: {}
        Weaknesses: {}
        |----- × ----- × ----- × -----|
        Ability: {}
        Special Ability: {}
        -----   -----   -----
        Backstory: {}
        -----   -----   -----Image:-----   -----   -----
        {}
        """.format()

class Pokemon:
    def __init__(self):
        self._name = 'MissingNO'
        self._hp = 0
        self._attack = 0
        self._defense = 0
        self._sp_attack = 0
        self._sp_defense = 0
        self._speed = 0
        self._abilities = []
        self._types = []
        self._height = 0
        self._weight = 0
    def __str__(self):
        return '\t'.join([
            self._name,
            self._hp,
            self._attack,
            self._defense,
            self._sp_attack,
            self._sp_defense,
            self._speed,
            ', '.join(self._abilities),
            ', '.join(self._types),
            self._height,
            self._weight
        ])

class ListPokemon:
    def __init__(self):
        self.ocs = []
    def add_oc(self):
        character = Pokemon()
        self.ocs.append(character)
    def view_inventory(self):
        print('\t'.join(['', 'NAME', 'HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPEED']))
        for idx, character in enumerate(self.ocs):
            print(idx + 1, end='\t')
            print(character)


LIST = ListPokemon()

# for POKEMON in DISTROS_DICT['Pokemon']:
    # AUX = DISTROS_DICT['Pokemon'][POKEMON]['base stats']
    # print("-----{}-----".format(POKEMON))
    # print("HP: {}".format(Calc.hp_stat(AUX['HP'])))
    # print("ATK: {}".format(Calc.stat(AUX['Attack'])))
    # print("DEF: {}".format(Calc.stat(AUX['Defense'])))
    # print("SP. ATK: {}".format(Calc.stat(AUX['Sp. Attack'])))
    # print("SP. DEF: {}".format(Calc.stat(AUX['Sp. Defense'])))
    # print("SPEED: {}".format(Calc.stat(AUX['Speed'])))
    # print("ABILITIES: {}".format(", ".join(DISTROS_DICT['Pokemon'][POKEMON]['abilities'])))
    # print("TYPES: {}".format(", ".join(DISTROS_DICT['Pokemon'][POKEMON]['types'])))
    # print("WEIGHT: {}".format(int(DISTROS_DICT['Pokemon'][POKEMON]['weight'])))
    # print("HEIGHT: {}".format(int(DISTROS_DICT['Pokemon'][POKEMON]['height'])))

# print(json.dumps(DISTROS_DICT, indent=4, sort_keys=True))

print("""Species: {}
        \nGender: {}
        Name: {}
        Type: {}
        Age: {}
        Personality: {}
        Occupation: {}
        Likes: {}
        Dislikes: {}
        -----   -----   -----
        Height: {}
        Weight: {}
        -----   -----   -----
        Strenghts: {}
        Weaknesses: {}
        |----- × ----- × ----- × -----|
        Ability: {}
        Special Ability: {}
        -----   -----   -----
        Backstory: {}
        -----   -----   -----Image:-----   -----   -----
        {}
        """.format(range(17))
    )