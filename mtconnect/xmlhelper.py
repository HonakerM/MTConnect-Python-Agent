from xml.etree import ElementTree

        

def read_devices(file):
    output_dict = {}
    device_tree = ElementTree.parse(file)
    root = device_tree.getroot()
    for device in root:
        
    