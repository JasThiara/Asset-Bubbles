'''
Created on Nov 6, 2013

@author: Jas
'''
from sage.all import *
import csv, multiprocessing
from datetime import date
from FlorenZmirou import FlorenZmirou
from CrossValidation import *
def BuildNASDAQRowEntry(x):
    return FlorenZmirou(tickerParams=[x[0],1,60,False,x[1]])
def BuildNYSERowEntry(x):
    return FlorenZmirou(tickerParams=[x[0],1,60,True,x[1]])

if __name__ == '__main__':
    nasdaqFileReader = open('TickerSymbols/bubbleTest.csv','r')
    nasdaqFileWriter = open('TickerSymbols/bubbleOutput.csv','w')
    nasdaqCsvReader = csv.reader(nasdaqFileReader,delimiter=',')
    nasdaqCsvWriter = csv.writer(nasdaqFileWriter,delimiter=',')
    todaysDate = date.today()
    fzList = [BuildNASDAQRowEntry(z) for z in nasdaqCsvReader]
    for FZ in fzList:
        crossValidationN1 = ExtrapolationOptimizationTestN1(FZ)
        mBarN1 = crossValidationN1.sortedResultantList[0][0]
        if mBarN1 < .9:
            isBubble = False
            mBarN2= -1
        elif mBarN1 > 1.1:
            isBubble = True
            mBarN2= -1
        else:
            crossValidationN2 = ExtrapolationOptimizationTestN2(FZ)
            mBarN2 = crossValidationN2.sortedResultantList[0][0]
            if mBarN2 < .9:
                isBubble = False
            elif mBarN2 > 1.1:
                isBubble = True
            else:
                isBubble = -1
        nasdaqCsvWriter.writerow((FZ.CompanyName,FZ.Ticker,todaysDate,todaysDate,isBubble,mBarN1,mBarN2))
    
