'''
Created on Feb 8, 2014

@author: Jas
'''
import unittest
from sage.all import *
from Spline import NaturalCubicSpline
class Test(unittest.TestCase):


    def testNaturalCubicSpline(self):
        data = [(0,1),(1,exp(1)), (2,exp(2)),(3,exp(3))]
        S = NaturalCubicSpline(data)
        PolyPlot = S.plot()
        #var('x')
        #ActualPlot = plot(exp(x),(0,3),color='red')
        combinedPlot = PolyPlot
        combinedPlot.save('testNaturalCubicSpline.png')
        self.assertEqual(1,1)     


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testNaturalCubicSpline']
    unittest.main()