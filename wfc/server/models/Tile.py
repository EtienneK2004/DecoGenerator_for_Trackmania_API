import random

class Tile:
    superpositions = None
    collapse = None


    def __init__(self, blocks):
        self.superpositions = list(blocks)




    def get_superpositions(self):
        return self.superpositions

    def nb_superpositions(self):
        return len(self.superpositions)

    def reset_superpositions(self, newSuperpositions=None):
        s = self.superpositions
        if newSuperpositions is None:
            self.superpositions = []
        else:
            self.superpositions = newSuperpositions
        return s




    def isCollapse(self):
        return self.collapse is not None


    def force_collapse(self, superposition=None):
        if len(self.superpositions) == 0:
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
            'b': self.collapse.split('_')[0].split('.')[0],
            'd': self.collapse.split('_')[1],
            'v': None, 'c': 0, 'm': 'Normal'
        }
