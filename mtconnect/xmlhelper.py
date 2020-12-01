from xml.etree import ElementTree
from device import MTDevice, MTComponent, MTDataItems
        
from json import loads, dumps

def read_devices(file):

    device_tree = ElementTree.parse(file)
    root = device_tree.getroot()
    print(dir(root))
    for device in root.getchildren():
        #get identifiers
        name = device.get('name')
        uuid = device.get('uuid')
        id = device.get('id')
        description = device.find('Description')

        #name and uuid are required for devices
        if(not name or not uuid):
            raise ValueError('Name and UUID required for device')
        
        if(description is not None):
            description = description.text

        new_device = MTDevice(name,uuid,id,description)
        


    '''
    device_string =  open(file, 'r').read()
    device_dictionary = xmltodict.parse(device_string,  process_namespaces=True)

    device_dictionary = loads(dumps(device_dictionary))
    device_list = device_dictionary['Devices']
    print(device_list)
    for device in device_list:
        print(device)
        description=None
        if 'Description' in device:
            description = device['Description']

        new_device = MTDevice(device['@id'],device['@name'],device['@uuid'], description)
        print(1)
        for dataItem in device['DataItems']['DataItem']:
            print(1)

    #for devices in device_dictionary['Devices']:
    #    print(device_dictionary[devices])
    
    '''
read_devices('../tests/test_probe.xml')
        
    