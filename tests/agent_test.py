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
        self.test_agent = MTConnect(loc='tests/test_device.xml') 
 

    def testProbe(self):
        self.test_agent.probe()
    
    def testCurrent(self):
        self.test_agent.current()
    
    def testSample(self):
        self.test_agent.sample()

if __name__ == '__main__':
    unittest.main()
