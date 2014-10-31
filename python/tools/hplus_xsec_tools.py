
import ROOT

import math
from array import array

class hplus_xsec_tools():

    def __init__(self, inputFileName):
        self.inputFileName_ = inputFileName
        self.unit_pb = 1.
        self.unit_fb = self.unit_pb*1.e-3

    ## @staticmethod
##     def _add_in_quadrature(*xs):
##         return math.sqrt(sum(x*x for x in xs))

    def lookup_value(self, mA, tan_beta, parameter):
        Spline = ROOT.TGraph()
        
        hplustanb = array('d',[0])
        massA = array('d',[0])
        param = array('d',[0])
        
        inputFile_ = ROOT.TFile(self.inputFileName_)
        tree = ROOT.TTree()
        inputFile_.GetObject("FeynHiggs_results", tree)
        tree.SetBranchAddress( "tanb", hplustanb )
        tree.SetBranchAddress( "mA", massA )
        print parameter
        tree.SetBranchAddress( parameter, param )

        k=0
        Spline = ROOT.TGraph()
        i=0
        while tree.GetEntry(i):
            i += 1
            #if i==1 :
                #print massA[0], hplustanb[0], param[0], tan_beta
            if hplustanb[0]==tan_beta :
                #print float(massA[0]), float(param[0])
                Spline.SetPoint(k, float(massA[0]), float(param[0]))
            k=k+1
        #del hplustanb, massA, param
        Spline.Sort()
        print Spline.Eval(float(mA))
        print "-----------------------------------------------------"
        return Spline.Eval(float(mA))

    def _add_br_tHpb(self, mA, tan_beta, input):
        " Lookup the branching ratio for t->Hp+b"
        # Unpack
        type, type_info = input
        type_info['BR-tHpb'] = self.lookup_value(mA, tan_beta, "BR_tHpb")

    def _add_br_taunu(self, mA, tan_beta, input):
        " Lookup the branching ratio for Hp->tau+nu"
        # Unpack
        type, type_info = input
        type_info['BR-taunu'] = self.lookup_value(mA, tan_beta, "BR_Hp_taunu")

    def _add_mass(self, mA, tan_beta, input):
        " Lookup the mass for Hp"
        type, type_info = input
        type_info['mass'] = self.lookup_value(mA, tan_beta, "mHp")

    def _add_xsec(self, mA, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('tHp_xsec', self.unit_pb)]:
            type_info['xsec'][prod_type] = unit*self.lookup_value(mA, tan_beta, "tHp_xsec")

    ## def _add_mu(self, mA, tan_beta, input):
##         type, type_info = input
##         type_info.setdefault('mu', {})
##         if(self.inputFileName_.find('mhmax-mu+200')>-1) : #for old mhmax scenario not produced with sushi
##             type_info['mu']['bbH'] = {
##                 -1 : self.lookup_value(mA, tan_beta, 'h_bbH_mudown_%s' % type)*self.unit_pb,
##                 +1 : self.lookup_value(mA, tan_beta, 'h_bbH_muup_%s' % type)*self.unit_pb,
##                 0 : 0,
##             }
##         else :
##             type_info['mu']['bbH'] = {
##                 -1 : (self.lookup_value(mA, tan_beta, 'h_bbH_mudown_%s' % type) -
##                       self.lookup_value(mA, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
##                 +1 : (self.lookup_value(mA, tan_beta, 'h_bbH_muup_%s' % type) -
##                       self.lookup_value(mA, tan_beta, 'h_bbH_xsec_%s' % type))*self.unit_pb,
##                 0 : 0,
##                 }
##         type_info['mu']['bbH4f'] = {
##             -1 : (self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s_low' % type) -
##                   self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_pb,
##             +1 : (self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s_high' % type) -
##                   self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_pb,
##             0 : 0,
##             }
##         type_info['mu']['ggF'] = {
##             -1 : (self.lookup_value(mA, tan_beta, 'h_ggF_xsec20_%s' % type) -
##                   self.lookup_value(mA, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
##             +1 : (self.lookup_value(mA, tan_beta, 'h_ggF_xsec05_%s' % type) -
##                   self.lookup_value(mA, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
 ##            0 : 0,
##           }

    def query(self, mA, tan_beta):

        higgs_types = [ 'Hp' ]
        
        # Build emtpy dictionaries for each Higgs type
        output = {
            'mA' : mA,
            'tan_beta' : tan_beta,
            'higgses' : {
                'Hp' : {}
            }
        }
        
        for higgs_type in higgs_types:
            self._add_mass(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_tHpb(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_taunu(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_xsec(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            #self._add_mu(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))

        print output
        return output
