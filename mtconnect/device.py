#general imports
import uuid 
from xml.etree import ElementTree

#import mtcitems
from .standard_list import MTC_DataID_list
from .storage import MTDataEntity

#class helper for MTGeneric to display component tree
def tree_helper(component, level=0):
    output_string = '+'+ ('-'*5)*level + str(component.id)+'\n'
    for item in component.get_sub_items():
        output_string = output_string + '+'+('-'*5)*(level+1)+'+'+str(item.id)+'\n'
        
    component_list = component.get_sub_components()
    
    for comp in component_list:
        output_string = output_string + tree_helper(comp,level+1)

    return output_string

#class helper for MTGeneric to get all subcomponents
def item_helper(component):
    output_list = []
    item_list = component.get_sub_items()
    for item in item_list:
        output_list.append(item)
    
    component_list = component.get_sub_components()
    for component in component_list:
        output_list = output_list + item_helper(component)
    
    return output_list
        

class MTGeneric:
    # ! Use: Generic item for all parts of device. Includes components and data_list
    # ? Data: Holds id,name, and attributes as well as parent componnetn and data_list

    #generic variables
    id = None
    name = None

    #attributes
    attributes = {}

    #parrent component
    parent_component = None

    def __init__(self, id, name, component):
        if(id is None):
            raise ValueError('Missing required id for MTC')
        

        self.id = id
        self.name = name
        self.parent_component = component

        self.attributes = {}
        self.data_list = []


    #add attribute to container
    def add_attribute(self, name, value):
        self.attributes[name] = value
    
    def __str__(self):
        return "{} with id {} and name {} with parent {}".format(type(self),self.id,self.name,self.parent_component)
    

class MTGenericContainer(MTGeneric):
    #generic variables
    description = None

    #variables used for storage of sub items
    sub_components = {}
    items = {}

    #raw xml data
    xml_data = None

    def __init__(self,id, name, xml_data, parent_component, description=None):
        super().__init__(id, name, parent_component)

        self.xml_data = xml_data
        self.description = description
        self.sub_components = {}
        self.items = {}
        

    #add subaccount directly to container
    def add_subcomponent(self, Component):
        self.sub_components[Component.id] = Component
    
    #add item directly to conrainter
    def add_item(self, Item):
        self.items[Item.id] = Item
    
    #get list of subcomponents
    def get_sub_components(self):
        return list(self.sub_components.values())
    
    #get list of dataitems
    def get_sub_items(self):
        return list(self.items.values())

    #get all sub items of component
    def get_all_sub_items(self):
        return item_helper(self)

    def display_tree(self):
        return tree_helper(self)
    
    def generate_xml(self):
        return ElementTree.tostring(self.xml_data)

class MTDevice(MTGenericContainer):
    #generic variables
    uuid = None

    #variables used for traversal of sub items
    item_dict = {}
    component_dict = {}
    
    def __init__(self,id, name,xml_data, unique_id=None, description=None):
        super().__init__(id, name, xml_data, None, description)
        
        if(unique_id is None):
            unique_id = uuid.uuid4()

        self.uuid = unique_id
        self.item_dict={}
        self.component_dict={}
    
    def add_subcomponent(self, Component):
        super().add_subcomponent(Component)
        self.component_dict[Component.id] = Component

    def add_item(self, Item):
        super().add_item(Item)
        self.item_dict[Item.id] = Item

    #add device to device list for traversal
    def add_sub_item(self, Item):
        self.item_dict[Item.id] = Item

    #add component to device list for traversal
    def add_sub_component(self, Component):
        self.component_dict[Component.id] = Component
    
    def get_sub_item(self):
        return self.item_dict.keys()

class MTComponent(MTGenericContainer):
    #descriptor variables
    type = None

    #parent variables
    device = None
    
    def __init__(self,id, name, type, xml_data, parent_component, device, description=None):
        super().__init__(id,name, xml_data, parent_component, description)
  
        self.type = type
        self.device = device

class MTDataItem(MTGeneric):
    category = None
    type = None

    #parent variable
    device = None

    #Last value thats outside the buffer
    ##used in current 
    last_value = None

    #list of data entity assigned
    data_list = []

    def __init__(self, id, name, type, category, device, component):
        

        category = category.upper()
        if(None in [id, type,category, component, device]):
            raise ValueError('Missing required value for DataItem')
        
        if(category not in ['SAMPLE','CONDITION','EVENT']):
            raise ValueError('{} is not a valid category'.format(category))

        if(type not in MTC_DataID_list):
            raise ValueError('{} is not a valid type'.format(type))

        if(id in device.get_sub_item()):
            raise ValueError('id must be unique. {} has been used'.format(id))
        
        super().__init__(id,name,component)

        self.type = type
        self.category = category

        self.device = device

        

    
    #Handle DataEntitys assigned
    def push_data(self, DataEntity):
        if(self.last_value is None):
            self.last_value = DataEntity

        self.data_list.append(DataEntity)
    
    def pop_data(self):
        self.data_list.pop(0)

    def get_data(self, start_sequence=float('-inf'), end_sequence=float('inf')):
        output_list = []
        for data in self.data_list:
            if(data.sequence_number>start_sequence and data.sequence_number<=end_sequence):
                output_list.append(data)
        return output_list
    
    def get_current(self, seq=float('inf')):
        data = self.get_data(end_sequence=seq)
        if(not data):
            return self.last_value

        return data[-1]
    
