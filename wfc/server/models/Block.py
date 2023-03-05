def rotate_block(Blockname, dir):
    return Blockname.split('_')[0] + '_' + str(add_dir(int(Blockname.split('_')[1]), dir))

def add_dir(baseDir, relativeDir):
    dirs = [0, 1, 2, 3]
    return dirs[(dirs.index(baseDir) + dirs.index(relativeDir))%4]

def opposite_dir(dir):
    dirs = ['0', '1', 'Top', '2', '3', 'Bottom']
    return dirs[(dirs.index(dir)+3)%6]

def sub_dir(first, second):
    dirs = ['0', '1', '2', '3']
    return dirs[(dirs.index(first) - dirs.index(second))%4]

STR_DIR_LIST = ['0', '1', '2', '3']
INT_DIR_LIST = [0, 1, 2, 3]

class Block:
    name = ""
    weight = 0
    rotation = 0
    sockets = None #contains sockets id or Socket
    top = None
    bottom = None
    possibleBlocks = None

    def __init__(self, name, weight, rotation):
        self.name = name
        self.weight = weight
        self.rotation = rotation
        self.sockets = []

    """
    def __init__(self, blDict, rotation, blockset):
        bDict = dict(blDict)
        self.possibleBlocks = {}
        self.rotation = rotation
        self.name = bDict['name']
        self.weight = bDict['weight']
        #self.name = bDict['name'] + "_" + rotation
        
        self.possibleBlocks[add_dir(0, rotation)] = self.possible_blocks_side(bDict['0'], '0', blockset)
        self.possibleBlocks[add_dir(1, rotation)] = self.possible_blocks_side(bDict['1'], '1', blockset)
        self.possibleBlocks[add_dir(2, rotation)] = self.possible_blocks_side(bDict['2'], '2', blockset)
        self.possibleBlocks[add_dir(3, rotation)] = self.possible_blocks_side(bDict['3'], '3', blockset)

        if blockset["dimensions"] == 3:
            self.possibleBlocks["Top"] = self.possible_blocks_side(bDict['top'], 'Top', blockset)
            self.possibleBlocks["Bottom"] = self.possible_blocks_side(bDict['bottom'], 'Bottom', blockset)

        for d in INT_DIR_LIST:
            for i in range(len(self.possibleBlocks[d])):
                self.possibleBlocks[d][i] = rotate_block(self.possibleBlocks[d][i], rotation)
    """

    def addSocket(self, socket):
        self.sockets.append(socket)
        if(len(self.sockets) > 4):
            raise("ERROR, to many sockets for a block")

    def setTopSocket(self, socket):
        self.top = socket
    
    def setBottomSocket(self, socket):
        self.bottom = socket

    def getBlockNextRotation(self):
        r = self.rotation + 1 if self.rotation < 3 else 0
        new_block = Block(self.name, self.weight, r)
        #rotation the sockets
        new_block.addSocket(self.sockets[3])
        new_block.addSocket(self.sockets[0])
        new_block.addSocket(self.sockets[1])
        new_block.addSocket(self.sockets[2])
        new_block.setTopSocket(self.top)
        new_block.setBottomSocket(self.bottom)

        return new_block


    def possible_blocks_side(self, sidename, dir, blockSetJson):
        blocks = []
        if dir == "Top":
            for block in blockSetJson['blocks']:
                if block['bottom'] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name'] + "_" + str(self.rotation))
            return blocks

        if dir == "Bottom":
            for block in blockSetJson['blocks']:
                if block['top'] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name'] + "_" + str(self.rotation))
            return blocks

        for block in blockSetJson['blocks']:
            for rotation in STR_DIR_LIST:
                if block[sub_dir(dir, rotation).lower()] in blockSetJson['sockets'][sidename]:
                    blocks.append(block['name']+"_"+opposite_dir(rotation))
        return blocks

    def __eq__(self, other):
        return self.name == other.name and self.rotation == other.rotation
