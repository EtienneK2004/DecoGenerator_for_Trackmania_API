def rotate_block(Blockname, dir):

    return Blockname.split('_')[0] + '_' + add_dir(Blockname.split('_')[1], dir)

def add_dir(baseDir, relativeDir):
    dirs = ['0', '1', '2', '3']
    return dirs[(dirs.index(baseDir) + dirs.index(relativeDir))%4]

def opposite_dir(dir):
    dirs = ['0', '1', 'Top', '2', '3', 'Bottom']
    return dirs[(dirs.index(dir)+3)%6]

def sub_dir(first, second):
    dirs = ['0', '1', '2', '3']
    return dirs[(dirs.index(first) - dirs.index(second))%4]

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
