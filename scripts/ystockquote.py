#!/usr/bin/env python
#
#  Copyright (c) 2007-2008, Corey Goldberg (corey@goldb.org)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.


import urllib


"""
This is the "ystockquote" module.

This module provides a Python API for retrieving stock data from Yahoo Finance.

sample usage:
>>> import ystockquote
>>> print ystockquote.get_price('GOOG')
529.46
"""


def __request(symbol, stat):#Python provides several ways to download the file that in its standard library, download a file is over HTTP using the urllib or urllib2 module. The requests library method is get, which corresponds to the HTTP GET. Then you just take the requests object and call its content property to get the data you want to write. . 
    url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
    return urllib.urlopen(url).read().strip().strip('"')# opening the url,reading and removing the leading char from string


def get_all(symbol):
    """
    Get all available quote data for the given ticker symbol.
    
    Returns a dictionary.
    """
    values = __request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')# requesting informaton from url and giving symbol and stat and making string 
    data = {} # dictinory of string 
    data['price'] = values[0] # The price of each stock 
    data['change'] = values[1]# the change in price from the beginning of the day time to end time
    data['volume'] = values[2]# number of stock traded in specific given period 
    data['avg_daily_volume'] = values[3] # average number of volume of stock traded in time 
    data['stock_exchange'] = values[4]# new york stock exchange- where stock is being exchanged
    data['market_cap'] = values[5]# the value of the stock
    data['book_value'] = values[6]# book value = total assets-intangible assets-liabilities.
    data['ebitda'] = values[7]# earnings before interest taxes depreciations amortization
    data['dividend_per_share'] = values[8]# owner's pay check per share owned
    data['dividend_yield'] = values[9] # = total dividend for one year divided by price
    data['earnings_per_share'] = values[10]# ebitda divided by total shares outstanding 
    data['52_week_high'] = values[11]# highest price of past 52 weeks
    data['52_week_low'] = values[12]# lowest price
    data['50day_moving_avg'] = values[13]# average price over the past 50 days
    data['200day_moving_avg'] = values[14]# average price over the past 200 days
    data['price_earnings_ratio'] = values[15]# market price per share divided by annual earning per share
    data['price_earnings_growth_ratio'] = values[16]
    data['price_sales_ratio'] = values[17] # market cap divided by the revenue of recent year
    data['price_book_ratio'] = values[18]
    data['short_ratio'] = values[19]# ratio of short sales by investors
    return data
    
    
def get_price(symbol): # function get_price from stock symbol 
    return __request(symbol, 'l1') # returning  the requested url symbol and going to dict pointing to l1


def get_change(symbol):
    return __request(symbol, 'c1')
    
    
def get_volume(symbol): 
    return __request(symbol, 'v')


def get_avg_daily_volume(symbol): 
    return __request(symbol, 'a2')
    
    
def get_stock_exchange(symbol): 
    return __request(symbol, 'x')
    
    
def get_market_cap(symbol):
    return __request(symbol, 'j1')
   
   
def get_book_value(symbol):
    return __request(symbol, 'b4')


def get_ebitda(symbol): 
    return __request(symbol, 'j4')
    
    
def get_dividend_per_share(symbol):
    return __request(symbol, 'd')


def get_dividend_yield(symbol): 
    return __request(symbol, 'y')
    
    
def get_earnings_per_share(symbol): 
    return __request(symbol, 'e')


def get_52_week_high(symbol): 
    return __request(symbol, 'k')
    
    
def get_52_week_low(symbol): 
    return __request(symbol, 'j')


def get_50day_moving_avg(symbol): 
    return __request(symbol, 'm3')
    
    
def get_200day_moving_avg(symbol): 
    return __request(symbol, 'm4')
    
    
def get_price_earnings_ratio(symbol): 
    return __request(symbol, 'r')


def get_price_earnings_growth_ratio(symbol): 
    return __request(symbol, 'r5')


def get_price_sales_ratio(symbol): 
    return __request(symbol, 'p5')
    
    
def get_price_book_ratio(symbol): 
    return __request(symbol, 'p6')
       
       
def get_short_ratio(symbol): 
    return __request(symbol, 's7')
    
    
def get_historical_prices(symbol, start_date, end_date): # three argument variables 
    """
    Get historical prices for the given ticker symbol.
    Date format is 'YYYYMMDD'
    
    Returns a nested list.
    """
    url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
          'd=%s&' % str(int(end_date[4:6]) - 1) + \
          'e=%s&' % str(int(end_date[6:8])) + \
          'f=%s&' % str(int(end_date[0:4])) + \
          'g=d&' + \
          'a=%s&' % str(int(start_date[4:6]) - 1) + \
          'b=%s&' % str(int(start_date[6:8])) + \
          'c=%s&' % str(int(start_date[0:4])) + \
          'ignore=.csv'
    days = urllib.urlopen(url).readlines()
    data = [day[:-2].split(',') for day in days]
    return data
        