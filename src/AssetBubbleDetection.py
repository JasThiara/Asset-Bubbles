'''
Created on Nov 21, 2013

@author: Jas
'''
from sage.all import *
class AssetBubbleDetection(object):
    '''
    This class performs asset bubble detection over a variety of asset bubble objects
    Bubble Detection Strategy
    1) find an appropriate alpha using lagrangian multiplier(s)
    
    2) Suppose we know alpha, and have a floren zmirou object, FZ:
    assetBubbleList = list()
    for m = 1,...,9
        for n = 1,2,3
            assetBubbleList.append(AssetBubble(FZ,alpha,m,n))
    3) From the assetBubbleList, find the best assetBubble with the closest extrapolated approximation
    i.e.find f_alpha such that  min_{m,n in Integers} |f'(maxPrice ) - f_alpha ' (maxPrice)|
    4) Determine if f_alpha from (3) goes to infinity using proposition 3, if not infinity declare not asset bubble
    5) if determined matingale,  do Step D
    6) declare yes/no on asset bubble.
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass