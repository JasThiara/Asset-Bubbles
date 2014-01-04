'''
Created on Nov 21, 2013

@author: Jas
'''
from sage.all import *
from AssetBubble import AssetBubble
def frange(x, y, jump):
    l = list()
    while x < y:
        l.append(x)
        x += jump
    return l
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
        '''
        method for sorting asset bubbles
        '''
        interpolatedDerivative = AB.FlorenZmirou.CubicInterpolatedSigma.derivative(AB.FlorenZmirou.Stock.maxPrice)
        extrapolatedDerivative = AB.fExtrapolatedSpline.derivative(AB.FlorenZmirou.Stock.maxPrice)
        return abs( interpolatedDerivative - extrapolatedDerivative )
        
    def DetermineAssetBubble(self):
        '''
        check if assetbubblemodel.m is greater than 1
        '''
        return (self.AssetBubbleModel.m > 1)
        

    def __init__(self,FZ):
        '''
        Constructor
        Inputs:
        1) FZ - Floren Zmirou Object
        Description:
        1) Builds the assetBubbleList [AB1, AB2,...., AB(mMax*nMax)] as in the description
        2) Needs to sort assetBubbleList by abs( ABi.FlorenZmirou.CubicInterpolatedSigma.derivative(ABi.FlorenZmirou.Stock.maxPrice) - (ABi.fExtrapolatedSpline.derivative(ABi.FlorenZmirou.Stock.maxPrice))
        2.1) (2) is finding the best extrapolation function in assetBubbleList that has the closest derivative to the interpolated function
        3) Builds plot of interpolated function and the best extrapolated function
        4) determines the asset bubble
        '''
        self.assetBubbleList = list()
        self.mMax = 10
        self.nMax = 4
        mSet1 = set(range(1,self.mMax))
        mSet2 = set(frange(0.5,1,.05))
        self.mList = mSet1.union(mSet2)
        for m in self.mList:
            self.assetBubbleList.append(AssetBubble(FZ,m,1))
        self.assetBubbleList = sorted(self.assetBubbleList,key=lambda AB: AssetBubbleDetection.SortingFunction(AB))
        self.AssetBubbleModel = self.assetBubbleList[0]
        self.interpolatedFunction = self.AssetBubbleModel.FlorenZmirou.CubicInterpolatedSigma     
        self.extrapolatedFunction = self.AssetBubbleModel.fExtrapolatedSpline
        self.interpolatedDomain = self.AssetBubbleModel.FlorenZmirou.InterpolatedRange
        self.extrapolatedDomain = self.AssetBubbleModel.extrapolatedPlotDomain
        self.inverseVariancePlot = plot(self.interpolatedFunction,self.interpolatedDomain,color=(0,0,1)) + plot(self.extrapolatedFunction,self.extrapolatedDomain,color=(1,0,0))
        self.isAssetBubble = self.DetermineAssetBubble()
        