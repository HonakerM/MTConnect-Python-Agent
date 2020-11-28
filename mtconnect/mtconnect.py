from mtconnect.storage import MTBuffer, MTDataEntity

class MTConnect():
    # ! Use: Handle MTConnect agent
    # ? Data:

    buffer = None
    
    def __init__(self):
        self.buffer = MTBuffer()

    #validate data
    def validate_data(self,data):
        pass

    #push data from machines
    def push_data(self, DataId, value, type=None, sub_type=None):
        pass
    
    #run MTConnect probe command
    def probe(self):
        pass

    #run MTConnect sample command
    def sample(self, path, start, count, interval):
        pass

    #run MTConnnect current command
    def current(self, at, path):
        pass