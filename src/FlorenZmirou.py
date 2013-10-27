'''
Created on Oct 27, 2013

@author: Jas
'''

class FlorenZmirou(object):
    '''
    FlorenZmirou will provide us list of sigma values and interpolation from list of stock prices
    '''


    def __init__(self,stock):
        '''
        Input: Stock
        Discription: Step1: From stock, it will give us sigma(x)
                     Step2: Interpolate sigma(x) using step1.
        '''
        