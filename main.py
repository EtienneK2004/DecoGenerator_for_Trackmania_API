from flask import Flask
import json
import random
import pygame
from time import sleep






TILE_SIZE = 15
Y_AXIS_FOR_2D = 9
MAX_XZ_STAD = 48

taille = (TILE_SIZE*MAX_XZ_STAD,TILE_SIZE*MAX_XZ_STAD)

"""
pygame.init()
pygame.display.set_caption('Graphic Debug for Decogen')
surface = pygame.display.set_mode(taille)
"""

def draw_block(coo, name):
    return
    for event in pygame.event.get():
        a = 1
    co = [0,0,0]
    co[0], co[2] = coo[0]*TILE_SIZE, coo[2]*TILE_SIZE


    if name == None:
        pygame.draw.rect(surface, (50,50,50), pygame.Rect(co[0], co[2], TILE_SIZE, TILE_SIZE))
        return
    name, dir = name.split('_')
    if name == 'DecoPlatformBase':
        r = pygame.Rect(co[0], co[2], TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, (250,150,15), r)

    if name == 'OpenTechRoadStraight':
        if dir in ('North', 'South'):
            r1 = pygame.Rect(co[0], co[2], TILE_SIZE, TILE_SIZE)
            r2 = pygame.Rect(co[0]+TILE_SIZE/3, co[2], TILE_SIZE/3, TILE_SIZE)
            pygame.draw.rect(surface, (250,150,15), r1)
            pygame.draw.rect(surface, (200,200,200), r2)
        else:
            r1 = pygame.Rect(co[0], co[2], TILE_SIZE, TILE_SIZE)
            r2 = pygame.Rect(co[0], co[2]+TILE_SIZE/3, TILE_SIZE,TILE_SIZE/3)
            pygame.draw.rect(surface, (250,150,15), r1)
            pygame.draw.rect(surface, (200,200,200), r2)

    if name == 'OpenTechRoadCurve1':
        r1 = pygame.Rect(co[0], co[2], TILE_SIZE, TILE_SIZE)
        r2 = pygame.Rect(co[0]+TILE_SIZE/3, co[2]+TILE_SIZE/3, TILE_SIZE/3, TILE_SIZE/3)
        pygame.draw.rect(surface, (250,150,15), r1)
        pygame.draw.rect(surface, (200,200,200), r2)
        if dir in ('North', 'East'):
            r3 = pygame.Rect(co[0], co[2]+TILE_SIZE/3, TILE_SIZE/3, TILE_SIZE/3)
            pygame.draw.rect(surface, (200,200,200), r3)
        if dir in ('South', 'East'):
            r3 = pygame.Rect(co[0]+TILE_SIZE/3, co[2], TILE_SIZE/3, TILE_SIZE/3)
            pygame.draw.rect(surface, (200,200,200), r3)
        if dir in ('South', 'West'):
            r3 = pygame.Rect(co[0]+TILE_SIZE*2/3, co[2]+TILE_SIZE/3, TILE_SIZE/3, TILE_SIZE/3)
            pygame.draw.rect(surface, (200,200,200), r3)
        if dir in ('North', 'West'):
            r3 = pygame.Rect(co[0]+TILE_SIZE/3, co[2]+TILE_SIZE*2/3, TILE_SIZE/3, TILE_SIZE/3)
            pygame.draw.rect(surface, (200,200,200), r3)
    if coo[0] == 0:
        r = pygame.Rect(co[0], co[2], TILE_SIZE/3, TILE_SIZE/3)
        pygame.draw.rect(surface, (255, 0, 0), r)
    if coo[2] == 0:
        r = pygame.Rect(co[0], co[2], TILE_SIZE/3, TILE_SIZE/3)
        pygame.draw.rect(surface, (0, 0, 255), r)
    pygame.display.flip()





def add_dir(baseDir, relativeDir):
    dirs = ['North', 'East', 'South', 'West']
    return dirs[(dirs.index(baseDir) + dirs.index(relativeDir))%4]

def opposite_dir(dir):
    dirs = ['North', 'East', 'Top', 'South', 'West', 'Bottom']
    return dirs[(dirs.index(dir)+3)%6]


def rotate_block(Blockname, dir):

    return Blockname.split('_')[0] + '_' + add_dir(Blockname.split('_')[1], dir)

def sub_dir(first, second):
    dirs = ['North', 'East', 'South', 'West']
    return dirs[(dirs.index(first) - dirs.index(second))%4]

def dir_from_coords(basecoords, coords):
    if basecoords[0] < coords[0]:
        return "West"
    if basecoords[1] < coords[1]:
        return "Top"
    if basecoords[2] < coords[2]:
        return "North"
    if basecoords[0] > coords[0]:
        return "East"
    if basecoords[1] > coords[1]:
        return "Bottom"
    return "South"





