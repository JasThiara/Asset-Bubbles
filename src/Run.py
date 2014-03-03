'''
Created on Nov 6, 2013

@author: Jas
'''
from sage.all import *
import csv, multiprocessing
from datetime import date
from FlorenZmirou import FlorenZmirou

def BuildNASDAQRowEntry(x):
    return FlorenZmirou(tickerParams=[x[0],2,60,False,x[1]])
def BuildNYSERowEntry(x):
    return FlorenZmirou(tickerParams=[x[0],2,60,True,x[1]])

if __name__ == '__main__':
    nasdaqFileReader = open('TickerSymbols/NASDAQ.csv','r')
    nyseFileReader = open('TickerSymbols/NYSE.csv','r')
    nasdaqCsvReader = csv.reader(nasdaqFileReader,delimiter=',')
    nyseCsvReader = csv.reader(nyseFileReader,delimiter=',')
    todaysDate = date.today()
    try:
        cpus = multiprocessing.cpu_count()
    except NotImplementedError:
        cpus = 2   # arbitrary default
    nyseEntries = [row for row in nyseCsvReader]
    nasdaqEntries = [row for row in nasdaqCsvReader]
    NYSEflorenZmirouListPoolingProcess = multiprocessing.Pool(processes=cpus)
    NASDAQflorenZmirouListPoolingProcess = multiprocessing.Pool(processes=cpus)
    nyseFlorenZmirouList = NYSEflorenZmirouListPoolingProcess.map(BuildNYSERowEntry,nyseEntries)
    nasdaqFlorenZmirouList = NASDAQflorenZmirouListPoolingProcess.map(BuildNASDAQRowEntry,nasdaqEntries)
    florenZmirouList = nyseFlorenZmirouList.extend(nasdaqFlorenZmirouList)
    