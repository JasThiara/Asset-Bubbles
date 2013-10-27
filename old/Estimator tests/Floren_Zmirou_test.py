'''
Created on Apr 28, 2013

@author: Jas
'''
import unittest
from Sublocaltime import *
from math import fabs

class Test(unittest.TestCase):
    
    def setUp(self):
        self.n = 64
        self.hn = .25
        self.T = 64
        self.t = [i for i in range(1,65)]
        self.St = [0.623758588,0.667911451,0.677626587,0.690298464,
              0.70715594,0.73289075,0.766368958,0.786943206,
              0.88235025,0.924148129,0.938592027,1.068499619,
              1.087613376,1.090838708,1.416967477,1.508789038,
              1.601298349,1.758895375,1.762924681,1.874978702,
              1.887109144,1.923991643,1.954737435,1.988704942,
              2.034263798,2.111813272,2.116884649,2.118240098,
              2.145604367,2.257327346,2.27399522,2.329484913,
              2.334018746,2.356909098,2.404342694,2.407755122,
              2.426927494,2.564755415,2.576940277,2.636581837,
              2.667473868,2.675129559,2.744319836,2.766852948,
              3.013636155,3.140587018,3.246664493,3.376726713,
              3.5189456,3.556725212,3.581998844,3.832316687,
              3.977027894,4.049440629,4.082732624,4.367164847,
              4.607095249,4.724328187,4.724915233,4.812205825,
              4.83096962,4.840526121,5.134469458,5.338781837]
        self.x = [0.956,1.629,2.302,2.975,3.647,4.32]
        
    def tearDown(self):
        pass
    
    def test_indicator1(self):
        actual = Indicator_function(1<2)
        expected = 1
        msg = "Indicator function failed"
        self.assertEqual(actual, expected, msg)
        
    def test_indicator2(self):
        actual = Indicator_function(1>2)
        expected = 0
        msg = "Indicator function failed"
        self.assertEqual(actual, expected, msg)
        
    def test_Sublocal1(self):
        actual = Sublocal_Time(self.T,self.St,self.x[0],self.n, self.hn)
        expected = 20
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
    
    def test_Sublocal2(self):
        actual = Sublocal_Time(self.T,self.St,self.x[1],self.n, self.hn)
        expected = 12
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
        
    def test_Sublocal3(self):
        actual = Sublocal_Time(self.T,self.St,self.x[2],self.n, self.hn)
        expected = 24
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
    
    def test_Sublocal4(self):
        actual = Sublocal_Time(self.T,self.St,self.x[3],self.n, self.hn)
        expected = 8
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
        
    def test_Sublocal5(self):
        actual = Sublocal_Time(self.T,self.St,self.x[4],self.n, self.hn)
        expected = 8
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
        
    def test_Sublocal6(self):
        actual = Sublocal_Time(self.T,self.St,self.x[5],self.n, self.hn)
        expected = 4
        msg = "Sublocal function failed: (actual, expected) = (%d,%d)"%(actual,expected)
        self.assertEqual(actual,expected, msg)
    
    def test_LocalTime1(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[0],self.n, self.hn)
        expected = 17.52016107
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_LocalTime2(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[1],self.n, self.hn)
        expected = 6.981821548
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_LocalTime3(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[2],self.n, self.hn)
        expected = 4.964548815
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_LocalTime4(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[3],self.n, self.hn)
        expected = 11.36366652
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_LocalTime5(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[4],self.n, self.hn)
        expected = 10.96530067
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
        
    def test_LocalTime5(self):
        #Local_time(T,S,x,n,h_n):
        actual = Local_time(self.T,self.St,self.x[5],self.n, self.hn)
        expected = 17.72394077
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_Volatility1(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[0],self.n, self.hn)
        expected = 0.876008054
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
        
    def test_Volatility2(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[1],self.n, self.hn)
        expected = 0.581818462
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_Volatility3(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[2],self.n, self.hn)
        expected = 0.206856201
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_Volatility4(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[3],self.n, self.hn)
        expected = 1.420458315
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_Volatility5(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[4],self.n, self.hn)
        expected = 1.370662584
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
    
    def test_Volatility6(self):
        #Volatility_estimation(T,S,x,n,h_n):
        actual = Volatility_estimation(self.T,self.St,self.x[5],self.n, self.hn)
        expected = 4.430985193
        eps = 0.00001
        difference = fabs(actual-expected)
        Indication = Indicator_function(difference<eps)
        ExpectedIndication = 1
        msg = "Local function failed: (actual, expected) = (%f,%f)"%(actual,expected)
        self.assertEqual(Indication,ExpectedIndication, msg)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()