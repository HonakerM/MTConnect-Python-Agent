#general imports
import os


#mtconnect imports
from .storage import MTBuffer, MTDataEntity
from .xmlhelper import read_devices

class MTConnect():
    # ! Use: Handle MTConnect agent
    # ? Data:

    buffer = None
    
    device_dict = None

    def __init__(self,file_location='./device.xml'):
        self.buffer = MTBuffer()
        file_location = os.getenv('MTCDeviceFile',file_location)
        device_dict = read_devices(file_location)
        

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