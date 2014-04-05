'''
Created on Feb 9, 2014

@author: Jas
'''
from sage.all import *
from FlorenZmirou import FlorenZmirou
from CrossValidation import CrossValidationRKHSN1, RKHSN1
class MartingaleTesting:
    '''
    For asset bubble detection, one needs to test if for martingale/supermartingale conditions
    '''

    def __init__(self, En):
        '''
        Constructor
        Input:
        ticker                 : a ticker symbol, e.g. 'GOOG'
        historicalTimeRange    : a period of data request from, e.g. 10   
        En                     : Euler Maruyama samples
        '''
        #tickerPs = [ticker,historicalTimeRange,60]
        FZ = FlorenZmirou(en=En)
        CV = CrossValidationRKHSN1(FZ)
        self.c = CV.c
        self.tauN1 = CV.tau
        self.a = CV.a
        self.b = CV.b
        self.gridPoints = CV.gridPoints
        #self.fb = lambda x: self.c.dot_product(vector([RKHSN1(self.a,self.b,x,y,self.tau) for y in self.gridPoints]))
        self.rkhsN1Variance = lambda x: (1/self.c.dot_product(vector([RKHSN1(self.a,self.b,x,y,self.tauN1) for y in self.gridPoints])))**2
        stockPricePlot = points(zip(range(len(FZ.StockPrices)),FZ.StockPrices), color='green')
        rkhsN1Plot = points(zip(FZ.StockPrices,[self.rkhsN1Variance(x) for x in FZ.StockPrices]),color='blue')
        estimatedVariancePlot = points(zip(FZ.StockPrices,FZ.EstimatedVariance),color='red')
        (rkhsN1Plot + estimatedVariancePlot).save('RKHSn1Test.png')
        stockPricePlot.save('stockPriceTest.png')
        
        
if __name__ == '__main__':
    MartingaleTesting(11)