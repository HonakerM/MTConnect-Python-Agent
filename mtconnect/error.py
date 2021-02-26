from xml.etree import ElementTree

class MTError():
    name = ''
    message = ''

    agent = None

    def __init__(self,agent,message):
        self.agent = agent
        self.message = message
    
    def to_xml(self):
        root_container = ElementTree.Element('MTConnectError')
        root_container.append(self.agent.get_header())
        
        error_container = ElementTree.SubElement(root_container, 'Errors')
        error = ElementTree.SubElement(error_container,'Error')
        error.set('errorCode',self.name)
        error.text = self.message

        return ElementTree.tostring(root_container).decode()
        
class MTInvalidRequest(MTError):
    name = 'MTInvalidRequest'

class MTInvalidRange(MTError):
    name = 'MTInvalidRange'
