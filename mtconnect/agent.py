#general imports
import os
import uuid  
from xml.etree import ElementTree
from datetime import datetime
from numbers import Number

#mtconnect imports
from .storage import MTBuffer, MTDataEntity
from .xmlhelper import read_devices, process_path
from .error import MTInvalidRequest, MTInvalidRange


class MTConnect():
    # ! Use: Handle MTConnect agent
    # ? Data:
    #instanceID 
    instanceId = None
    hostname = None

    #item buffer
    buffer = None
    asset_buffer = None

    #dictionary of devices
    device_dict = None
    device_xml = None

    #used for traversal
    item_dict = {} # list of a
    component_dict = {} # list of components


    def __init__(self,loc='./device.xml',hostname='http://0.0.0.0:80'):
        #set variables
        self.hostname = hostname

        #initalize buffer
        self.buffer = MTBuffer()

        #read device information
        file_location = os.getenv('MTCDeviceFile',loc)
        self.device_dict, self.device_xml = read_devices(file_location)

        for device in self.device_dict.values():
            self.item_dict.update(device.item_dict)
            self.component_dict.update(device.component_dict)

        #generate instanceId -64bit int uuid4 is 128 so shift it
        self.instanceId = uuid.uuid4().int & (1<<64)-1

    #validate pushing data
    def get_dataId(self,dataId):
        for device in self.device_dict.values():
            if(dataId in device.get_sub_item()):
                return device.item_list[dataId]
        raise ValueError('DataID {} is not found'.format(dataId))

    #push data from machines
    def push_data(self, dataId, value):
        dataItem = self.get_dataId(dataId)
        new_data = MTDataEntity(dataItem, value)
        self.buffer.push(new_data)

    def get_header(self):
        header_element = ElementTree.Element('Header')
        header_element.set('version','1.6.0.0')
        header_element.set('instanceId',str(self.instanceId))
        header_element.set('creationTime',datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        header_element.set('bufferSize',str(self.buffer.buffer_size))
        header_element.set('assetBufferSize','0')
        header_element.set('assetCount','0')
        return header_element

    #run MTConnect probe command
    def probe(self):
        root_container = ElementTree.Element('MTConnectDevices')
        root_container.append(self.get_header())

        device_container = ElementTree.SubElement(root_container, 'Devices')
        for device in self.device_dict:
            device_container.append(self.device_dict[device].xml_data)
        
        return ElementTree.tostring(root_container).decode()

    #run MTConnect sample command
    def sample(self, path, start, count, interval):
        pass

    #run MTConnnect current command
    def current(self, at, path=None, interval=None):
        #data validation
        if(at is None and interval is None):
            raise MTInvalidRequest("Either At or Interval must not be None")

        if(at is not None and interval is not None):
            raise MTInvalidRequest("At and Interval must not be used in conjunction")

        if(not isinstance(at, Number) and at<0):
            raise MTInvalidRequest("At must be a non negative number")
        
        if(self.buffer.empty()):
            raise MTInvalidRange("Buffer is currently empty")

        if(at < self.buffer.first_sequence or at > self.buffer.last_sequence):
            raise MTInvalidRange("At must be between {} and {}".format(self.buffer.first_sequence, self.buffer.last_sequence))

        #apply path variable
        if(path is not None):
            component_list = process_path(self.device_xml, path, self.item_dict, self.component_dict)
        else:
            component_list = list(self.device_dict.values())
        



        #
        
                

    def error(self, error_text):
        pass