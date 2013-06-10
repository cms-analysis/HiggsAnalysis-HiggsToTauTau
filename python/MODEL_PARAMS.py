class MODEL_PARAMS:
    "Class for storing parameters of a model "
    def __init__(self):
        self.list_of_higgses = ['A', 'H', 'h']
        self.masses = {'A' : '120', 'H' : '130', 'h' : '118'}
        self.xsecs  = {'A' : '3'  , 'H' : '2'  , 'h' : '1'  }
        self.brs    = {'A' : '0.1', 'H' : '0.1', 'h' : '0.1'}
        self.tanb = 15
    def _add_higgs(self,higgs):
        " Adding higgs to list_of_higgs"
        self.list_of_higgses.append(higgs)
    def _set_masses(self, higgs, mass):
        " Adding mass for higgs to parameters "
        self.masses[higgs] = mass
    def _set_xsec(self, higgs, xsec):
        " Adding xsec for higgs to parameters "
        self.xsecs[higgs] = xsec
    def _set_br(self, higgs, br):
        " Adding br for higgs to parameters "
        self.brs[higgs] = br
