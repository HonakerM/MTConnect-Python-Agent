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
from .device import MTComponent, MTDevice
from .loghandler import MTLogger
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
        MTLogger.info("Initializing MTConnect Agent")
        #set variables
        self.hostname = hostname

        #initalize buffer
        self.buffer = MTBuffer()

        #read device information
        file_location = os.getenv('MTCDeviceFile',loc)
        MTLogger.debug('Reading Devices from {}'.format(file_location))
        device_data = read_devices(file_location)

        

        #Update item dict to contain all items
        self.device_dict, self.device_xml  = device_data
        for device in self.device_dict.values():
            self.item_dict.update(device.item_dict)
            self.component_dict.update(device.component_dict)

        #generate instanceId -64bit int uuid4 is 128 so shift it
        self.instanceId = str(uuid.uuid4().int & (1<<64)-1)
        MTLogger.debug('Settings UUID to {}'.format(self.instanceId))

        #create inital values for item
        for item in self.item_dict.values():
            self.push_data(item.id, "UNAVAILABLE")
        
        MTLogger.info("Finished Initalizing MTConnect Agent")

    #
    # Accessor Functions
    #
    def get_device_list(self):
        return self.device_dict.values()
    
    def get_device(self,name=None):
        if(name is None):
            return get_device_list()[0]
        else:
            return self.device_dict[name]
    #
    # Data Functions
    #

    #validate pushing data
    def get_dataId(self,dataId):
        for device in self.device_dict.values():
            if(dataId in device.get_sub_item()):
                return device.item_dict[dataId]
        raise ValueError('DataID {} is not found'.format(dataId))

    #push data from machines
    def push_data(self, dataId, value):
        dataItem = self.get_dataId(dataId)
        new_data = MTDataEntity(dataItem, value)
        self.buffer.push(new_data)


    #
    # MTConnect/XML Functions   
    # 

    def get_header(self):
        header_element = ElementTree.Element('Header')
        header_element.set('version','1.6.0.0')
        header_element.set('instanceId',str(self.instanceId))
        header_element.set('creationTime',datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
        header_element.set('bufferSize',str(self.buffer.size()))
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
    def sample(self, path=None, start=None, count=None):
        #data validation

        #if count is given but not start
        if(start is None and count is not None):
            if(count <0):
                start = self.buffer.last_sequence
            else:
                start = self.buffer.first_sequence

        if(start is None):
            start = self.buffer.first_sequence

        if(count is None):
            count = 100

        if(not isinstance(start, Number) and start<0):
            return MTInvalidRequest(self, "Start must be a non negative number").to_xml()

        if(not isinstance(count, Number) ):
            return MTInvalidRequest(self, "Count must be a number").to_xml()
        
        if(self.buffer.empty()):
            return MTInvalidRange(self, "Buffer is currently empty").to_xml()

        if(start < self.buffer.first_sequence or start > self.buffer.last_sequence):
            return MTInvalidRange(self, "Start must be between {} and {}".format(self.buffer.first_sequence, self.buffer.last_sequence)).to_xml()
    
        if(abs(count) > self.buffer.size()):
            return MTInvalidRange(self, "Count must not be greater than {}".format(self.buffer.size()))
        
        #put count and start into usable formats
        if(count < 0):
            start = start + count
            count = abs(count)
        
        end = start + count

        #apply path variable
        if(path is not None):
            component_list = process_path(self.device_xml, path, self.item_dict, self.component_dict)
        else:
            component_list = list(self.device_dict.values())

        #get all sub items from path
        item_list = set()
        for component in component_list:
            item_list = item_list.union(set(component.get_all_sub_items()))
        item_list = list(item_list)

        #get all itesm last dataitem
        current_dict = {}
        for item in item_list:

            #get data 
            data = item.get_data(start, end)
            
            #if device had no data yet then initialize
            if(item.device not in current_dict):
                current_dict[item.device] = {}

            #if component has no data then initialize
            if item.parent_component not in current_dict[item.device]:
                current_dict[item.device][item.parent_component] = {}

            if item.category not in current_dict[item.device][item.parent_component]:
                current_dict[item.device][item.parent_component][item.category]=[]

            current_dict[item.device][item.parent_component][item.category].append(data)

        #format the output xml
        current_stream = ElementTree.Element('Streams')
        for device in current_dict:
            #create root device stream
            device_element = ElementTree.SubElement(current_stream, 'DeviceStream')
            device_element.set('name',device.name)
            device_element.set('uuid',device.uuid)


            #loop through all data iterms and compoments
            for component in current_dict[device]:

                #get root component stream
                stream_element = ElementTree.SubElement(device_element, 'ComponentStream')
                if(isinstance(component, MTComponent)):
                    stream_element.set('component',component.type)
                elif(isinstance(component, MTDevice)):
                    stream_element.set('component','Device')
                stream_element.set('name',component.name)
                stream_element.set('componentId',component.id)

                #get data
                component_data = current_dict[device][component]

                #For each category add data to xml
                for category in component_data:
                    sample_container = ElementTree.SubElement(stream_element, category.title()+'s')
                    for item_list in component_data[category]:
                        for item in item_list:
                            sample_container.append(item.get_xml())
        #format final xml
        root_container = ElementTree.Element('MTConnectStreams')
        root_container.append(self.get_header())
        root_container.append(current_stream)
        return ElementTree.tostring(root_container).decode()


    #run MTConnnect current command
    def current(self, at=None, path=None):
        #data validation
        if(at is None):
            at = self.buffer.last_sequence


        if(not isinstance(at, Number) or at<0):
            return MTInvalidRequest(self, "At must be a non negative number")
        
        if(self.buffer.empty()):
            return MTInvalidRange(self, "Buffer is currently empty")

        if(at < self.buffer.first_sequence or at > self.buffer.last_sequence):
            return MTInvalidRange(self, "At must be between {} and {}".format(self.buffer.first_sequence, self.buffer.last_sequence))

        #apply path variable
        if(path is not None):
            component_list = process_path(self.device_xml, path, self.item_dict, self.component_dict)
        else:
            component_list = list(self.device_dict.values())

        #get all sub items from path
        item_list = set()
        for component in component_list:
            item_list = item_list.union(set(component.get_all_sub_items()))
        item_list = list(item_list)

        #get all itesm last dataitem
        current_dict = {}
        for item in item_list:

            #get data 
            data = item.get_current(at)
            
            #if device had no data yet then initialize
            if(item.device not in current_dict):
                current_dict[item.device] = {}

            #if component has no data then initialize
            if item.parent_component not in current_dict[item.device]:
                current_dict[item.device][item.parent_component] = {}

            if item.category not in current_dict[item.device][item.parent_component]:
                current_dict[item.device][item.parent_component][item.category]=[]
            
            
            
            current_dict[item.device][item.parent_component][item.category].append(data)
        
        #format the output xml
        current_stream = ElementTree.Element('Streams')
        for device in current_dict:
            #create root device stream
            device_element = ElementTree.SubElement(current_stream, 'DeviceStream')
            device_element.set('name',device.name)
            device_element.set('uuid',device.uuid)


            #loop through all data iterms and compoments
            for component in current_dict[device]:

                #get root component stream
                stream_element = ElementTree.SubElement(device_element, 'ComponentStream')
                if(isinstance(component, MTComponent)):
                    stream_element.set('component',component.type)
                elif(isinstance(component, MTDevice)):
                    stream_element.set('component','Device')
                stream_element.set('name',component.name)
                stream_element.set('componentId',component.id)

                #get data
                component_data = current_dict[device][component]

                #For each category add data to xml
                for category in component_data:
                    sample_container = ElementTree.SubElement(stream_element, category.title()+'s')
                    for item in component_data[category]:
                        
                        sample_container.append(item.get_xml())
        #format final xml
        root_container = ElementTree.Element('MTConnectStreams')
        root_container.append(self.get_header())
        root_container.append(current_stream)
        return ElementTree.tostring(root_container).decode()
            


    def error(self, error_text):
        pass
