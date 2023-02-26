from datetime import datetime
import time

class Build:

    """
    uuid
    account_id
    create_date
    finish_date
    status
    file_name (uuid+createDate.json)
    """

    def __init__(self):
        self.uuid = ""
        self.account_id = ""
        self.create_date = int(time.time())
        self.finish_date = ""
        self.status = ""
        self.file_name = ""

    def __str__(self):
        return f"{self.account_id}({self.create_date},{self.status},{self.file_name})"

    def setResultFileName(self):
        self.file_name = self.uuid + "_" + str(self.create_date) + ".json"

    def setFinishDate(self):
        self.finish_date = int(time.time())

    def dump(self):
        return {
            'uuid' : self.uuid,
            'account_id' : self.account_id,
            'create_date' : self.create_date,
            'finish_date' : self.finish_date,
            'status' : self.status,
            'file_name' : self.file_name,
        }

    def initWithJson(self, json):
        self.uuid = json.get('uuid')
        self.account_id = json.get('account_id')
        self.create_date = json.get('create_date')
        self.finish_date = json.get('finish_date')
        self.status = json.get('status')
        self.file_name = json.get('file_name')

    def initWithDB(self, dbResult):
        self.uuid = dbResult[0]
        self.account_id = dbResult[1]
        self.create_date = int(datetime.timestamp(dbResult[2]))
        if(dbResult[3] is None):
            self.finish_date = ""
        else:
            self.finish_date = int(datetime.timestamp(dbResult[3]))
        self.status = dbResult[4]
        self.file_name = dbResult[5]
        



