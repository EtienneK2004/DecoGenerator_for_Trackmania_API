from flask import Flask
import json
import random

Y_AXIS_FOR_2D = 9


def relative_to_absolute(baseDir, relativeDir):
    dirs = ['North', 'East', 'South', 'West']
    return dirs[(dirs.index(baseDir) + dirs.index(relativeDir))%4]


def rotate_block(Blockname, dir):

    return Blockname.split('_')[0] + '_' + relative_to_absolute(Blockname.split('_')[1], dir)





class Block:
    name = ""
    possibleBlocks = {}
    def __init__(self, bDict, rotation):
        dirs = ['North', 'East', 'South', 'West']
        self.name = bDict['name'] + "_" + rotation
        self.possibleBlocks[relative_to_absolute("North", rotation)] = bDict['north']
        self.possibleBlocks[relative_to_absolute("East", rotation)] = bDict['east']
        self.possibleBlocks[relative_to_absolute("South", rotation)] = bDict['south']
        self.possibleBlocks[relative_to_absolute("West", rotation)] = bDict['west']

        for d in dirs:
            for i in range(len(self.possibleBlocks[d])):
                self.possibleBlocks[d][i] = rotate_block(self.possibleBlocks[d][i], rotation)





class BlockSet:
    listBlocks = {}
    name = ""
    dimensions = 0
    def __init__(self, BlockSetJson):
        self.name = BlockSetJson['name']
        self.dimensions = BlockSetJson['dimensions']
        for b in BlockSetJson['blocks']:
            dirs = ['North', 'East', 'South', 'West']
            for d in dirs:
                self.listBlocks[b['name']+'_'+d] = Block(b, d)

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
        return list(map(lambda x : rotate_block(x, dir), self.listBlocks[blockname][relative_to_absolute(basedir, dir)]))




    def get_name(self):
        return self.name





class Stadium:
    tiles = {} # Key is a tuple of 3 int (coordinates)
    blockSet = None

    def __init__(self, BlockSet):
        self.blockSet = BlockSet
        if BlockSet.dimensions == 2:
            for x in range(42):
                for z in range(42):
                    self.add_tile((x, Y_AXIS_FOR_2D, z))

    def add_tile(self, coords3D):
        self.tiles[coords3D] = Tile(self.blockSet.get_all_blocknames())


    def is_coords_out_of_stadium(self, coords):
        return coords[0] > 41 or coords[1] > 31 or coords[2] > 41 or coords[0] < 0 or coords[1] < 9 or coords[2] < 0


    def get_superpositions(self, coords3D):
        return self.tiles[coords3D].get_superpositions()


    def collapse(self, coords3D, superposition=None):
        self.tiles[coords3D].force_collapse(superposition)


    def neighbours_of_coords(self, coords3D, dimensions=3):
        listn = []
        listn.append((coords3D[0]+1,coords3D[1], coords3D[2]))
        listn.append((coords3D[0]-1,coords3D[1], coords3D[2]))
        if dimensions > 1:
            listn.append((coords3D[0],coords3D[1], coords3D[2]+1))
            listn.append((coords3D[0],coords3D[1], coords3D[2]-1))
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
        if self.is_coords_out_of_stadium(coords):
            return True

        for b in self.tiles[coords].get_superpositions():
            print('comparaison', blockname, self.blockSet.possible_blocks_near(b, dir))
            if blockname in self.blockSet.possible_blocks_near(b, dir):
                return True

        return False


    def refresh_tile(self, coords3D):
        print('refresh', coords3D)
        # For each superposition, keep it if all neighbours have a superposition allowing it
        # If a change was made, refresh neighbours
        dirs = ['East', 'West', "South",'North']
        keeps = []
        change = False
        for superpos in self.tiles[coords3D].get_superpositions():
            keep = True
            idir = 0
            for n in self.neighbours_of_coords(coords3D, dimensions=2):
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dirs[idir], n):
                    keep = False
                    change = True
                    break


                idir = (idir+1)%4

            if keep:
                keeps.append(superpos)
        if change:
            print()
            print(keeps)
            self.tiles[coords3D].reset_superpositions(newSuperpositions=keeps)
            print(coords3D, self.tiles[coords3D].get_superpositions())
            for n in self.neighbours_of_coords(coords3D, dimensions=2):
                self.refresh_tile(n)





        # VERY IMPORTANT



    def find_lowest_superposition(self):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = None
        for coords in self.tiles.keys():
            if not self.tiles[coords].isCollapse() and self.tiles[coords].nb_superpositions() < min:
                min = self.tiles[coords].nb_superpositions()
                coordsofmin = coords

        return coords



    def toJson(self):
        list = []
        t = None
        for coords in self.tiles.keys():
            self.tiles[coords].force_collapse() # DONT KEEP THIS LINE  -----------------------  SHIT HERE
            t = self.tiles[coords].toObj()
            t['Coord'] = coords
            list.append(t)
        return json.dumps(list)


    def solve(self):
        co = list(self.tiles.keys())[random.randint(0, len(self.tiles.keys())-1)]


        while co is not None:
            print(co)
            self.collapse(co)
            for n in self.neighbours_of_coords(co, dimensions=2):
                self.refresh_tile(n)
            co = self.find_lowest_superposition()






class Tile:
    superpositions = []
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
        if self.isCollapse():
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
    #app.run(debug=True)