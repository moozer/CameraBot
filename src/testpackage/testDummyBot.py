'''
Created on 8 Dec 2012

@author: moz
'''
import unittest
from DummyBot.DummyBot import DummyBot

Direction_NE = [1, 1]
Direction_SW = [-1, -1]
Direction_Neutral = [0,0]

JustAnInteger = 0
def fctAddOne():
    global JustAnInteger 
    JustAnInteger += 1
    
class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testDummy(self):
        Bot = DummyBot()
        Bot.SetDirection( Direction_NE )
        self.assertEqual( Bot.direction, Direction_NE )
        pass
    
    def testImage(self):
        Bot = DummyBot()
        OldImg = Bot.image
        Bot.SetDirection( Direction_NE )
        self.assertNotEquals(OldImg, Bot.image )

    def testAcqFlag(self):
        Bot = DummyBot()
        
        Bot.EnableAcquisition( fctAddOne )

        OldInt = JustAnInteger
        Bot.SetDirection( Direction_NE )
        self.assertEqual(OldInt+1, JustAnInteger)
        
        Bot.DisableAcquisition()
        OldInt = JustAnInteger
        Bot.SetDirection( Direction_Neutral )
        self.assertEqual(OldInt, JustAnInteger) # fct not called..
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDummy']
    unittest.main()