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
    #Objectives
    #0) load ticker data
    #1) for m = 1,...,9:
    #1.1) create FlorenZmirou object
    #1.2) create AssetBubble Object
    #1.3) create table with the following:
    #1.3.1) Usable Grid Points
    #1.3.2) Estimated Sigma value from Floren Zmirou Estimator
    #1.3.3) Number of Points for each Grid Point
    #1.3.4) Plot cubic spline interpolation of sigma
    #1.4)Extrapolate sigma_b if necessary
    tickerData = Stock("../old/scripts/BBRY_2013-04-29.csv")#part 0
    tickerMax = tickerData.GetMaxStockPrice()
    tickerMin = tickerData.GetMinStockPrice()
    tickerStepSize = (tickerMax - tickerMin)/100.0
    tickerRange = pl.frange(tickerMax,tickerMin,tickerStepSize)
    florenZmirou = FlorenZmirou(tickerData)
    sigma = florenZmirou.CubicInterpolatedSigma
    sigmaValues = []
    for x in tickerRange:
        sigmaValues.append(sigma(x))
    sigmaGraph = list_plot(sigmaValues,plotjoined=True)
    sigmaGraph.save("sigmaGraph.png")
    dataDictionary = {}
    for m in range(1,10):
        #1.3) create table with the following:
        #1.3.1) Usable Grid Points
        #1.3.2) Estimated Sigma value from Floren Zmirou Estimator
        #1.3.3) Number of Points for each Grid Point
        #1.3.4) Plot cubic spline interpolation of sigma
        dataDictionary[m] = []
        alpha = (1.0+m)/2.0
        assetBubble  = AssetBubble(florenZmirou,alpha,m)
        dataDictionary[m].append(florenZmirou.EstimatedSigma)
        histogram = {gridPoint:[len(florenZmirou.StockPricesByGridPointDictionary[gridPoint])] for gridPoint in florenZmirou.UsableGridPoints}
        dataDictionary[m].append(histogram)
#    m = 1
#    BBRY = Stock("../old/scripts/BBRY_2013-04-29.csv")# or "../scripts/csv/[TICKER]_YYYY-MM-DD.csv"
##    High = BBRY.GetMaxStockPrice()
##    Low = BBRY.GetMinStockPrice()
##    StepSize = float(High-Low)/100.0
##    Prices = pl.frange(Low,High,StepSize)
##    BBRYFlorenZmirou = FlorenZmirou(BBRY)
##    BBRYVariance = [BBRYFlorenZmirou.CubicInterpolatedSigma(x) for x in Prices]#needs to be fixed
##    InterpolatedSigmaGraph = line(PriceSigmaPoints)
##    InterpolatedSigmaGraph.save("InterpolatedSigma.png")
#    BBRYAssetBubble = AssetBubble(BBRYFlorenZmirou)
#    F = vector(BBRYAssetBubble.InverseVariance)
#    
#    #ReproducingKernelArray = [[BBRYAssetBubble.ReproducingKernalFunction(2,m,x,y) for x in BBRYFlorenZmirou.UsableGridPoints] for y in BBRYFlorenZmirou.UsableGridPoints]
#    #ReproducingKernelQ = matrix(ReproducingKernelArray)
#    #c = ReproducingKernelQ.inverse() * F
#    print "F in Latex: \n %s\n\n\n"%latex(F)
#    print "GridPoints: \n %s \n\n\n"%BBRYFlorenZmirou.GridPoints
#    print "UsableGridPoints: \n %s \n\n\n"%BBRYFlorenZmirou.UsableGridPoints
#    print "Estimated Sigma: \n %s \n\n\n"%BBRYFlorenZmirou.EstimatedSigma
#    
#    #print "Q in Latex: \n %s\n\n\n"%latex(ReproducingKernelQ)
#    #print "c in Latex: \n %s\n\n\n"%latex(c)
#    