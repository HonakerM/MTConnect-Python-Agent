#import user test
import unittest

#import storage objects
from mtconnect.storage import MTBuffer, MTDataEntity

#import libraries for testing
import os
import datetime



class DataEntity(unittest.TestCase):

    def testDataCreation(self):
        entity = MTDataEntity('test',1)

        self.assertTrue(isinstance(entity.timestamp, type(datetime.datetime.now())))
        self.assertEqual(entity.MTC_dataid,'test')
        self.assertEqual(entity.value,1)

    def testSequenceNumber(self):
        entity = MTDataEntity('test',1)
        entity.set_sequence(1)
        self.assertEqual(entity.sequence_number,1)

class BufferTest(unittest.TestCase):

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
        buffer = MTBuffer(buffer_length=2)

        data_1 = MTDataEntity('cat_1',1)
        data_2 = MTDataEntity('cat_1',2)
        data_3 = MTDataEntity('cat_2',1)

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
        
        self.assertEqual(buffer.last_value, {'cat_1':2,'cat_2':1})

    def testBufferGet(self):
        buffer = MTBuffer(buffer_length=2)
        data_1 = MTDataEntity('cat_1',1)
        data_2 = MTDataEntity('cat_1',2)
        buffer.push(data_1)
        buffer.push(data_2)


        self.assertEqual(buffer.get_data(1,1), ([data_1],2))
        self.assertEqual(buffer.get_data(1,2), ([data_1,data_2],3))
        self.assertEqual(buffer.get_data(1,3), ([data_1,data_2],3))
        



if __name__ == '__main__':
    unittest.main()