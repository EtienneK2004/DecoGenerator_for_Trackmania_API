import random
from models.Block import Block
from models.Socket import Socket

class BlockSet:
    listBlocks = None
    listSockets = None
    name = ""
    dimensions = 0
    def __init__(self, BlockSetJson):
        self.listBlocks = []
        self.listSockets = {}
        self.name = BlockSetJson['name']
        self.dimensions = BlockSetJson['dimensions']

        #Sockets
        for k in BlockSetJson['sockets'].keys():
            self.listSockets[k] = Socket(k)
        
        #Sockets Friends
        for s_id in self.listSockets:
            friends = BlockSetJson['sockets'][s_id]
            for f_id in friends:
                self.listSockets[s_id].addFriend(self.listSockets[f_id])

        rotations = [0, 1, 2, 3]
        weight = 0
        name = ""

        for b in BlockSetJson['blocks']:
            friends = []
            
            block = Block(b['name'], b['weight'], 0)
            for f_id in b['sockets']: #frist is north, second is east ...
                block.addSocket(self.listSockets[f_id])
            if self.dimensions > 2:
                block.setTopSocket(self.listSockets[b['top']])
                block.setBottomSocket(self.listSockets[b['bottom']])
            self.listBlocks.append(block)

            #get the 3 rotations
            next_block_rotation = block.getBlockNextRotation()
            self.listBlocks.append(next_block_rotation)
            next_block_rotation = next_block_rotation.getBlockNextRotation()
            self.listBlocks.append(next_block_rotation)
            next_block_rotation = next_block_rotation.getBlockNextRotation()
            self.listBlocks.append(next_block_rotation)

            #for d in rotations:
            #    self.listBlocks.append(Block(b, d, BlockSetJson))


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
        return self.listBlocks
        #return self.listBlocks.values()

    def get_all_blocknames(self):
        return [ block.name for block in self.get_all_blocks()]

    def possible_blocks_near(self, block, dir, basedir=None):
        if basedir is None:
            return block.possibleBlocks[dir]
            #return self.listBlocks[blockname].possibleBlocks[dir]


    def get_name(self):
        return self.name
