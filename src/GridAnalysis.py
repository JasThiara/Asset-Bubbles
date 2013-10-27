'''
Created on Oct 27, 2013

@author: Jas
'''

class GridAnalysis(object):
    '''
    Description: need to create method that determines what grid points are usable for interpolation and extrapolation 
    '''
    def GetGridPoints(self):
        '''
        Description: It will make grid Points
        Output: Returns list of grid points
        '''
        self.n = len(self.Stock.StockPrices)
        self.h_n= self.Derive_hn(self.Stock.StockPrices)
        self.T = 60*self.n # 60 sec times total number of data points because T is every minute from [0,T]
        self.x = self.Derive_x_values(self.Stock.StockPrices)

    def __init__(self,stock):
        '''
        Constructor
        '''
        self.Stock = stock
        self.GridPoints = self.GetGridPoints()
        self.UsableGridPoints= self.DoGridAnalysis()
        
    def DoGridAnalysis(self):
    
        