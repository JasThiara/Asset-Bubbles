'''
Created on Nov 21, 2013

@author: Jas
'''
from sage.all import *
from AssetBubble import AssetBubble
class AssetBubbleDetection(object):
    '''
    This class performs asset bubble detection over a variety of asset bubble objects
    Bubble Detection Strategy
    
    
    2) Suppose we know alpha = (1+m)/2, and have a floren zmirou object, FZ:
    assetBubbleList = list()
    for m = 1,...,9
        for n = 1,2,3
            assetBubbleList.append(AssetBubble(FZ,m,n))
    3) From the assetBubbleList, find the best assetBubble with the closest extrapolated approximation
    i.e.find f_alpha such that  min_{m,n in Integers} |f'(maxPrice ) - f_alpha ' (maxPrice)|
    4) Determine if f_alpha from (3) goes to infinity using proposition 3, if not infinity declare not asset bubble
    5) if determined matingale,  do Step D
    6) declare yes/no on asset bubble.
    '''
    @staticmethod
    def SortingFunction(AB):
        interpolatedDerivative = AB.FlorenZmirou.CubicInterpolatedSigma.derivative(AB.FlorenZmirou.Stock.maxPrice)
        extrapolatedDerivative = AB.fExtrapolatedSpline.derivative(AB.FlorenZmirou.Stock.maxPrice)
        return abs( interpolatedDerivative - extrapolatedDerivative )
        

    def __init__(self,FZ):
        '''
        Constructor
        Inputs:
        1) FZ - Floren Zmirou Object
        Description:
        1) Builds the assetBubbleList [AB1, AB2,...., AB(mMax*nMax)] as in the description
        2) Needs to sort assetBubbleList by abs( ABi.FlorenZmirou.CubicInterpolatedSigma.derivative(ABi.FlorenZmirou.Stock.maxPrice) - (ABi.fExtrapolatedSpline.derivative(ABi.FlorenZmirou.Stock.maxPrice))
        2.1) (2) is finding the best extrapolation function in assetBubbleList that has the closest derivate to the interpolated function
        '''
        self.assetBubbleList = list()
        self.mMax = 10
        self.nMax = 4
        for m in range(1,self.mMax):
            for n in range(1,self.nMax):
                self.assetBubbleList.append(AssetBubble(FZ,m,n))
        sorted(self.assetBubbleList,key=lambda AB: abs())                
        