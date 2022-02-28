#import user test
import unittest

#import storage objects
from mtconnect.agent import MTConnect

#import libraries for testing
import os
import datetime



class AgentTest(unittest.TestCase):
    test_agent = None

    def __init__(self, *args, **kwargs):
        super(AgentTest, self).__init__(*args, **kwargs)
        self.test_agent = MTConnect(loc='test_device.xml')
 

    def testProbe(self):
        self.test_agent.probe()
    
    def testCurrent(self):
        self.test_agent.current()
    
    def testSample(self):
        self.test_agent.sample()
    
    def testSetDeviceVariables(self):
        device = self.test_agent.get_device()
        #test update
        self.test_agent.set_device_name(device,'test_name')
        new_name = device.xml_data.get('name')
        self.assertEqual(new_name,'test_name')
        
        self.test_agent.set_device_id(device,2)
        new_id = device.xml_data.get('id')
        self.assertEqual(new_id,2)

if __name__ == '__main__':
    unittest.main()
