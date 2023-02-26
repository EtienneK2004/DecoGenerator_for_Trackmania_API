from StatusEnum import status as BuildStatus

class WFCServerOutputDto :

    def __init__(self):
        self.uuid = ""
        self.status = BuildStatus["Created"]
        self.file_name = ""
        self.parameters = [{"blockset":"firstSet"}]

    def json(self):
        return {
            'uuid' : self.uuid,
            'status' : self.status,
            'file_name' : self.file_name,
            'parameters' : self.parameters
        }