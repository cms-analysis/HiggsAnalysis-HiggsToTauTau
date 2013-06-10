class MODEL_PARAMS:
    """Class for storing parameters of a model"""
    def __init__(self):
        self.list_of_higgses = ['A', 'H', 'h']
        self.masses = {'A' : '120', 'H' : '130', 'h' : '118'}
        self.xsecs  = {'A' : '3'  , 'H' : '2'  , 'h' : '1'  }
        self.brs    = {'A' : '0.1', 'H' : '0.1', 'h' : '0.1'}
        self.tanb = 15
