
#class helper for MTDevice/MTComponent to display component tree
def tree_helper(component, level=0):
    output_string = '+'+ ('-'*5)*level + str(component.id)+'\n'
    for item in component.get_sub_items():
        output_string = output_string + '+'+('-'*5)*(level+1)+'+'+str(item.id)+'\n'
        
    component_list = component.get_sub_components()
    
    for comp in component_list:
        output_string = output_string + tree_helper(comp,level+1)

    return output_string


class MTDevice:
    #generic variables
    id = None
    name = None
    uuid = None
    description = None
    
    #variables used for storage of sub items
    sub_components = {}
    items = {}

    #variables used for traversal of sub items
    item_list = {}
    component_list = {}

    attributes = {}

    def __init__(self,name, uuid,id, description=None):
        if(id is None):
            raise ValueError('Missing required value for Component')
        
        self.id = id
        self.name = name
        self.uuid = uuid
        self.description = description
    
    #add subaccount directly to device
    def add_subcomponent(self, Component):
        self.sub_components[Component.id] = Component
        self.component_list[Component.id] = Component

    #add add item directly to device
    def add_item(self, Item):
        self.items[Item.id] = Item
        self.item_list[Item.id] = Item

    #add device to device list for traversal
    def add_sub_item(self, Item):
        self.item_list[Item.id] = Item

    #add component to device list for traversal
    def add_sub_component(self, Component):
        self.component_list[Component.id] = Component

    def add_attribute(self, name,value):
        self.attributes[name] = value
    
    def get_sub_components(self):
        return list(self.sub_components.values())
    
    def get_sub_items(self):
        return list(self.items.values())

    def display_tree(self):
        return tree_helper(self)

class MTComponent:
    #descriptor variables
    id = None
    name = None
    type = None

    #parent variables
    device = None
    parent_component = None

    #variables used for storage of subaccounts
    sub_components = {}
    items = {}

    attributes = {}

    def __init__(self,name, id, type, device, parent_component):
        if(None in [id, type, device]):
            raise ValueError('Missing required value for Component')
            
        self.id = id
        self.name = name
        self.type = type
        self.device = device
        self.parent_component = parent_component

        self.sub_components = {}
        self.items = {}
        self.attributes = {}
    
    #add subaccount directly to device
    def add_subcomponent(self, Component):

        #self.sub_components[Component.id] = 1
        self.sub_components[Component.id] = Component


    #add add item directly to device
    def add_item(self, Item):
        self.items[Item.id] = Item

    def add_attribute(self, name,value):
        self.attributes[name] = value
    
    def get_sub_components(self):
        return list(self.sub_components.values())
    
    def get_sub_items(self):
        return list(self.items.values())

    def display_tree(self):
        return tree_helper(self)

    




class MTDataItem:
    id = None
    category = None
    type = None
    attributes = {}

    #parent variable
    component = None
    device = None

    def __init__(self, id, type, category, device, component):
        if(None in [id, type,category, component, device]):
            raise ValueError('Missing required value for DataItem')
        self.id = id
        self.type = type
        self.category = category

        self.device = device
        self.component = component
    
    def add_attribute(self, name, value):
        self.attributes[name] = value


    
