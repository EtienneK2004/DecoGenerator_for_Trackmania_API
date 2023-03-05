import random
import json
from models.Tile import Tile

# for all generation
MAX_XZ_STAD = 48 # size on x + z

# for 2D
Y_AXIS_FOR_2D = 1 # ground level for 2 dimension blockset only

# for 3D
Y_MAX = 9 # max height of the build
#TODO : add Y_MIN (always high or equal to 9, default tm2020 level)

# return the direction between to first coords and the second
def dir_from_coords(basecoords, x, y, z):
    if basecoords[0] < x:
        return "3"
    if basecoords[1] < y:
        return "Top"
    if basecoords[2] < z:
        return "0"
    if basecoords[0] > x:
        return "1"
    if basecoords[1] > y:
        return "Bottom"
    return "2"




class Stadium:
    tiles = None # 3d array. The tm covertion is at the render for Y Axis
    blockSet = None
    y_max = 1
    nb_superpositions = 0

    def __init__(self, BlockSet):
        self.tiles = []
        self.blockSet = BlockSet
        self.nb_superpositions = len(self.blockSet.get_all_blocks())

        if(self.blockSet.dimensions == 3):
            self.y_max = Y_MAX

        self.tiles = [[[Tile(self.blockSet.get_all_blocknames()) for y in range(self.y_max)] for z in range(MAX_XZ_STAD)] for x in range(MAX_XZ_STAD)]


    def is_coords_out_of_stadium(self, coords):
        return coords[0] > (MAX_XZ_STAD-1) or coords[1] >= Y_MAX or coords[2] > (MAX_XZ_STAD-1) or coords[0] < 0 or coords[1] < 0 or coords[2] < 0


    def get_superpositions(self, x, y, z):
        return self.tiles[x][z][y].get_superpositions()


    def collapse(self, x, y, z, superposition=None):
        if(self.tiles[x][z][y].collapse is not None):
            return
        if superposition is None:
            superposition = self.blockSet.get_random_block(self.tiles[x][z][y].get_superpositions())

        self.tiles[x][z][y].force_collapse(superposition)
        a = self.neighbours_of_coords(x, y, z)

        for n in a:
            self.refresh_tile(n)
        #try:
        #    self.collapse(self.find_lowest_superposition_of_list(a))
        #except:
        #    pass


    def neighbours_of_coords(self, x, y, z):
        dimensions = self.blockSet.dimensions
        listn = []
        if dimensions > 1:
            listn.append((x,   y, z+1))
            listn.append((x-1, y, z  ))
            listn.append((x,   y, z-1))
            listn.append((x+1, y, z  ))


        if dimensions > 2:
            listn.append((x, y+1, z))
            listn.append((x, y-1, z))

        rmv = []

        for i in listn:
            if self.is_coords_out_of_stadium(i):
                rmv.append(i)

        for i in rmv:
            listn.remove(i)

        return listn


    def can_Block_be_at_Direction_of_Tile(self, blockname, dir, coords):
        x,y,z = coords[0],coords[1],coords[2]
        for b in self.tiles[x][z][y].get_superpositions():

            if blockname in self.blockSet.possible_blocks_near(b, dir):
                return True

        return False


    def refresh_tile(self, coords3D):
        x,y,z = coords3D[0],coords3D[1],coords3D[2]
        # For each superposition, keep it if all neighbours have a superposition allowing it
        # If a change was made, refresh neighbours
        keeps = []
        change = False
        for superpos in self.tiles[x][z][y].get_superpositions():
            keep = True
            idir = 2
            for n in self.neighbours_of_coords(x,y,z):
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dir_from_coords(n, x,y,z), n): # can place superposition by dir
                    keep = False
                    change = True
                    break

            if keep:
                keeps.append(superpos)
        if change and len(keeps) > 0:
            self.tiles[x][z][y].reset_superpositions(newSuperpositions=keeps)
            for n in self.neighbours_of_coords(x,y,z):
                self.refresh_tile(n)


    def find_lowest_superposition(self):
        min = self.nb_superpositions
        coordsofmin = [] #contain a list of tuple that represent the coord of all tiles with the lowest superposition possibility

        for x in range(MAX_XZ_STAD):
            for z in range(MAX_XZ_STAD):
                for y in range(self.y_max):
                    if not self.tiles[x][z][y].isCollapse() and self.tiles[x][z][y].nb_superpositions() < min:
                        min = self.tiles[x][z][y].nb_superpositions()
                        coordsofmin = [(x,y,z)]
                    elif not self.tiles[x][z][y].isCollapse() and self.tiles[x][z][y].nb_superpositions() == min:
                        coordsofmin.append((x,y,z))

        if len(coordsofmin) == 0:
            return None
        return coordsofmin[random.randint(0, len(coordsofmin)-1)]

    def solve(self):
        #take a random key of the grid
        co_x = random.randint(0, MAX_XZ_STAD - 1)
        co_y = 0
        if self.blockSet.dimensions == 3:
            co_y = random.randint(0, Y_MAX - 1)
        co_z = random.randint(0, MAX_XZ_STAD - 1)
        coord = (co_x, co_y, co_z)

        while coord is not None:
            co_x, co_y, co_z = coord[0], coord[1], coord[2] # TODO : change that
            self.collapse(co_x, co_y, co_z)
            coord = self.find_lowest_superposition()

    def toJson(self):
        list = []
        t = None
        y_2d_build = Y_AXIS_FOR_2D + 9

        for x in range(MAX_XZ_STAD):
            for z in range(MAX_XZ_STAD):
                for y in range(self.y_max):
                    if not(x < 0 or z >= MAX_XZ_STAD):
                        t = self.tiles[x][z][y].toObj()
                        if not t['b'] == "":
                            if self.blockSet.dimensions == 3:
                                t['v'] = (x, y*2, z)
                            else:
                                t['v'] = (x, y_2d_build, z)
                            list.append(t)

        return json.dumps(list)

