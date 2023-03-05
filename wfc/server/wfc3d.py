import json
import random
from time import sleep,time
import sys

import models.Block
from models.Block import Block
from models.BlockSet import BlockSet
from models.Stadium import Stadium

sys.setrecursionlimit(10000) #there is propably to many recursion

blockSetList = {}

def loadBlockSetList():
    with open("/usr/files/blocksets/blockSetList3D.json", 'r') as f:
    #with open("../../data/files/blocksets/blockSetList3D.json", 'r') as f:
        setList = json.load(f)
    global blockSetList
    t = sorted(setList, key=lambda x: x['name'])

    for b in t:
        blockSetList[b['name']] = BlockSet(b)

    return "List has been updated !"

"""
TODO :
- custom size (x,z)
- define ground high (y)
- custom (x,z) start point (to map on from a specific position)
- set + subsets + custom weight
- already placed Tile (list of blockname, coord, dir)

"""
def run(nameofset, args = None):
    metric_start = time()
    loadBlockSetList()
    set = blockSetList[nameofset]
    if set is None:
       return "No set found."
    print(">> WFC >> Loading BlockSetList : "  + str(time() - metric_start))

    metric_start = time()
    stadium = Stadium(set)
    print(">> WFC >> Init Stadium grid : "  + str(time() - metric_start))

    metric_start = time()
    stadium.solve()
    print(">> WFC >> Solving Stadium : "  + str(time() - metric_start))
    return stadium.toJson()



### for local testing
print("start")
#print(run("GrassMountains"))
#print(run("GrassRoad"))
print("fin")
