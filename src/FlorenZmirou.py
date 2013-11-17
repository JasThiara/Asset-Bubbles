'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
import locale
import sys
locale.setlocale(locale.LC_NUMERIC, "")
class FlorenZmirou(object):
    '''
    FlorenZmirou will provide us list of sigma values and interpolation from list of stock prices
    '''
    def GetGridPoints(self):
        '''
        Description: It will make grid Points
        Output: Returns list of grid points
        '''
        self.n = len(self.Stock.StockPrices)
        self.h_n= self.Derive_hn(self.Stock.StockPrices)
        self.T = 60*self.n # 60 sec times total number of data points because T is every minute from [0,T]
        return self.Derive_x_values(self.Stock.StockPrices)
    
    
    def __init__(self,stock):
        '''
        Input: Stock
        Discription: Step1: From stock, it will give us sigma(x)
                     Step2: Interpolate sigma(x) using step1.
        '''
        self.Stock = stock
        self.GridPoints = self.GetGridPoints()
        self.UsableGridPoints, self.StockPricesByGridPointDictionary = self.DoGridAnalysis(self.T,self.Stock.StockPrices,self.GridPoints,self.n,self.h_n,.05)
        self.EstimatedSigma = [self.Volatility_estimation(self.T,self.Stock.StockPrices,ex,self.n,self.h_n) for ex in self.UsableGridPoints]# these are the sigma values evulated at the grid points
        self.EstimatedVariance = [i*i for i in self.EstimatedSigma]
        self.InverseVariance = [1.0/i for i in self.EstimatedVariance]
        self.CubicInterpolatedSigma = self.GetCubicInterpolatedSigma()
        
    def GetCubicInterpolatedSigma(self):
        '''
        Description: It will give us cubic spline interpolation of sigma of grid points.
        Output: Given a list of grid points and estimated sigma, spline(Points) is an object such that spline(Points) is the value of the spline interpolation through the points in grid points and estimated sigma
        '''
        N = len(self.UsableGridPoints)
        Points = []
        for i in range(N):
            x = self.UsableGridPoints[i]
            y = self.EstimatedSigma[i]
            Points.append((x,y))
        return spline(Points)

   
    def Sublocal_Time(self,T,S,x,n,h_n):
        """
        funtion: Sublocal_time
        input:T is time period 
              1) stock price (s(t1).......s(tn))= S
              2) x values in [0,infinity)
              3) n , h_n
        outout L_T^n(x)
        
        Description: L_T^n(x) = (T/ 2nh_n) sigma i =1,n 1_{|s_t(i)-x)| < h_n}
    
        """
        sum = 0.0
        scalar = T/(2.0*n*h_n)
        for i in range(len(S)):
            Sti = S[i]
            absoluteValue = abs(Sti-x)
            indicatorValue = self.Indicator_function(absoluteValue<h_n)
            sum = sum+indicatorValue
        return scalar*sum
          
            
    def Local_time(self,T,S,x,n,h_n):
        """
        funtion: Local_time
        input:
              1) stock price (s(t1).......s(tn))= S
              2) x values in [0,infinity)
              3) n , h_n
        outout l_T^n(x) = l_T^n(x)*S_n(x)
        
        Description: l_T^n(x) = (T/ 2nh_n) sigma i =1,n-1 1_{|s_t(i)-x)| < h_n}*n(s(t(i+1))-s(t(i))^2
        """
        sum = 0.0
        scalar = T/(2.0*n*h_n)
        for i in range(len(S)-1):
            Sti = S[i]
            Stj = S[i+1]
            absoluteValue = abs(Sti-x)
            Difference = (Stj-Sti)**2
            indicatorValue = self.Indicator_function(absoluteValue<h_n)
            sum = sum+indicatorValue*n*Difference
        return scalar*sum
    
    def Volatility_estimation(self,T,S,x,n,h_n):
        """
        funtion: Volatility_estimator
        input:
              1) stock price (s(t1).......s(tn))= S
              2) x values in [0,infinity)
              3) n , h_n
        outout l_T^n(x) = (l_T^n(x)*S_n(x))/(sigma i =1,n-1 1_{|s_t(i)-x)| < h_n})
        
        Description: S_n(x) = (l_T^n(x))/(sigma i =1,n-1 1_{|s_t(i)-x)| < h_n})
        """
        return self.Local_time(T,S,x,n,h_n)/self.Sublocal_Time(T,S,x,n,h_n)
    
    def Indicator_function(self,condition):
        """
        function Indicator_function
        input:
             condition
        output:
              0 or 1
              
        Description : (sigma i =1,n-1 1_{|S(s)-x)| < h_n})
        """
        return condition
    def Derive_hn(self,S):
        """
        Derive h_n function
        input:
               stock price (s(t1).......s(tn))= S
        outout h_n
        
        Description: 1/n^(1/3)
        """
        n = len(S)
        h_n = 1/n**(1.0/3.0)
        return h_n
    def x_step_size(self,S):
        """
        Derive x values function
        input:
               stock price (s(t1).......s(tn))= S
        outout x grid points
        Description: trying to create step size to generate x
        """
        h_n = self.Derive_hn(S)
        doubleh_n = 2*h_n
        Difference= max(S)-min(S)
        x_hn =Difference*doubleh_n
        return x_hn
    
    def Derive_x_values(self,S):
        """
     
        input:
               stock price (string as file location pythons(t1).......s(tn))= S
        outout x values
        Description: Derive x grid points
        """
        x_hn = self.x_step_size(S)
        halfh_n = x_hn/2.0
        x = list()
        x.append(min(S)+halfh_n)
        ex = x[0]
        Smax = max(S)
        while ex <Smax:
            ex = ex+x_hn
            x.append(ex)
        return x
        
    def DoGridAnalysis(self,T,S,x,n,h_n,Y):
        '''
        Input:1) T = Time from[0,T] which is for a day each mintue (60*n)
             2) S = Stock prices
             3) x = Grid Points
             4) h_n = 1/n^(1/3)
             5) n = Number of stock data points
             6) Y =  Y percent of total data points
        Ingredients: 1) S_(ti), 
                     2) indicator function, 
                     3) grid points, 
                     4) a dictionary where the keys are the grid points and the value is a list for each grid point (used in Step 2)
        Description : sigma i =1,n-1 1_{|s_t(i)-x)| < h_n} = *
        Recipe:           step1: 
                              for Si in S1,S2....Sn:
                                   for x in X1,X2...Xm:
                                      if |Si-x|<h_n:
                                        step 2: 
                                        Add Si into list corresponding to x
                               Step 3:
                               for x in X1, X2,...,Xm: 
                                    if the list of data points corresponding to x has greater than Y% of total grid points n:
                                         add it to the list of usable grid points
                               Step 4:
                               return the outputs
        Output: 1) the list of usable grid points
                   2) for each usable grid point, the list of stockprices
            n=len(S)
        '''
        usableGridPoints = x
        d = dict()# Creating empty dictionary
        stockPriceCount = float(len(S)) 
        for gridPoint in x:# The grid points are your keys
            d[gridPoint]=list()#a dictionary where the keys are the grid points and the value is a list for each grid point (used in Step 2)
            for stockPrice in S:# stock price in S    
                if  abs(gridPoint-stockPrice)<h_n:# satisfying the condition if true then add x value to corresponding Si
                    d[gridPoint].append(stockPrice)#Note the number of points for the gridPoint is len(d[gridPoint])
        for gridPoint in x:
            listOfPointsForGridPoint = d[gridPoint]
            numberOfPointsInList = float(len(listOfPointsForGridPoint))
            percentOfStockPrices = numberOfPointsInList / stockPriceCount
            if  percentOfStockPrices < Y:# We just want to remove the number grid points from the dictionary since we have all data.
                usableGridPoints.remove(gridPoint)
                del d[gridPoint]#pop(key[, default]) If key is in the dictionary, remove it and return its value, else return default. If default is not given and key is not in the dictionary, a KeyError is raised.
        return usableGridPoints, d# 1) the list of usable grid points 2) for each usable grid point, the list of usable grid points
    
    def format_num(self,num):
        """
        Format a number according to given places.
        Adds commas, etc. Will truncate floats into ints!
        """
        try:
            inum = int(num)
            return locale.format("%.*f", (0, inum), True)
    
        except (ValueError, TypeError):
            return str(num)
        
    def get_max_width(self,table, index):
        """Get the maximum width of the given column index"""
        return max([len(self.format_num(row[index])) for row in table])
    
    def pprint_table(self,out, table):
        """Prints out a table of data, padded for alignment
        @param out: Output stream (file-like object)
        @param table: The table to print. A list of lists.
        Each row must have the same number of columns. 
        """
        col_paddings = []
        for i in range(len(table[0])):
            col_paddings.append(self.get_max_width(table, i))
        for row in table:
            # left col
            print >> out, row[0].ljust(col_paddings[0] + 1),
            # rest of the cols
            for i in range(1, len(row)):
                col = self.format_num(row[i]).rjust(col_paddings[i] + 2)
                print >> out, col,
            print >> out
            
    def CreateZmirouTable(self):
        '''
        #1.3) create table with the following:
        #1.3.1) Usable Grid Points
        #1.3.2) Estimated Sigma value from Floren Zmirou Estimator
        #1.3.3) Number of Points for each Grid Point
        '''
        table= []
        columnNames = ["Usable Grid Points", "Estimated Sigma Zmirou", "Number of Points"]
        table.append(columnNames)
        gridPoints = self.UsableGridPoints
        estimatedSigma = self.EstimatedSigma
        for i in range(len(gridPoints)):
            table.append([str(gridPoints[i]), str(estimatedSigma[i]), str(len(self.StockPricesByGridPointDictionary[gridPoints[i]]))])
        out = sys.stdout
        return self.pprint_table(out, table)