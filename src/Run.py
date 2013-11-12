'''
Created on Nov 6, 2013

@author: Jas
'''
import pylab as pl
from sage.all import *
from Stock import *
from FlorenZmirou import *
from AssetBubble import *
if __name__ == '__main__':
    m = 1
    BBRY = Stock("../old/scripts/BBRY_2013-04-29.csv")# or "..\scripts\csv\[TICKER]_YYYY-MM-DD.csv"
    High = BBRY.GetMaxStockPrice()
    Low = BBRY.GetMinStockPrice()
    StepSize = float(High-Low)/100.0
    Prices = pl.frange(Low,High,StepSize)
    BBRYFlorenZmirou = FlorenZmirou(BBRY)
    Sigmas = [BBRYFlorenZmirou.CubicInterpolatedSigma(x) for x in Prices]#needs to be fixed
    PriceSigmaPoints = [(price,sigma) for price in Prices for sigma in Sigmas]
    InterpolatedSigmaGraph = line(PriceSigmaPoints)
    InterpolatedSigmaGraph.save("InterpolatedSigma.png")
    BBRYAssetBubble = AssetBubble(BBRYFlorenZmirou)
    F = vector(BBRYAssetBubble.InverseVariance)
    
    #ReproducingKernelArray = [[BBRYAssetBubble.ReproducingKernalFunction(2,m,x,y) for x in BBRYFlorenZmirou.UsableGridPoints] for y in BBRYFlorenZmirou.UsableGridPoints]
    #ReproducingKernelQ = matrix(ReproducingKernelArray)
    #c = ReproducingKernelQ.inverse() * F
    print "F in Latex: \n %s\n\n\n"%latex(F)
    print "GridPoints: \n %s \n\n\n"%BBRYFlorenZmirou.GridPoints
    print "UsableGridPoints: \n %s \n\n\n"%BBRYFlorenZmirou.UsableGridPoints
    print "Estimated Sigma: \n %s \n\n\n"%BBRYFlorenZmirou.EstimatedSigma
    
    #print "Q in Latex: \n %s\n\n\n"%latex(ReproducingKernelQ)
    #print "c in Latex: \n %s\n\n\n"%latex(c)
    