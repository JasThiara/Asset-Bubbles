'''
Created on Nov 7, 2013

@author: clinton
'''
import unittest
from FlorenZmirou import FlorenZmirou

class Test(unittest.TestCase):
    L = ['GRPN',1,60,False,'goog inc']
    FZ = FlorenZmirou(tickerParams=L)
    X = [0.0   , 1.0 ,   2.0   , 3.0    ,4.0  ,  5.0  ,  6.0  ,  7.0 ,   8.0 ,   9.0]
    Y = [0.0 ,   1.0   , 4.0   , 9.0   , 16.0    ,25.0    ,36.0,    49.0  ,  64.0 ,   81.0]
    
    def testInterpolationBubbleTest(self):
        self.FZ.StockPrices = self.X
        self.FZ.EstimateVariance = self.Y
        G = self.FZ.InterpolationBubbleTest(self.Y, self.X)
        K = 9.0
        self.assertEqual(G, K, 'bad result')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()