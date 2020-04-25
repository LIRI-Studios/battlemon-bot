import math
import json
import os


SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/database.json')


def hp_stat(num=0):
    return 204+math.floor(2*num)


def stat(num=0):
    return math.floor(1.1 * math.floor(2*num) + 0.9) + 108


with open(FILE_PATH, 'r') as f:
    DISTROS_DICT = json.load(f)

# DISTROS_DICT = DISTROS_DICT['Pokemon']['delphox']['base stats']

class Pokemon:
    def __init__(self, name):
        self.name = name

for POKEMON in DISTROS_DICT['Pokemon']:
    AUX = DISTROS_DICT['Pokemon'][POKEMON]['base stats']
    print("-----{}-----".format(POKEMON))
    print("HP: {}".format(hp_stat(AUX['HP'])))
    print("ATK: {}".format(stat(AUX['Attack'])))
    print("DEF: {}".format(stat(AUX['Defense'])))
    print("SP. ATK: {}".format(stat(AUX['Sp. Attack'])))
    print("SP. DEF: {}".format(stat(AUX['Sp. Defense'])))
    print("SPEED: {}".format(stat(AUX['Speed'])))
    print("ABILITIES: {}".format(", ".join(DISTROS_DICT['Pokemon'][POKEMON]['abilities'])))
    print("TYPES: {}".format(", ".join(DISTROS_DICT['Pokemon'][POKEMON]['types'])))
    print("WEIGHT: {}".format(int(DISTROS_DICT['Pokemon'][POKEMON]['weight'])))
    print("HEIGHT: {}".format(10*int(DISTROS_DICT['Pokemon'][POKEMON]['height'])))

# print(json.dumps(DISTROS_DICT, indent=4, sort_keys=True))
