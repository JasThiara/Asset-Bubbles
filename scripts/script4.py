'''
Created on Mar 31, 2013

@author: Jas
'''
import urllib 
from datetime import date
def request(ticker):
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/%s/chartdata;type=quote;range=1d/csv'%ticker
    return urllib.urlopen(url).read()
def create_file(filename):
    return open(filename,'w')
def csv_file(filename,data):
    fileptr = create_file(filename)
    fileptr.write(data) 
    fileptr.close()
if __name__ == '__main__':
    TICKERS = ['BBRY','PANL','VHC','SLCS','SRPT','DDD','WAC','PANL','MLNX','BSFT','BBY','CLF','NSM','WLT']
    get_today_date = date.today() 
    for ticker in TICKERS:
        Data = request(ticker) 
        filename = "csv/%s_%s.csv"%(ticker, get_today_date)
        csv_file(filename,Data)
        