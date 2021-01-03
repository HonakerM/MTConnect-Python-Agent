#general imports
from xml.etree import ElementTree

#MTConnect imports
from .device import MTDevice, MTComponent, MTDataItem




#
# AGENT XML Helpers
#
def process_path(device_xml,path, item_dict, component_dict):  
    xml_list = device_xml.findall(path)
    component_list = []
    for element in xml_list:
        
        id = element.get('id')
        print(id)
        if(id in item_dict):
            component_list.append(item_dict[id])

        if(id in component_dict):
            component_list.append(component_dict[id])
    return component_list
        

#
# DEVICE XML Helpers
#

#function to process all of the dataitems on a component
def process_dataitem(item_list, device, component):
    for item in item_list:
        #get required objects
        id = item.get('id')
        category = item.get('category')
        type = item.get('type')
        name = item.get('name')

    
        new_item = MTDataItem(id,name, type,category,device,component)
        
        for attribute in item.items():
            new_item.add_attribute(attribute[0], attribute[1])
        component.add_item(new_item)
        device.add_sub_item(new_item)

#function to recursively add components
def process_components(component_list, device, parent_component):
    for component in component_list:
        #get component attributes
        name = component.get('name')
        type = component.tag
        id = component.get('id')
        description = component.find('Description')

        #get the text value for the description
        if(description is not None):
            description = description.text

        #create top level component
        new_component = MTComponent(id, name, type, component, parent_component, device, description)
        device.add_sub_component(new_component)

        parent_component.add_subcomponent(new_component)

        #get list of attributes
        for attribute in component.items():
            new_component.add_attribute(attribute[0], attribute[1])

        #get list of data items
        component_items = component.find('DataItems')
        if(component_items is not None):
            process_dataitem(component_items,device, new_component)

        #get list of subcomponents
        sub_component_item = component.find('Components')
        if(sub_component_item is not None):
            sub_component_list = sub_component_item.getchildren()
            process_components(sub_component_list, device, new_component)        

#read device xml from file
def read_devices(file):
    #read data file
    try:
        device_tree = ElementTree.parse(file)
    except FileNotFoundError:
        raise ValueError('{} is not a valid file'.format(file))

    #list of devices
    device_list = {}

    #get devices
    root = device_tree.getroot()
    for device in root.getchildren():
        #get identifiers for device
        device_name = device.get('name')
        device_uuid = device.get('uuid')
        device_id = device.get('id')
        device_description = device.find('Description')

        #get the text value for the description
        if(device_description is not None):
            device_description = device_description.text

        #create device
        new_device = MTDevice(device_id,device_name,device, device_uuid,device_description)
        
        #get list of attributes
        for attribute in device.items():
            new_device.add_attribute(attribute[0], attribute[1])

        #get list of data items
        device_items = device.find('DataItems')
        if(device_items is not None):
            process_dataitem(device_items,new_device, new_device)

        #get list of subcomponents
        component_item = device.find('Components')
        if(component_item is not None):
            component_list = component_item.getchildren()
            process_components(component_list, new_device, new_device)

        device_list[new_device.id]=new_device

    return (device_list, device_tree)

        
    