import random
import json
from models.Tile import Tile

Y_AXIS_FOR_2D = 20
Y_MAX = 9
MAX_XZ_STAD = 10

def dir_from_coords(basecoords, coords):
    if basecoords[0] < coords[0]:
        return "3"
    if basecoords[1] < coords[1]:
        return "Top"
    if basecoords[2] < coords[2]:
        return "0"
    if basecoords[0] > coords[0]:
        return "1"
    if basecoords[1] > coords[1]:
        return "Bottom"
    return "2"




class Stadium:
    tiles = None # Key is a tuple of 3 int (coordinates)
    blockSet = None

    def __init__(self, BlockSet):
        self.tiles = {}
        self.blockSet = BlockSet
        if BlockSet.dimensions == 2:
            for x in range(MAX_XZ_STAD):
                for z in range(MAX_XZ_STAD):
                    self.add_tile((x, Y_AXIS_FOR_2D, z))

        if BlockSet.dimensions == 3:
            for x in range(MAX_XZ_STAD):
                for y in range(9, 9+Y_MAX):
                    for z in range(MAX_XZ_STAD):
                        self.add_tile((x, y, z))

    def add_tile(self, coords3D):
        self.tiles[coords3D] = Tile(self.blockSet.get_all_blocknames())


    def is_coords_out_of_stadium(self, coords):
        return coords[0] > (MAX_XZ_STAD-1) or coords[1] >= Y_MAX+9 or coords[2] > (MAX_XZ_STAD-1) or coords[0] < 0 or coords[1] < 9 or coords[2] < 0


    def get_superpositions(self, coords3D):
        return self.tiles[coords3D].get_superpositions()


    def collapse(self, coords3D, superposition=None):
        if(self.tiles[coords3D].collapse is not None):
            return
        if superposition is None:
            superposition = self.blockSet.get_random_block(self.tiles[coords3D].get_superpositions())

        self.tiles[coords3D].force_collapse(superposition)
        a = self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions)

        for n in a:
            self.refresh_tile(n)
        #try:
        #    self.collapse(self.find_lowest_superposition_of_list(a))
        #except:
        #    pass


    def neighbours_of_coords(self, coords3D, dimensions=3):
        listn = []
        if dimensions > 1:
            listn.append((coords3D[0],coords3D[1], coords3D[2]+1))
            listn.append((coords3D[0]-1,coords3D[1], coords3D[2]))
            listn.append((coords3D[0],coords3D[1], coords3D[2]-1))
            listn.append((coords3D[0]+1,coords3D[1], coords3D[2]))


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

        for b in self.tiles[coords].get_superpositions():

            if blockname in self.blockSet.possible_blocks_near(b, dir):
                return True

        return False


    def refresh_tile(self, coords3D):

        # For each superposition, keep it if all neighbours have a superposition allowing it
        # If a change was made, refresh neighbours
        keeps = []
        change = False
        for superpos in self.tiles[coords3D].get_superpositions():
            keep = True
            idir = 2
            for n in self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions):
                if not self.can_Block_be_at_Direction_of_Tile(superpos, dir_from_coords(n, coords3D), n):

                    keep = False
                    change = True
                    break



            if keep:
                keeps.append(superpos)
        if change and len(keeps) > 0:
            self.tiles[coords3D].reset_superpositions(newSuperpositions=keeps)
            for n in self.neighbours_of_coords(coords3D, dimensions=self.blockSet.dimensions):
                self.refresh_tile(n)









    def find_lowest_superposition(self):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = []
        k = list(self.tiles.keys())
        return self.find_lowest_superposition_of_list(k)

    def find_lowest_superposition_of_list(self, coordsList):
        min = len(self.blockSet.get_all_blocks())
        coordsofmin = []
        k = coordsList
        for co in range(len(k)):
            if not self.tiles[k[co]].isCollapse() and self.tiles[k[co]].nb_superpositions() < min:

                min = self.tiles[k[co]].nb_superpositions()
                coordsofmin = [k[co]]
            elif not self.tiles[k[co]].isCollapse() and self.tiles[k[co]].nb_superpositions() == min:
                coordsofmin.append(k[co])
        if len(coordsofmin) == 0:
            return None
        return coordsofmin[random.randint(0, len(coordsofmin)-1)]



    def toJson(self):
        list = []
        t = None
        for coords in self.tiles.keys():
            #self.tiles[coords].force_collapse() # DONT KEEP THIS LINE  -----------------------  SHIT HERE
            if not(coords[0] < 0 or coords[2] >= MAX_XZ_STAD):
                t = self.tiles[coords].toObj()
                if not t['b'] == "":
                    if self.blockSet.dimensions == 3:
                        t['v'] = (coords[0], coords[1]*2-9, coords[2])
                    else:
                        t['v'] = coords
                    list.append(t)

        return json.dumps(list)
        #return json.dumps({"JsonBlocks": list})


    def solve(self):
        co = list(self.tiles.keys())[random.randint(0, len(self.tiles.keys())-1)]


        while co is not None:
            self.collapse(co)
            co = self.find_lowest_superposition()

