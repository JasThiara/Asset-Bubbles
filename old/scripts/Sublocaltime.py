'''
Created on Mar 31, 2013

@author: Jas
'''


def Sublocal_Time(T,S,x,n,h_n):
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
        indicatorValue = Indicator_function(absoluteValue<h_n)
        sum = sum+indicatorValue
    return scalar*sum
      
        
def Local_time(T,S,x,n,h_n):
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
        indicatorValue = Indicator_function(absoluteValue<h_n)
        sum = sum+indicatorValue*n*Difference
    return scalar*sum

def Volatility_estimation(T,S,x,n,h_n):
    """
    funtion: Volatility_estimator
    input:
          1) stock price (s(t1).......s(tn))= S
          2) x values in [0,infinity)
          3) n , h_n
    outout l_T^n(x) = (l_T^n(x)*S_n(x))/(sigma i =1,n-1 1_{|s_t(i)-x)| < h_n})
    
    Description: S_n(x) = (l_T^n(x))/(sigma i =1,n-1 1_{|s_t(i)-x)| < h_n})
    """
    return Local_time(T,S,x,n,h_n)/Sublocal_Time(T,S,x,n,h_n)

def Indicator_function(condition):
    """
    function Indicator_function
    input:
         condition
    output:
          0 or 1
          
    Description : (sigma i =1,n-1 1_{|S(s)-x)| < h_n})
    """
    return condition

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
               2) for each usable grid point, the list of usable grid points
        n=len(S)
       '''
           
            for i in range len(S):
                Sti = S[i]
                for j in range of len(x):
                    xj = x[m]
                    if abs(S[i]-x[m]<h_n):
                        S[i].append(x[m])
            for xj =x[m]:
                if S[i].append(x[m])>1%*len(x)
                    

def Derive_hn(S):
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
def x_step_size(S):
    """
    Derive x values function
    input:
           stock price (s(t1).......s(tn))= S
    outout x grid points
    Description: trying to create step size to generate x
    """
    h_n = Derive_hn(S)
    doubleh_n = 2*h_n
    Difference= max(S)-min(S)
    x_hn =Difference*doubleh_n
    return x_hn

def Derive_x_values(S):
    """
 
    input:
           stock price (s(t1).......s(tn))= S
    outout x values
    Description: Derive x grid points
    """
    x_hn = x_step_size(S)
    halfh_n = x_hn/2.0
    x = list()
    x.append(min(S)+halfh_n)
    ex = x[0]
    Smax = max(S)
    while ex <Smax:
        ex = ex+x_hn
        x.append(ex)
    return x
    

    