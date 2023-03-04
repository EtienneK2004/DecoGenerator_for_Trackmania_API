import json
import random
from time import sleep
import sys





Y_AXIS_FOR_2D = 9
Y_MAX = 9
MAX_XZ_STAD = 10

sys.setrecursionlimit(2000)




def add_dir(baseDir, relativeDir):
    dirs = ['0', '1', '2', '3']
    return dirs[(dirs.index(baseDir) + dirs.index(relativeDir))%4]

def opposite_dir(dir):
    dirs = ['0', '1', 'Top', '2', '3', 'Bottom']
    return dirs[(dirs.index(dir)+3)%6]

def rotate_block(Blockname, dir):

    return Blockname.split('_')[0] + '_' + add_dir(Blockname.split('_')[1], dir)

def sub_dir(first, second):
    dirs = ['0', '1', '2', '3']
    return dirs[(dirs.index(first) - dirs.index(second))%4]

def dir_from_coords(basecoords, coords):
    if basecoords[0] < coords[0]:
        return "3"
    if basecoords[1] < coords[1]:
        return "Top"
    if basecoords[2] < coords[2]:
        return "0"
    if basecoords[0] > coords[0]:
        return "1"
    if basecoords[1] > coords[1]:
        return "Bottom"
    return "2"





class Block:
    name = ""
    weight = 0
    possibleBlocks = None
    def __init__(self, blDict, rotation, blockset):
        bDict = dict(blDict)
        self.possibleBlocks = {}
        dirs = ['0', '1', '2', '3']
        self.name = bDict['name'] + "_" + rotation
        self.weight = bDict['weight']
        self.possibleBlocks[add_dir("0", rotation)] = self.possible_blocks_side(bDict['0'], '0', blockset)
        self.possibleBlocks[add_dir("1", rotation)] = self.possible_blocks_side(bDict['1'], '1', blockset)
        self.possibleBlocks[add_dir("2", rotation)] = self.possible_blocks_side(bDict['2'], '2', blockset)
        self.possibleBlocks[add_dir("3", rotation)] = self.possible_blocks_side(bDict['3'], '3', blockset)

        if blockset["dimensions"] == 3:
            self.possibleBlocks["Top"] = self.possible_blocks_side(bDict['top'], 'Top', blockset)
            self.possibleBlocks["Bottom"] = self.possible_blocks_side(bDict['bottom'], 'Bottom', blockset)


        for d in dirs:
            for i in range(len(self.possibleBlocks[d])):
                self.possibleBlocks[d][i] = rotate_block(self.possibleBlocks[d][i], rotation)


    def possible_blocks_side(self, sidename, dir, blockSetJson):
        blocks = []
        if dir == "Top":
            for block in blockSetJson['blocks']:
                if block['bottom'] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name'] + "_" + self.name.split("_")[1])
            return blocks

        if dir == "Bottom":
            for block in blockSetJson['blocks']:
                if block['top'] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name'] + "_" + self.name.split("_")[1])
            return blocks

        for block in blockSetJson['blocks']:
            for rotation in ['0', '1', '2', '3']:
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
            dirs = ['0', '1', '2', '3']
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

        if BlockSet.dimensions == 3:
            for x in range(MAX_XZ_STAD):
                for y in range(9, 9+Y_MAX):
                    for z in range(MAX_XZ_STAD):
                        self.add_tile((x, y, z))

    def add_tile(self, coords3D):
        self.tiles[coords3D] = Tile(self.blockSet.get_all_blocknames())


    def is_coords_out_of_stadium(self, coords):
        return coords[0] > (MAX_XZ_STAD-1) or coords[1] >= Y_MAX+9 or coords[2] > (MAX_XZ_STAD-1) or coords[0] < 0 or coords[1] < 9 or coords[2] < 0


    def get_superpositions(self, coords3D):
        return self.tiles[coords3D].get_superpositions()


    def collapse(self, coords3D, superposition=None):
        if(self.tiles[coords3D].collapse is not None):
            return
        if superposition is None:
            superposition = self.blockSet.get_random_block(self.tiles[coords3D].get_superpositions())

        self.tiles[coords3D].force_collapse(superposition)
        a = self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions)

        for n in a:
            self.refresh_tile(n)
        #try:
        #    self.collapse(self.find_lowest_superposition_of_list(a))
        #except:
        #    pass


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
            for n in self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions):
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dir_from_coords(n, coords3D), n):

                    keep = False
                    change = True
                    break



            if keep:
                keeps.append(superpos)
        if change and len(keeps) > 0:
            self.tiles[coords3D].reset_superpositions(newSuperpositions=keeps)
            for n in self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions):
                self.refresh_tile(n)









    def find_lowest_superposition(self):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = []
        k = list(self.tiles.keys())
        return self.find_lowest_superposition_of_list(k)

    def find_lowest_superposition_of_list(self, coordsList):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = []
        k = coordsList
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
                if not t['b'] == "":
                    if self.blockSet.dimensions == 3:
                        t['v'] = (coords[0], coords[1]*2-9, coords[2])
                    else:
                        t['v'] = coords
                    list.append(t)

        return json.dumps(list)
        #return json.dumps({"JsonBlocks": list})


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
            'b': self.collapse.split('_')[0].split('.')[0],
            'd': self.collapse.split('_')[1],
            'v': None, 'c': 0, 'm': 'Normal'
        }



blockSetList = []


def loadBlockSetList():
    with open("/usr/files/blocksets/blockSetList3D.json", 'r') as f:
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



def run(nameofset):
    loadBlockSetList()
    set = binary_search_BlockSet(nameofset)
    if set is None:
       return "No set found."

    stadium = Stadium(set)

    stadium.solve()
    return stadium.toJson()

