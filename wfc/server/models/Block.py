class Block:
    name = ""
    weight = 0
    rotation = 0
    sockets = None #contains sockets id ordored by north east south west top bottom

    def __init__(self, name, weight, rotation):
        self.name = name
        self.weight = weight
        self.rotation = rotation
        self.sockets = []


    def addSocket(self, socket):
        self.sockets.append(socket)
        if(len(self.sockets) > 6):
            raise("ERROR, to many sockets for a block")
    
    #change from [north, east, south, west] to [north, south, east, west]
    def reorderSockets(self):
        tmp = self.sockets[1]
        self.sockets[1] = self.sockets[2]
        self.sockets[2] = tmp

    def getBlockNextRotation(self, dimension):
        r = self.rotation + 1 if self.rotation < 3 else 0
        new_block = Block(self.name, self.weight, r)
        #rotation the sockets
        new_block.addSocket(self.sockets[3])
        new_block.addSocket(self.sockets[2])
        new_block.addSocket(self.sockets[0])
        new_block.addSocket(self.sockets[1])
        if(dimension > 2):
            new_block.addSocket(self.sockets[4])
            new_block.addSocket(self.sockets[5])

        return new_block

    def __eq__(self, other):
        return self.name == other.name and self.rotation == other.rotation
