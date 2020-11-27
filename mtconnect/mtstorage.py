import os #enviormentl variabels
import datetime #get currenttime

class MTDataEntity():
    # ! Use: Handle the individual data values
    # ? Data: Holds sequence number, tiemstamp, and data 

    #sequence number in buffer and timestamp
    sequence_number = None
    timestamp = None

    #data category and subcategory in generic terms
    type = None
    sub_type = None

    #data category in MTConnect terms
    MTC_dataid = None

    #actual value
    value = None


    def __init__(self, DataId, value, type=None, sub_type=None):
        self.MTC_dataid = DataId
        self.value = value
        self.timestamp = datetime.datetime.utcnow()

        if(type is not None):
            self.type = type

        if(sub_type is not None):
            self.sub_type = sub_type

    def set_sequence(self, number):
        self.sequence_number = number
        return self.sequence_number

    def get_sequence(self):
        return self.sequence_number

    def get_time_str(self):
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")


class MTBuffer():
    # ! Use: Handle buffer operations for MTConnect agent
    # ? Data: Holds all data about sequencing and previous values

    #buffer variables
    buffer = None
    buffer_size = None

    #keep track of buffer location
    first_sequence = None #oldest piece of data
    last_sequence = None #newest piece of data
    next_sequence = 0

    #keep track of previous values flowing through the buffer
    last_value = {}


    def __init__(self, **kwargs):
        #get buffer size
        if(buffer_length is None):
            buffer_length = os.environ.get("BUFFER_SIZE",16384)

        #initialize buffer    
        self.buffer_size = buffer_length
        self.buffer = [None] * self.buffer_size


    def push(self, DataElement):
        if(not isinstance(DataElement,MTDataEntity)):
            raise ValueError("DataElement is not of type MTDataEntity")
        
        #DataElement.set_sequence(self.next_sequence)
        

        




    
