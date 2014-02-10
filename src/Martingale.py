'''
Created on Feb 9, 2014

@author: Jas
'''
from sage.all import *
from FlorenZmirou import FlorenZmirou
from CrossValidation import CrossValidation, RKHSN1
class MartingaleTesting:
    '''
    For asset bubble detection, one needs to test if for martingale/supermartingale conditions
    '''

    def __init__(self, ticker,historicalTimeRange):
        '''
        Constructor
        Input:
        ticker                 : a ticker symbol, e.g. 'GOOG'
        historicalTimeRange    : a period of data request from, e.g. 10    
        '''
        tickerPs = [ticker,historicalTimeRange,60]
        FZ = FlorenZmirou(tickerParams=tickerPs)
        CV = CrossValidation(FZ)
        self.c = CV.c
        self.tauN1 = CV.tau
        self.a = CV.a
        self.b = CV.b
        self.gridPoints = CV.gridPoints
        self.rkhsN1Variance = lambda x: (1/self.c.dot_product(vector([RKHSN1(self.a,self.b,x,y,self.tau) for y in self.gridPoints])))**2
        
        
        
        
        