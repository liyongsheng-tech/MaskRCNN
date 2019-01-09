import unittest
from CocoDataloader import CocoLoader

class TestCocoDataloader(unittest.TestCase):

    def testDefaults(self):
        cocoLoader = CocoLoader()
        self.assertEqual(cocoLoader.dataDir, CocoLoader.DEFAULT_DIR)
        self.assertEqual(cocoLoader.dataType, CocoLoader.DEFAULT_TYPE)
    
    def testAssignment(self):
        dataDir = '../DS_coco'
        dataType = 'train2017'
        cocoLoader = CocoLoader(dataDir=dataDir, dataType=dataType)