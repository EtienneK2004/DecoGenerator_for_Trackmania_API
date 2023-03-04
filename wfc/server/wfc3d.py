import json
import random
from time import sleep
import sys

import models.Block
from models.Block import Block
from models.BlockSet import BlockSet
from models.Stadium import Stadium

sys.setrecursionlimit(2000)

blockSetList = {}

def loadBlockSetList():
    with open("/usr/files/blocksets/blockSetList3D.json", 'r') as f:
        setList = json.load(f)
    global blockSetList
    t = sorted(setList, key=lambda x: x['name'])

    for b in t:
        blockSetList[b['name']] = BlockSet(b)

    return "List has been updated !"


def run(nameofset, args = None):
    loadBlockSetList()
    set = blockSetList[x]
    if set is None:
       return "No set found."

    stadium = Stadium(set)

    stadium.solve()
    return stadium.toJson()

