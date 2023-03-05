
class Socket:
    name = None
    friends = None #a dic can be better #TODO check

    def __init__(self, name):
        self.name = name
        self.friends = []
    
    def addFriend(self, friend):
        if(not friend in self.friends):
            self.friends.append(friend)
    
    def getFriends(self):
        return self.friends

    def __eq__(self, other):
        return self.name == other.name
    
    #def __str__(self):
    #    return self.name