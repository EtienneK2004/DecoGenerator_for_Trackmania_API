from flask import Flask
import json
import random

"""
class BlockSet:
    listBlocks = []
    name = ""
    def __init__(self, nameOfSet, listOfBlocks):
        self.listBlocks = listOfBlocks
        self.name = nameOfSet
"""
blockSetList = []

def loadBlockSetList()
    with f as open("blockSetList.json", 'r'):
        setList = json.load(f)
    blockSetList = setList.sorted(key=lambda x: x['name'])



def binary_search_BlockSet(x):
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        if blockSetList[mid]['name'] < x['name']:
            low = mid + 1

        elif blockSetList[mid]['name'] > x['name']:
            high = mid - 1

        else:
            return blockSetList[mid]

    # If we reach here, then the element was not present
    return None

app = Flask(__name__)

@app.route("/get-blocks/<nameofset>", methods=["GET"])
def getBlocks(nameofset):
   set = binary_search(nameofset)
   if set is None:
       return "No set found."


if __name__ == '__main__':
    app.run(debug=True)
    print("API lancée")