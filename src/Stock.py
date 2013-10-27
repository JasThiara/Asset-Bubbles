'''
Created on Oct 27, 2013

@author: Jas
'''
import csv
class Stock(object):
    '''
    Stock class will read a csv file provide a list of stock prices 
    '''
    
    def IsNumber(self,rowValue):
        ''' Please use/call this method in your script below to determine if row[1] is a numerical string or not.'''
        try:
            float(rowValue)
            return True
        except ValueError:
            return False
        
    def __init__(self,FileName):
        '''
        Input: FileName
        Description: it will give us list of stock prices from csv file.
        ''' 
        self.StockPrices=self.GetStockPrices(FileName)
        
    def GetStockPrices(self,FileName): 
        '''
        Input: FileName
        Description: Getting stock prices for that FileName
        Output: list of Stock prices
        ''' 
        cr = csv.reader(open(FileName,"r U"))
        next(cr, None) # skip the header
        c1 = []
        for row in cr: # reading file from csv file    
            if self.IsNumber(row[1]):#if the string, row[1], is a numerical string 
                c1.append(float(row[1]))#add it into the list
        return c1