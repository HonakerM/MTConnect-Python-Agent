


class MTDevice:
    id = None
    name = None
    uuid = None
    description = None
    
    sub_components = {}
    items = {}

    def __init__(self,name, uuid,id=None, description=None):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.description = description

class MTComponent:
    id = None
    name = None
    type = None

    sub_components = {}
    items = {}


class MTDataItems:
    id = None
    name = None
    category = None
    nativeUnits = None
    subType = None
    type = None
    units = None

    
