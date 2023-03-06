import random
from models.Block import Block

class BlockSet:
    listBlocks = None
    listSockets = None #dict of socket_id pointing friends socket_id { 0 : [1,2]}
    name = ""
    dimensions = 0
    def __init__(self, BlockSetJson):
        self.listBlocks = []
        listSocketNames = {} #dict of socket_name pointing socket_id { "socketname" : 0}
        self.listSockets = {}
        self.name = BlockSetJson['name']
        self.dimensions = BlockSetJson['dimensions']

        #Sockets
        i = 0
        for k in BlockSetJson['sockets'].keys():
            listSocketNames[k] = i
            i += 1
        
        #Sockets Friends
        for s_name, s_id in listSocketNames.items():
            friends = BlockSetJson['sockets'][s_name]
            self.listSockets[s_id] = []
            for f_name in friends:
                self.listSockets[s_id].append(listSocketNames[f_name])

        for b in BlockSetJson['blocks']:
            friends = []
            
            block = Block(b['name'], b['weight'], 0)
            for f_name in b['sockets']: #frist is north, second is east ...
                block.addSocket(listSocketNames[f_name])
            block.reorderSockets()
            if self.dimensions > 2:
                block.addSocket(listSocketNames[b['top']])
                block.addSocket(listSocketNames[b['bottom']])
            self.listBlocks.append(block)

            #get the 3 rotations
            next_block_rotation = block.getBlockNextRotation(self.dimensions)
            self.listBlocks.append(next_block_rotation)
            next_block_rotation = next_block_rotation.getBlockNextRotation(self.dimensions)
            self.listBlocks.append(next_block_rotation)
            next_block_rotation = next_block_rotation.getBlockNextRotation(self.dimensions)
            self.listBlocks.append(next_block_rotation)

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

    def get_name(self):
        return self.name
