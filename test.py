import os
from tinydb import TinyDB, Query

SCRIPT_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(SCRIPT_DIR, 'database/users.json')
DATABASE = TinyDB(FILE_PATH)
SEARCH = Query()
DATABASE.insert({'name':'Vincent', 'ID':0})
DATABASE.insert({'name':'Osamu', 'ID':1})
DATABASE.insert({'name':'Vincent', 'ID':2})
print(len(DATABASE.search(SEARCH.name == 'Mo')))