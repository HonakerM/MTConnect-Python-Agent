import os #enviormentl variabels
import datetime #get currenttime
import numbers #verrify value is number
from xml.etree import ElementTree #generate xml

#MTConnect Imports
from .helper import type_to_pascal
class MTDataEntity():
    # ! Use: Handle the individual data values
    # ? Data: Holds sequence number, tiemstamp, and data 

    #sequence number in buffer and timestamp
    sequence_number = None
    timestamp = None

    #The MTDataItem that this data refernced
    dataItem = None

    #actual value
    value = None


    def __init__(self, dataItem, value):
        #set values
        self.dataItem = dataItem
        if(dataItem.category =='SAMPLE' and (not isinstance(value, numbers.Number) and value!="UNAVAILABLE")):
            raise ValueError('SAMPLE value must be number')
            
        if(dataItem.category =='EVENT' and not isinstance(value, str)):
            raise ValueError('EVENT value must be a string')

        if(dataItem.category =='CONDITION' and value not in ['UNAVAILABLE', 'NORMAL', 'WARNING', 'FAULT']):
            raise ValueError('CONDITION value must be one of UNAVAILABLE, NORMAL, WARNING, or FAULT')

        self.value = value
        self.timestamp = datetime.datetime.utcnow()

    #
    # Accessor Functions 
    #
    
    #get timestamp as MTCOnnect formated string
    def get_time_str(self):
        return self.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")

    #get xml data for current/sample
    def get_xml(self):
        element = ElementTree.Element(type_to_pascal(self.dataItem.type))
        element.set('dataItemId',self.dataItem.id)
        element.set('timestamp',self.get_time_str())
        if(self.dataItem.name is not None):
            element.set('name',self.dataItem.name)

        element.set('sequence',str(self.sequence_number))

        element.text = str(self.value)
        return element


    #
    # Mutator Functions 
    #
    def set_sequence(self, number):
        self.sequence_number = number
        return self.sequence_number


class MTBuffer():
    # ! Use: Handle buffer operations for MTConnect agent
    # ? Data: Holds all data about sequencing and previous values

    #buffer variables
    buffer = None
    buffer_size = None

    #keep track of buffer location
    first_sequence = None #oldest piece of data
    last_sequence = None #newest piece of data
    buffer_pos = 0 #keep track of place in buffer



    #
    # Constructor Functions
    #
    def __init__(self, buffer_length=None):
        #get buffer size
        if(buffer_length is None):
            buffer_length = int(os.environ.get("BUFFER_SIZE",16384))

        #initialize buffer    
        self.buffer_size = buffer_length
        self.buffer = [None] * self.buffer_size

    #
    # Accessor Functions
    #
    def get_buffer(self):
        return self.buffer

    def get_data(self, seq, count=None):
        #if requested sequence is to below sequence
        if(seq<self.first_sequence):
            return ([],self.first_sequence)
        
        #if count is none get max count
        if(count == None):
            count = self.buffer_size

        #if count is <= 0 then return nothing
        if(count <= 0):
            return ([],seq)

        #get location in the buffer
        buffer_loc = seq - self.first_sequence

        #get end position and adjust if it goes over
        end_pos = buffer_loc + count
        if(end_pos >= self.buffer_size):
            end_pos = self.buffer_size

        #get next_sequence calculations
        next_sequence = self.buffer[end_pos-1].sequence_number + 1
        return (self.buffer[buffer_loc:end_pos],next_sequence)
    
    def empty(self):
        return self.first_sequence is None

    def size(self):
        return self.buffer_size    

    #
    # Mutator  Functions
    #
    def push(self, DataElement):
        #if DataElement is not the correct type
        if(not isinstance(DataElement,MTDataEntity)):
            raise TypeError("DataElement is not of type MTDataEntity")

        #if sequence number is greater than the buffer size
        if(self.buffer_pos >= self.buffer_size):
            #get last item
            last_item = self.buffer.pop(0)

            #remove last item from refernced Device
            last_item.dataItem.pop_data()
            
            #update last item list
            last_item.last_value = last_item

            #update sequence
            self.first_sequence = self.buffer[0].sequence_number

            #add last item
            self.buffer.append(None)
            self.buffer_pos = self.buffer_size-1
        
        #get new sequence number
        if(self.last_sequence is None):
            sequence_number = 1
        else:
            sequence_number = self.last_sequence + 1

        #set sequence number and add to list
        DataElement.set_sequence(sequence_number)
        self.buffer[self.buffer_pos] = DataElement

        #add data to refernced dataItem
        DataElement.dataItem.push_data(DataElement)

        #update counter and static variables
        self.buffer_pos = self.buffer_pos + 1
        self.last_sequence = sequence_number
        if(self.first_sequence is None):
            self.first_sequence = sequence_number
