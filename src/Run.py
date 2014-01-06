'''
Created on Nov 6, 2013

@author: Jas
'''
from sage.all import *
from Stock import *
from FlorenZmirou import *
from AssetBubble import *

import math
def frange(x, y, jump):
    l = list()
    while x < y:
        l.append(x)
        x += jump
    return l
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
    #    tickerData = Stock(filename="../old/scripts/csv/CLF_2013-04-29.csv")#part 0
    Params = ['ba',1,60]
    tickerData = Stock(tickerParams=Params)#part 0
    tickerMax = tickerData.GetMaxStockPrice()#xmax
    tickerMin = tickerData.GetMinStockPrice()#xmin
    tickerStepSize = (tickerMax - tickerMin)/100.0
    tickerRange = frange(tickerMin,tickerMax,tickerStepSize)
    florenZmirou = FlorenZmirou(tickerData)
    Asset = AssetBubble(florenZmirou)
    print Asset.isBubble
    print Asset.m_bar
#    sigma = florenZmirou.CubicInterpolatedSigma
#    sigmaValues = []
#    for x in tickerRange:
#        sigmaValues.append((x,sigma(x)))
#    sigmaValuesMax = max([sigmaValue[1] for sigmaValue in sigmaValues if not math.isnan(sigmaValue[1])])#ymax
#    sigmaValuesMin = min([sigmaValue[1] for sigmaValue in sigmaValues if not math.isnan(sigmaValue[1])])#ymin
#    sigmaGraph = list_plot(sigmaValues,plotjoined=True,xmax=tickerMax+1,xmin=tickerMin-1,ymax=sigmaValuesMax+1,ymin=sigmaValuesMin-1)
#    sigmaGraph.save("sigmaGraph%s.png"%Params[0])
#    table = florenZmirou.CreateZmirouTable()
#    print table
#    assetBubbleDetectionObject = AssetBubbleDetection(florenZmirou)
#    assetBubbleDetectionObject.inverseVariancePlot.save("interpolatedExtrapolatedInverseVariancePlot%s.png"%Params[0])
#    if assetBubbleDetectionObject.isAssetBubble:
#        print "\n%s has a bubble!\n"%Params[0]
#    else:
#        print "\n%s has no bubble!\n"%Params[0]