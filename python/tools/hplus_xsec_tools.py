
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

    def lookup_value(self, parameter1, tan_beta, searched_parameter):
        Spline = ROOT.TGraph()
        
        hplustanb = array('d',[0])
        all_parameter1 = array('d',[0])
        searched_param = array('d',[0])
        
        inputFile_ = ROOT.TFile(self.inputFileName_)
        tree = ROOT.TTree()
        inputFile_.GetObject("FeynHiggs_results", tree)
        tree.SetBranchAddress( "tanb", hplustanb )
        if "lowmH" in self.inputFileName_:
            tree.SetBranchAddress( "mu", all_parameter1 )
        else :
            tree.SetBranchAddress( "mA", all_parameter1 )
        tree.SetBranchAddress( searched_parameter, searched_param )

        k=0
        Spline = ROOT.TGraph()
        i=0
        while tree.GetEntry(i):
            i += 1
            if hplustanb[0]==tan_beta :
                Spline.SetPoint(k, float(all_parameter1[0]), float(searched_param[0]))
                k=k+1
        Spline.Sort()
        if not "lowmH" in self.inputFileName_:
            if searched_parameter=="mA" :
                return parameter1
        return Spline.Eval(float(parameter1))

    def _add_br_tHpb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for t->Hp+b"
        # Unpack
        type, type_info = input
        type_info['BR-tHpb'] = self.lookup_value(parameter1, tan_beta, "BR_tHpb")

    def _add_br_taunu(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for Hp->tau+nu"
        # Unpack
        type, type_info = input
        type_info['BR-taunu'] = self.lookup_value(parameter1, tan_beta, "BR_Hp_taunu")

    def _add_mass(self, parameter1, tan_beta, input):
        " Lookup the mass for Hp"
        type, type_info = input
        type_info['mass'] = self.lookup_value(parameter1, tan_beta, "mHp")

    def _add_massA(self, parameter1, tan_beta, input):
        " Lookup the mass for Hp"
        type_info = input
        type_info['massA'] = self.lookup_value(parameter1, tan_beta, "mA")

    def _add_xsec(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('HH', self.unit_pb), ('HW', self.unit_pb) ]:
            type_info['xsec'][prod_type] = unit*self.lookup_value(parameter1, tan_beta, "tHp_xsec")

    def _add_mu(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        type_info['mu']['HH'] = {
            -1 : float(0.21),
            +1 : float(0.21),
            0 : 0,
            }
        type_info['mu']['HW'] = {
            -1 : float(0.21),
            +1 : float(0.21),
            0 : 0,
            }

    def query(self, parameter1, tan_beta): #parameter1 = higgsino mass mu in case of lowmH and mass of pseudoscalar in all other scenarios 

        higgs_types = [ 'Hp' ]
        
        # Build emtpy dictionaries for each Higgs type
        output = {
            'mA' : parameter1,
            'tan_beta' : tan_beta,
            'higgses' : {
                'Hp' : {}
            }
        }
        
        for higgs_type in higgs_types:
            self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_tHpb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_taunu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_mu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
        self._add_massA(parameter1, tan_beta, output)
        print output
        return output
