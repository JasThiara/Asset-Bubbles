'''
Created on Jan 6, 2014

@author: Jas
'''
from sage.all import *
import unittest
from Approximation import *

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testRKHSN1(self):
        tau = 1
        b = pi
        a = 0
        X = 3*pi/4
        x = pi/4
        Expected = (tau * cosh(tau * (b-X)) * cosh(tau * (x-a)) )/sinh(tau * (b-a))
        Actual = RKHSN1(a,b,X,x,tau)
        self.assertEqual(Expected,Actual)
    
    def testBB(self):
        a1 = 1
        a2 = 2
        b1 = 1
        b2 = 2
        z = 1/sqrt(2)
        Expect= exp(1)*cos(1/2)+exp(1)*sin(1/2)
        Actual = bb(a1,a2,b1,b2,z)
        self.assertEqual(Expect,Actual)
        
    def test

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()