class Block:
    name = ""
    weight = 0
    possibleBlocks = None
    def __init__(self, blDict, rotation, blockset):
        bDict = dict(blDict)
        self.possibleBlocks = {}
        dirs = ['North', 'East', 'South', 'West']
        self.name = bDict['name'] + "_" + rotation
        self.weight = bDict['weight']
        self.possibleBlocks[add_dir("North", rotation)] = self.possible_blocks_side(bDict['north'], 'North', blockset)
        self.possibleBlocks[add_dir("East", rotation)] = self.possible_blocks_side(bDict['east'], 'East', blockset)
        self.possibleBlocks[add_dir("South", rotation)] = self.possible_blocks_side(bDict['south'], 'South', blockset)
        self.possibleBlocks[add_dir("West", rotation)] = self.possible_blocks_side(bDict['west'], 'West', blockset)


        for d in dirs:
            for i in range(len(self.possibleBlocks[d])):
                self.possibleBlocks[d][i] = rotate_block(self.possibleBlocks[d][i], rotation)


    def possible_blocks_side(self, sidename, dir, blockSetJson):
        blocks = []
        for block in blockSetJson['blocks']:
            for rotation in ['North', 'East', 'South', 'West']:
                if block[sub_dir(dir, rotation).lower()] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name']+"_"+opposite_dir(rotation))
        return blocks




class BlockSet:
    listBlocks = None
    name = ""
    dimensions = 0
    def __init__(self, BlockSetJson):
        self.listBlocks = {}
        self.name = BlockSetJson['name']
        self.dimensions = BlockSetJson['dimensions']
        for b in BlockSetJson['blocks']:
            dirs = ['North', 'East', 'South', 'West']
            for d in dirs:
                blocko = Block(b, d, BlockSetJson)
                namoblocko = b['name']+'_'+d
                self.listBlocks[namoblocko] = blocko


    def get_random_block(self, listOfBlocknames):
        listWeight = []
        totalW = 0
        for block in listOfBlocknames:
            b = self.listBlocks[block]
            listWeight.append((block, b.weight))
            totalW += b.weight

        r = random.randint(1, totalW)
        cptW = 0
        for block in listWeight:
            cptW += block[1]
            if r <= cptW:
                return block[0]



    def get_all_blocks(self):
        return self.listBlocks.values()


    def get_all_blocknames(self):
        allblocks = self.get_all_blocks()
        allblocknames = []
        for block in allblocks:
            allblocknames.append(block.name)
        return allblocknames



    def possible_blocks_near(self, blockname, dir, basedir=None):
        if basedir is None:
            return self.listBlocks[blockname].possibleBlocks[dir]
        #return list(map(lambda x : rotate_block(x, dir),   self.listBlocks[blockname].possibleBlocks[add_dir(basedir, dir)]))





    def get_name(self):
        return self.name





