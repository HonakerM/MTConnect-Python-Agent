#import user test
import unittest

#import storage objects
from mtconnect.storage import MTBuffer, MTDataEntity
from mtconnect.device import MTDataItem, MTDevice

#import libraries for testing
import os
import datetime



class DataEntity(unittest.TestCase):
    test_device = None
    test_item_1 =  None

    def __init__(self, *args, **kwargs):
        super(DataEntity, self).__init__(*args, **kwargs)

        self.test_device = MTDevice('test_device','1',None)
        self.test_item_1 = MTDataItem('test_1','test_1','SYSTEM','SAMPLE',self.test_device,self.test_device)
    
    def testDataCreation(self):
        entity = MTDataEntity(self.test_item_1,1)

        self.assertTrue(isinstance(entity.timestamp, type(datetime.datetime.now())))
        self.assertEqual(entity.dataItem.id,'test_1')
        self.assertEqual(entity.value,1)

    def testSequenceNumber(self):
        entity = MTDataEntity(self.test_item_1,1)
        entity.set_sequence(1)
        self.assertEqual(entity.sequence_number,1)

class BufferTest(unittest.TestCase):
    test_device = None
    test_item_1 = None
    test_item_2 = None
    
    test_buffer = None

    def __init__(self, *args, **kwargs):
        super(BufferTest, self).__init__(*args, **kwargs)

        self.test_device = MTDevice('test_device','1',None)
        self.test_item_1 = MTDataItem('test_1','test_1','SYSTEM','SAMPLE',self.test_device,self.test_device)
        self.test_item_2 = MTDataItem('test_2','test_2','SYSTEM','SAMPLE',self.test_device,self.test_device)
        
        self.test_buffer = MTBuffer(buffer_length=2)

    def testBufferCreation(self):
        buffer = MTBuffer()
        self.assertEqual(len(buffer.get_buffer()),16384)
        os.environ['BUFFER_SIZE']='10'
        buffer = MTBuffer()
        self.assertEqual(len(buffer.get_buffer()),10)
        buffer = MTBuffer(buffer_length=2)
        self.assertEqual(len(buffer.get_buffer()),2)

    def testBufferPush(self):
        #initalize buffer
        buffer = self.test_buffer

        data_1 = MTDataEntity(self.test_item_1,1)
        data_2 = MTDataEntity(self.test_item_1,2)
        data_3 = MTDataEntity(self.test_item_2,1)

        buffer.push(data_1)
        self.assertEqual(data_1.sequence_number, 1)
        self.assertEqual(buffer.get_buffer(),[data_1,None])
        self.assertEqual(buffer.first_sequence,1)

        buffer.push(data_2)
        self.assertEqual(data_2.sequence_number, 2)
        self.assertEqual(buffer.get_buffer(),[data_1,data_2])
        self.assertEqual(buffer.last_sequence,2)
        self.assertEqual(buffer.first_sequence,1)

        buffer.push(data_3)
        self.assertEqual(data_3.sequence_number, 3)
        self.assertEqual(buffer.get_buffer(),[data_2,data_3])
        self.assertEqual(buffer.last_sequence,3)
        self.assertEqual(buffer.first_sequence,2)
        
    def testBufferGet(self):
        buffer = self.test_buffer

        test_device = MTDevice('test_device','1','1',None)
        test_item = MTDataItem('test_1','test_1','SYSTEM','SAMPLE',test_device,test_device)
        data_1 = MTDataEntity(test_item,1)
        data_2 = MTDataEntity(test_item,2)
        buffer.push(data_1)
        buffer.push(data_2)


        self.assertEqual(buffer.get_data(1,1), ([data_1],2))
        self.assertEqual(buffer.get_data(1,2), ([data_1,data_2],3))
        self.assertEqual(buffer.get_data(1,3), ([data_1,data_2],3))
        



if __name__ == '__main__':
    unittest.main()
