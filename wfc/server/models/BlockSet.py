import random
from models.Block import Block

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
