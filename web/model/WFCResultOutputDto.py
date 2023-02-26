from StatusEnum import status as BuildStatus

class WFCResultOutputDto :

    def __init__(self):
        self.uuid = ""
        self.status = BuildStatus["Created"]
        self.JsonBlocks = []

    def json(self):
        return {
            'uuid' : self.uuid,
            'status' : self.status,
            'JsonBlocks' : self.JsonBlocks
        }