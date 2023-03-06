import random
import json

# for all generation
MAX_XZ_STAD = 48 # size on x + z
Y_AXIS_GROUND_LVL = 20 # ground level for 2 dimension blockset only

# for 3D
Y_MAX = 9 # max height of the build
#TODO : add Y_MIN (always high or equal to 9, default tm2020 level)

# return the direction between to first coords and the second
def dir_from_coords(basecoords, x, y, z):
    if basecoords[0] < x:
        return 3
    if basecoords[1] < y:
        return 4 #"Top"
    if basecoords[2] < z:
        return 0
    if basecoords[0] > x:
        return 1
    if basecoords[1] > y:
        return 5 #"Bottom"
    return 2

def opposite_dir(dir):
    dirs = [0, 1, 4, 2, 3, 5]
    return dirs[(dirs.index(dir)+3)%6]


class Stadium:
    tiles = None # 3d array. The tm covertion is at the render for Y Axis
    tiles_poss = None
    blockSet = None
    all_blocks = None
    y_max = 1
    nb_superpositions = 0

    def __init__(self, BlockSet):
        self.tiles = []
        self.tiles_poss = []
        self.blockSet = BlockSet
        self.nb_superpositions = len(self.blockSet.get_all_blocks())
        self.all_blocks = self.blockSet.get_all_blocks()

        if(self.blockSet.dimensions == 3):
            self.y_max = Y_MAX

        self.tiles = [[[[True for i in range(self.nb_superpositions)] for y in range(self.y_max)] for z in range(MAX_XZ_STAD)] for x in range(MAX_XZ_STAD)]
        self.tiles_poss = [[[self.nb_superpositions for y in range(self.y_max)] for z in range(MAX_XZ_STAD)] for x in range(MAX_XZ_STAD)]

    def is_coords_out_of_stadium(self, coords):
        return coords[0] > (MAX_XZ_STAD-1) or coords[1] >= self.y_max or coords[2] > (MAX_XZ_STAD-1) or coords[0] < 0 or coords[1] < 0 or coords[2] < 0

    def neighbours_of_coords(self, x, y, z):
        dimensions = self.blockSet.dimensions
        listn = []
        if dimensions > 1:
            i = (x,   y, z+1)
            if not self.is_coords_out_of_stadium(i) : listn.append(i)
            i = (x-1, y, z  )
            if not self.is_coords_out_of_stadium(i) : listn.append(i)
            i = (x,   y, z-1)
            if not self.is_coords_out_of_stadium(i) : listn.append(i)
            i = (x+1, y, z  )
            if not self.is_coords_out_of_stadium(i) : listn.append(i)

        if dimensions > 2:
            i = (x, y+1, z)
            if not self.is_coords_out_of_stadium(i) : listn.append(i)
            i = (x, y-1, z)
            if not self.is_coords_out_of_stadium(i) : listn.append(i)

        return listn

    def can_Block_be_at_Direction_of_Tile(self, index, dir, coords):
        x,y,z = coords[0],coords[1],coords[2]
        #print("can_Block_be_at_Direction_of_Tile")
        #print(coords)
        #print(self.all_blocks[index].name)

        #les possibilites du voisin du voisin
        poss = [b for b, c in enumerate(self.tiles[x][z][y]) if c ]

        #TODO check for top and bottom matching

        # if one of the superposition of the coord tiles has a matching socket with the block given, we return true
        for b in poss:
            """print("poss? :" + self.all_blocks[b].name + " dir : " + str(dir))
            print(self.all_blocks[b].sockets[dir]) #OUI
            print(self.all_blocks[index].sockets[opposite_dir(dir)].friends)
            print("OR")
            print(self.all_blocks[b].sockets)
            print(self.all_blocks[index].sockets[dir])"""

            if(dir == 4):
                if(self.all_blocks[b].top in self.all_blocks[index].bottom.friends):
                    return True
            elif(dir == 5):
                if(self.all_blocks[b].bottom in self.all_blocks[index].top.friends):
                    return True
            elif(self.all_blocks[b].sockets[dir] in self.all_blocks[index].sockets[opposite_dir(dir)].friends):
                return True
            #elif(self.all_blocks[index].sockets[opposite_dir(dir)] in self.all_blocks[b].sockets[dir].friends):
            #    return True
            #if self.all_blocks[index].name + "_" + str(self.all_blocks[index].rotation) in self.blockSet.possible_blocks_near(self.all_blocks[b], dir): #TODO :check values and dont use string
            #    return True

        return False

    def refresh_tile(self, coords3D):
        x,y,z = coords3D[0],coords3D[1],coords3D[2]
        # For each superposition, keep it if all neighbours have a superposition allowing it
        # If a change was made, refresh neighbours
        keeps = []
        disables = []
        change = False
        superpos_index = [ superpos for superpos, c in enumerate(self.tiles[x][z][y]) if c ]
        for superpos in superpos_index: #superpos is only indexes of True superpositions
            keep = True
            idir = 2
            for n in self.neighbours_of_coords(x,y,z):
                #print("frist voisin")
                #print(n)
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dir_from_coords(n, x,y,z), n): # can place superposition by dir #TODO check le truc #block index can be given to the function
                    keep = False
                    change = True
                    break
                #raise("stop")

            if not keep:
                disables.append(superpos)

        # remove all not possible superposition
        if change and disables : #TODO check if change can be removed
            for disable in disables:
                self.tiles[x][z][y][disable] = False
                self.tiles_poss[x][z][y] -= 1
            for n in self.neighbours_of_coords(x,y,z):
                self.refresh_tile(n)

    def find_lowest_superposition(self):
        min = self.nb_superpositions
        coordsofmin = [] #contain a list of tuple that represent the coord of all tiles with the lowest superposition possibility

        for x in range(MAX_XZ_STAD):
            for z in range(MAX_XZ_STAD):
                for y in range(self.y_max):
                    if self.tiles_poss[x][z][y] > 1 :
                        if self.tiles_poss[x][z][y] < min: 
                            min = self.tiles_poss[x][z][y]
                            coordsofmin = [(x,y,z)]
                        elif self.tiles_poss[x][z][y] == min:
                            coordsofmin.append((x,y,z))

        if not coordsofmin:
            return None
        return coordsofmin[random.randint(0, len(coordsofmin)-1)]

    def collapse(self, x, y, z):
        # exit if tile is collapsed
        if(self.tiles_poss[x][z][y] <= 1):
            return
        
        # force collapse on the given coord 
        superposition = random.randint(0, self.nb_superpositions - 1)
        while not self.tiles[x][z][y][superposition]:
            superposition = random.randint(0, self.nb_superpositions - 1)

        self.tiles[x][z][y] = [False for i in range (self.nb_superpositions)]
        self.tiles[x][z][y][superposition] = True
        self.tiles_poss[x][z][y] = 1

        for n in self.neighbours_of_coords(x, y, z):
            #print("refresh n")
            #print(n)
            self.refresh_tile(n)

    def solve(self):
        #take a random key of the grid
        co_x = random.randint(0, MAX_XZ_STAD - 1)
        co_y = random.randint(0, Y_MAX - 1) if self.blockSet.dimensions == 3 else 0
        co_z = random.randint(0, MAX_XZ_STAD - 1)

        coord = (co_x, co_y, co_z)
        #coord = (0,0,0)

        while coord is not None:
            co_x, co_y, co_z = coord[0], coord[1], coord[2] # TODO : change that
            self.collapse(co_x, co_y, co_z)
            coord = self.find_lowest_superposition()

    def toObj(self,block):
        return {
            'b': block.name,
            'd': block.rotation,
            'v': None, 'c': 0, 'm': 'Normal'
        }

    def toJson(self):
        list = []
        t = None
        y_2d_build = Y_AXIS_GROUND_LVL + 9
        all_blockset_blocks = self.blockSet.get_all_blocks()

        for x in range(MAX_XZ_STAD):
            for z in range(MAX_XZ_STAD):
                for y in range(self.y_max):
                    if not(x < 0 or z >= MAX_XZ_STAD):
                        t = self.toObj(all_blockset_blocks[[i for i, c in enumerate(self.tiles[x][z][y]) if c][0]])
                        if not t['b'] == "":
                            if self.blockSet.dimensions == 3:
                                t['v'] = (x, y*2 + Y_AXIS_GROUND_LVL, z)
                            else:
                                t['v'] = (x, y_2d_build, z)
                            list.append(t)

        return json.dumps(list)

