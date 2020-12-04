#general imports
from xml.etree import ElementTree

#import mtcitems
from .standard_list import MTC_DataID_list

#class helper for MTDevice/MTComponent to display component tree
def tree_helper(component, level=0):
    output_string = '+'+ ('-'*5)*level + str(component.id)+'\n'
    for item in component.get_sub_items():
        output_string = output_string + '+'+('-'*5)*(level+1)+'+'+str(item.id)+'\n'
        
    component_list = component.get_sub_components()
    
    for comp in component_list:
        output_string = output_string + tree_helper(comp,level+1)

    return output_string

class MTGenericContainer:
    #generic variables
    id = None
    name = None
    description = None

    #attributes
    attributes = {}

    #parent container
    parent_component = None

    #variables used for storage of sub items
    sub_components = {}
    items = {}

    #raw xml data
    xml_data = None

    def __init__(self,name, id, xml_data, parent_component, description=None):
        if(id is None):
            raise ValueError('Missing required value for Component')
        
        self.id = id
        self.name = name
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

    #add attribute to container
    def add_attribute(self, name,value):
        self.attributes[name] = value
    
    #get list of subcomponents
    def get_sub_components(self):
        return list(self.sub_components.values())
    
    #get list of dataitems
    def get_sub_items(self):
        return list(self.items.values())


    def display_tree(self):
        return tree_helper(self)
    
    def generate_xml(self):
        return ElementTree.tostring(self.xml_data)

class MTDevice(MTGenericContainer):
    #generic variables
    uuid = None

    #variables used for traversal of sub items
    item_list = {}
    component_list = {}
    
    def __init__(self,name,id,xml_data, uuid=None, description=None):
        super().__init__(name, id, xml_data, None, description)

        self.uuid = uuid
        self.item_list={}
        self.component_list={}
    
    def add_subcomponent(self, Component):
        super().add_subcomponent(Component)
        self.component_list[Component.id] = Component

    def add_item(self, Item):
        super().add_item(Item)
        self.item_list[Item.id] = Item

    #add device to device list for traversal
    def add_sub_item(self, Item):
        self.item_list[Item.id] = Item

    #add component to device list for traversal
    def add_sub_component(self, Component):
        self.component_list[Component.id] = Component
    
    def get_sub_item(self):
        return self.item_list.keys()

class MTComponent(MTGenericContainer):
    #descriptor variables
    type = None

    #parent variables
    device = None
    
    def __init__(self,name, id, type, xml_data, parent_component, device, description=None):
        super().__init__(name,id, xml_data, parent_component, description)
  
        self.type = type
        self.device = device

class MTDataItem:
    id = None
    category = None
    type = None
    attributes = {}

    #parent variable
    component = None
    device = None

    def __init__(self, id, type, category, device, component):
        category = category.upper()
        if(None in [id, type,category, component, device]):
            raise ValueError('Missing required value for DataItem')
        
        if(category not in ['SAMPLE','CONDITION','EVENT']):
            raise ValueError('{} is not a valid category'.format(category))

        if(type not in MTC_DataID_list):
            raise ValueError('{} is not a valid type'.format(type))

        if(id in device.get_sub_item()):
            raise ValueError('id must be unique. {} has been used'.format(id))

        self.id = id
        self.type = type
        self.category = category

        self.device = device
        self.component = component
    
    def add_attribute(self, name, value):
        self.attributes[name] = value


    