class Stadium:
    tiles = None # Key is a tuple of 3 int (coordinates)
    blockSet = None

    def __init__(self, BlockSet):
        self.tiles = {}
        self.blockSet = BlockSet
        if BlockSet.dimensions == 2:
            for x in range(MAX_XZ_STAD):
                for z in range(MAX_XZ_STAD):
                    self.add_tile((x, Y_AXIS_FOR_2D, z))

    def add_tile(self, coords3D):
        self.tiles[coords3D] = Tile(self.blockSet.get_all_blocknames())


    def is_coords_out_of_stadium(self, coords):
        return coords[0] > (MAX_XZ_STAD-1) or coords[1] > 31 or coords[2] > (MAX_XZ_STAD-1) or coords[0] < 0 or coords[1] < 9 or coords[2] < 0


    def get_superpositions(self, coords3D):
        return self.tiles[coords3D].get_superpositions()


    def collapse(self, coords3D, superposition=None):
        if superposition is None:
            superposition = self.blockSet.get_random_block(self.tiles[coords3D].get_superpositions())

        self.tiles[coords3D].force_collapse(superposition)
        draw_block(coords3D, self.tiles[coords3D].collapse)
        a = self.neighbours_of_coords(coords3D, dimensions=2)

        for n in a:
            self.refresh_tile(n)



    def neighbours_of_coords(self, coords3D, dimensions=3):
        listn = []
        if dimensions > 1:
            listn.append((coords3D[0],coords3D[1], coords3D[2]+1))
            listn.append((coords3D[0]-1,coords3D[1], coords3D[2]))
            listn.append((coords3D[0],coords3D[1], coords3D[2]-1))
            listn.append((coords3D[0]+1,coords3D[1], coords3D[2]))


        if dimensions > 2:
            listn.append((coords3D[0],coords3D[1]+1, coords3D[2]))
            listn.append((coords3D[0],coords3D[1]-1, coords3D[2]))

        rmv = []

        for i in range(len(listn)):
            if self.is_coords_out_of_stadium(listn[i]):
                rmv.append(listn[i])

        for i in rmv:
            listn.remove(i)

        return listn


    def can_Block_be_at_Direction_of_Tile(self, blockname, dir, coords):

        for b in self.tiles[coords].get_superpositions():

            if blockname in self.blockSet.possible_blocks_near(b, dir):
                return True

        return False


    def refresh_tile(self, coords3D):
        # For each superposition, keep it if all neighbours have a superposition allowing it
        # If a change was made, refresh neighbours
        keeps = []
        change = False
        for superpos in self.tiles[coords3D].get_superpositions():
            keep = True
            idir = 2
            for n in self.neighbours_of_coords(coords3D, dimensions=2):
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dir_from_coords(n, coords3D), n):

                    keep = False
                    change = True
                    break



            if keep:
                keeps.append(superpos)
        if change and len(keeps) > 0:
            self.tiles[coords3D].reset_superpositions(newSuperpositions=keeps)
            for n in self.neighbours_of_coords(coords3D, dimensions=2):
                self.refresh_tile(n)









    def find_lowest_superposition(self):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = []
        k = list(self.tiles.keys())
        for co in range(len(k)):
            if not self.tiles[k[co]].isCollapse() and self.tiles[k[co]].nb_superpositions() < min:

                min = self.tiles[k[co]].nb_superpositions()
                coordsofmin = [k[co]]
            elif not self.tiles[k[co]].isCollapse() and self.tiles[k[co]].nb_superpositions() == min:
                coordsofmin.append(k[co])
        if len(coordsofmin) == 0:
            return None
        return coordsofmin[random.randint(0, len(coordsofmin)-1)]



    def toJson(self):
        list = []
        t = None
        for coords in self.tiles.keys():
            #self.tiles[coords].force_collapse() # DONT KEEP THIS LINE  -----------------------  SHIT HERE
            if not(coords[0] < 0 or coords[2] >= MAX_XZ_STAD):
                t = self.tiles[coords].toObj()
                if not t['BlockModelName'] == "":
                    t['Coord'] = coords
                    list.append(t)


        return json.dumps({"JsonBlocks": list})


    def solve(self):
        co = list(self.tiles.keys())[random.randint(0, len(self.tiles.keys())-1)]


        while co is not None:
            self.collapse(co)
            co = self.find_lowest_superposition()






class Tile:
    superpositions = None
    collapse = None


    def __init__(self, blocks):
        self.superpositions = list(blocks)




    def get_superpositions(self):
        return self.superpositions

    def nb_superpositions(self):
        return len(self.superpositions)

    def reset_superpositions(self, newSuperpositions=None):
        s = self.superpositions
        if newSuperpositions is None:
            self.superpositions = []
        else:
            self.superpositions = newSuperpositions
        return s




    def isCollapse(self):
        return self.collapse is not None


    def force_collapse(self, superposition=None):
        if len(self.superpositions) == 0:
            self.collapse = self.superpositions[0]
            return

        if not self.isCollapse() and superposition is None:
            self.collapse = self.superpositions[random.randint(0,len(self.superpositions)-1)]
            self.superpositions = [self.collapse]
            return

        if superposition in self.superpositions:
            self.collapse = superposition
            self.superpositions = [superposition]
            return

        print("force_collapse(" + superposition + ") in Tile in Stadium:")
        print("Wrong argument")

    def toObj(self):
        return {
            'BlockModelName': self.collapse.split('_')[0],
            'Dir': self.collapse.split('_')[1],
            'Coord': None, 'Color': 0, 'Mode': 'Normal'
        }



blockSetList = []

app = Flask(__name__)

@app.route("/reloadBlockSetList", methods=['GET'])
def loadBlockSetList():
    with open("blockSetList.json", 'r') as f:
        setList = json.load(f)
    global blockSetList
    blockSetList = sorted(setList, key=lambda x: x['name'])

    for b in range(len(blockSetList)):
        blockSetList[b] = BlockSet(blockSetList[b])

    return "List has been updated !"



def binary_search_BlockSet(x):
    low = 0
    high = len(blockSetList) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        if blockSetList[mid].get_name() < x:
            low = mid + 1

        elif blockSetList[mid].get_name() > x:
            high = mid - 1

        else:
            return blockSetList[mid]

    # If we reach here, then the element was not present
    return None



@app.route("/get-blocks/<nameofset>", methods=["GET"])
def getBlocks(nameofset):
    set = binary_search_BlockSet(nameofset)
    if set is None:
       return "No set found."

    stadium = Stadium(set)

    stadium.solve()
    return stadium.toJson()




if __name__ == '__main__':
    loadBlockSetList()
    app.run(host='127.0.0.1', port=8080,debug=True)