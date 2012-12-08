'''
Created on 8 Dec 2012

@author: moz
'''
import unittest
from DummyBot.DummyBot import DummyBot

Direction_NE = [1, 1]
Direction_SW = [-1, -1]
Direction_Neutral = [0,0]

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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDummy']
    unittest.main()