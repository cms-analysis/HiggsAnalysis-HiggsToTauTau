

import math

class MODEL_PARAMS :
    """Class for storing parameters of a model"""
    def __init__(self, ana_type):
        if ana_type=="Hplus":
           self.list_of_higgses = ['Hp']
           self.masses = {'Hp' : '125'}
           self.xsecs  = {'Hp' : '3'  }
           self.brs    = {'Hp' : '0.1'}
           self.ttscale= '1'
        else :
            self.list_of_higgses = ['A', 'H', 'h']
            self.masses = {'A' : '125', 'H' : '130', 'h' : '118'}
            self.xsecs  = {'A' : '3'  , 'H' : '2'  , 'h' : '1'  }
            self.brs    = {'A' : '0.1', 'H' : '0.1', 'h' : '0.1'}
        self.tanb = 15
        
    def effective(self, MOMENT=1, higgses=None) :
        """Return xsec*br for all elements indicated in higgses"""
        value = 0.
        if not higgses :
            higgses = self.list_of_higgses
        for x in higgses :
            value+=math.pow(float(self.xsecs[x])*float(self.brs[x]), MOMENT)
        return value if MOMENT == 1 else math.pow(value, 1./MOMENT)
    
