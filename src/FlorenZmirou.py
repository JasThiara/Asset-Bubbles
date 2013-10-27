'''
Created on Oct 27, 2013

@author: Jas
'''
from sage.all import *
class FlorenZmirou(object):
    '''
    FlorenZmirou will provide us list of sigma values and interpolation from list of stock prices
    '''
    
    
    def __init__(self,stock):
        '''
        Input: Stock
        Discription: Step1: From stock, it will give us sigma(x)
                     Step2: Interpolate sigma(x) using step1.
        '''
        self.Stock = stock
        self.GridPoints = self.GetGridPoints()
        self.EstimatedSigma = [self.Volatility_estimation(self.T,self.Stock.StockPrices,ex,self.n,self.h_n) for ex in self.GridPoints]# these are the sigma values evulated at the grid points
        self.CubicInterpolatedSigma = self.GetCubicInterpolatedSigma()
    def GetCubicInterpolatedSigma(self):
        '''
        Description: It will give us cubic spline interpolation of sigma of grid points.
        Output: Given a list of grid points and estimated sigma, spline(Points) is an object such that spline(Points) is the value of the spline interpolation through the points in grid points and estimated sigma
        '''
        N = len(self.GridPoints)
        Points = []
        for i in range(N):
            x = self.GridPoints[i]
            y = self.EstimatedSigma[i]
            Points.append((x,y))
        return spline(Points)

    def GetGridPoints(self):
        '''
        Description: It will make grid Points
        Output: Returns list of grid points
        '''
        self.n = len(self.Stock.StockPrices)
        self.h_n= self.Derive_hn(self.Stock.StockPrices)
        self.T = 60*n # 60 sec times total number of data points because T is every minute from [0,T]
        self.x = self.Derive_x_values(self.Stock.StockPrices)
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
        h_n = self.Derive_hn(self,S)
        doubleh_n = 2*h_n
        Difference= max(S)-min(S)
        x_hn =Difference*doubleh_n
        return x_hn
    
    def Derive_x_values(self,S):
        """
     
        input:
               stock price (s(t1).......s(tn))= S
        outout x values
        Description: Derive x grid points
        """
        x_hn = self.x_step_size(self,S)
        halfh_n = x_hn/2.0
        x = list()
        x.append(min(S)+halfh_n)
        ex = x[0]
        Smax = max(S)
        while ex <Smax:
            ex = ex+x_hn
            x.append(ex)
        return x
        
        
        
