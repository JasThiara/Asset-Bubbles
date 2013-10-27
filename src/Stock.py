'''
Created on Oct 27, 2013

@author: Jas
'''

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
       Discription: it will give us list of stock prices from csv file.
        '''
      self.StockPrices=self.GetStockPrices(FileName)
      
  def GetStockPrices(self,FileName): 
      '''
      Input: FileName
      Discription: Getting stock prices for that FileName
      Output: list of Stock prices
      ''' 