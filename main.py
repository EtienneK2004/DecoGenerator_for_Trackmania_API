from flask import Flask
import json
import random

Y_AXIS_FOR_2D = 9


class Block:
    name = ""
    # This lists contain the blocks' names
    relativeNorth = []
    relativeEast = []
    relativeSouth = []
    relativeWest = []
    def __init__(self, bDict):
        self.name = bDict['name']
        self.relativeNorth = bDict['north']
        self.relativeEast = bDict['east']
        self.relativeSouth = bDict['south']
        self.relativeWest = bDict['west']




class BlockSet:
    listBlocks = []
    name = ""
    dimensions = 0
    def __init__(self, BlockSetJson):
        self.name = BlockSetJson['name']
        self.dimensions = BlockSetJson['dimensions']
        for b in BlockSetJson['blocks']:
            self.listBlocks.append(Block(b))

    def get_all_blocks(self):
        return self.listBlocks

    def get_all_blocks_all_dir(self):
        allblocks = self.get_all_blocks()
        allblocksalldir = []
        for block in allblocks:
            allblocksalldir.append(block.name + "_North")
            allblocksalldir.append(block.name + "_East")
            allblocksalldir.append(block.name + "_South")
            allblocksalldir.append(block.name + "_West")
        return allblocksalldir


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
                    self.add_tile((x, Y_AXIS_FOR_2D, z), BlockSet)

    def add_tile(self, coords3D, BlockSet):
        self.tiles[coords3D] = Tile(BlockSet.get_all_blocks_all_dir())


    def get_superpositions(self, coords3D):
        return self.tiles[coords3D].get_superpositions()


    def collapse(self, coords3D, superposition=None):
        self.tiles[coords3D].force_collapse(superposition)


    def refresh_neighbours(self, coords3D):
        pass
        # VERY IMPORTANT



    def find_lowest_superposition(self):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = None
        for coords in self.tiles.keys():
            if self.tiles[coords].nb_superpositions() < min:
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




class Tile:
    superpositions = []
    collapse = None


    def __init__(self, blocks):
        self.superpositions = blocks


    def get_superpositions(self):
        return self.superpositions

    def nb_superpositions(self):
        return len(self.superpositions)


    def isCollapse(self):
        return len(self.superpositions) == 1


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

    return stadium.toJson()




if __name__ == '__main__':
    loadBlockSetList()
    app.run(debug=True)