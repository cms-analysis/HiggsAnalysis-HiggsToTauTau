
import ROOT

import math
from array import array

class twohdm_xsec_tools():

    def __init__(self, inputFileName):
        self.inputFileName_ = inputFileName
        self.unit_pb = 1.
        self.unit_fb = self.unit_pb*1.e-3

    def lookup_value(self, parameter1, tan_beta, searched_parameter, branch=""):
        Spline = ROOT.TGraph()
        
        twoHDMtanb = array('f',[0])
        all_parameter1 = array('f',[0])
        if branch=="" :
            searched_param = array('f',[0])
        
        inputFile_ = ROOT.TFile(self.inputFileName_)
        tree = ROOT.TTree()
        inputFile_.GetObject("Tree2HDM", tree)
        tree.SetBranchAddress( "tanbeta", twoHDMtanb )
        tree.SetBranchAddress( "cosba", all_parameter1 )
        if branch=="" :
            tree.SetBranchAddress( searched_parameter, searched_param )
        else :
            test = tree.GetLeaf(branch, searched_parameter)
            
        k=0
        Spline = ROOT.TGraph()
        i=0
        #print searched_parameter
        while tree.GetEntry(i):
            if twoHDMtanb[0]==tan_beta :
                if branch=="" :
                    #print float(all_parameter1[0]), float(searched_param[0]), float(parameter1)
                    Spline.SetPoint(k, float(all_parameter1[0]), float(searched_param[0]))
                else :
                    test.GetBranch().GetEntry(i)
                    #print float(all_parameter1[0]), float(test.GetValue()), float(parameter1)
                    Spline.SetPoint(k, float(all_parameter1[0]), float(test.GetValue()))
                k=k+1
            i += 1
        Spline.Sort()
        #print Spline.Eval(float(parameter1))
        #print " ------------------------------------------------------------------------------"
        return Spline.Eval(float(parameter1))

    def _add_br_hh(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for t->Hp+b"
        # Unpack
        type, type_info = input
        if type=="h" or type=="A" :
            type_info['BR-hh'] = 0
        else :
            type_info['BR-hh'] = self.lookup_value(parameter1, tan_beta, "hh", "BR%s" % type)

    def _add_br_zh(self, parameter1, tan_beta, input) :
        type, type_info = input
        if type=="h" or type=="H" :
            type_info['BR-Zh'] = 0
        else :
            type_info['BR-Zh'] = self.lookup_value(parameter1,tan_beta,"Zh","BR%s" % type)

    def _add_br_tautau(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for Hp->tau+nu"
        # Unpack
        type, type_info = input
        type_info['BR-tautau'] = self.lookup_value(parameter1, tan_beta, "tautau", "BR%s" % type)

    def _add_br_bb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for Hp->tau+nu"
        # Unpack
        type, type_info = input
        type_info['BR-bb'] = self.lookup_value(parameter1, tan_beta, "bb", "BR%s" % type)

    def _add_mass(self, parameter1, tan_beta, input):
        " Lookup the mass for each Higgs"
        type, type_info = input
        if type=="h" :
            type_info['mass'] = 125
        else :
            type_info['mass'] = self.lookup_value(parameter1, tan_beta, "m%s" % type)

    def _add_xsec(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('ggF', self.unit_pb)]:
            type_info['xsec'][prod_type] = unit*self.lookup_value(parameter1, tan_beta, "gg%s" % type)
        for prod_type, unit in [ ('santander', self.unit_pb)]: #this is only 5f scheme, but naming is needed to be picked up correctly
            type_info['xsec'][prod_type] = unit*self.lookup_value(parameter1, tan_beta, "bb%s" % type)


    ## def _add_mu(self, parameter1, tan_beta, input):
##         type, type_info = input
##         type_info.setdefault('mu', {})
##         type_info['mu']['HH'] = {
##             -1 : float(0.21),
##             +1 : float(0.21),
##             0 : 0,
##             }
##         type_info['mu']['HW'] = {
##             -1 : float(0.21),
##             +1 : float(0.21),
##             0 : 0,
##             }

    def query(self, parameter1, tan_beta): #parameter1 = cos(beta-alpha) 

        higgs_types = [ 'h', 'H', 'A' ]
        
        # Build emtpy dictionaries for each Higgs type
        output = {
            'parameter1' : parameter1,
            'tan_beta' : tan_beta,
            'higgses' : {
                'h' : {},
                'H' : {},
                'A' : {},
            }
        }
        
        for higgs_type in higgs_types:
            self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_zh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_hh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_tautau(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_bb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            #self._add_mu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
        
        print output
        return output
