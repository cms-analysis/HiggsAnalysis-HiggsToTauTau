
import ROOT

import math

from HiggsAnalysis.HiggsToTauTau.tools.mssm_xs_tools import mssm_xs_tools


class mssm_xsec_tools():

    def __init__(self, inputFileName, kINTERPOLATION, verbosity):
        self.unit_pb = 1.
        self.unit_fb = self.unit_pb*1.e-3
        self.inputFileName_ = inputFileName
        self.mssm = mssm_xs_tools(inputFileName, kINTERPOLATION, verbosity)

    @staticmethod
    def _add_in_quadrature(*xs):
        return math.sqrt(sum(x*x for x in xs))

    def _add_br_htt(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-tautau'] = self.mssm.br("%s->tautau" % type, parameter1, tan_beta)

    def _add_br_hmm(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-mumu'] = self.mssm.br("%s->mumu" % type, parameter1, tan_beta)

    def _add_br_hbb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-bb'] = self.mssm.br("%s->bb" % type, parameter1, tan_beta)

    def _add_br_Hhh(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-hh'] = self.mssm.br("%s->hh" % type, parameter1, tan_beta)

    def _add_br_AZh(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-Zh'] = self.mssm.br("%s->Zh" % type, parameter1, tan_beta)

    def _add_br_tHpb(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-tHpb'] = self.mssm.br("t->Hpb", parameter1, tan_beta)

    def _add_br_taunu(self, parameter1, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR-taunu'] = self.mssm.br("%s->taunu" % type, parameter1, tan_beta) 

    def _add_mass(self, parameter1, tan_beta, input):
        " Lookup the mass for a given higgs type "
        type, type_info = input
        if type == 'A':
            if self.inputFileName_.find('lowmH')>-1 :
                type_info['mass'] = self.mssm.mass("%s" % type, parameter1, tan_beta)
                return
            else :
                type_info['mass'] = parameter1
                return
        type_info['mass'] = self.mssm.mass("%s" % type, parameter1, tan_beta)

    def _add_xsec(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('gg', self.unit_pb), ('bb5F', self.unit_pb), ('bb4F', self.unit_pb) , ('bbSantander', self.unit_pb)]:
            type_info['xsec'][prod_type] = unit*self.mssm.xsec("%s->%s" % (prod_type, type), parameter1, tan_beta)
            
    def _add_muHp(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        type_info['mu']['HpHp'] = {
            -1 : float(0.21),
             +1 : float(0.21),
             0 : 0,
             }
        type_info['mu']['HpW'] = {
            -1 : float(0.21),
             +1 : float(0.21),
             0 : 0,
             }
        
    def _add_mu(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        type_info['mu']['bb5F'] = {
            -1 : (self.mssm.xsec("bb5F->%s::scaleDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bb5F->%s" % type, parameter1, tan_beta))*self.unit_pb,
             +1 : (self.mssm.xsec("bb5F->%s::scaleUp" % type, parameter1, tan_beta) -
                   self.mssm.xsec("bb5F->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        type_info['mu']['gg'] = {
            -1 : (self.mssm.xsec("gg->%s::scaleDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("gg->%s" % type, parameter1, tan_beta))*self.unit_pb,
             +1 : (self.mssm.xsec("gg->%s::scaleUp" % type, parameter1, tan_beta) -
                   self.mssm.xsec("gg->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        type_info['mu']['bb4F'] = {
            -1 : (self.mssm.xsec("bb4F->%s::scaleDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bb4F->%s" % type, parameter1, tan_beta))*self.unit_pb,
             +1 : (self.mssm.xsec("bb4F->%s::scaleUp" % type, parameter1, tan_beta) -
                   self.mssm.xsec("bb4F->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        type_info['mu']['bbSantander'] = {
            -1 : (self.mssm.xsec("bbSantander->%s::scaleDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bbSantander->%s" % type, parameter1, tan_beta))*self.unit_pb,
             +1 : (self.mssm.xsec("bbSantander->%s::scaleUp" % type, parameter1, tan_beta) -
                   self.mssm.xsec("bbSantander->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }

    def _add_pdf(self, parameter1, tan_beta, input):
        type, type_info = input
        type_info.setdefault('pdf', {})
        type_info['pdf']['bb5F'] = {               
            -1 : (self.mssm.xsec ("bb5F->%s::pdfasDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bb5F->%s" % type, parameter1, tan_beta))*self.unit_pb,
            +1 : (self.mssm.xsec ("bb5F->%s::pdfasUp" % type, parameter1, tan_beta)- 
                  self.mssm.xsec("bb5F->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        type_info['pdf']['gg'] = {
            -1 : (self.mssm.xsec ("gg->%s::pdfasDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("gg->%s" % type, parameter1, tan_beta))*self.unit_pb,
            +1 : (self.mssm.xsec ("gg->%s::pdfasUp" % type, parameter1, tan_beta) -
                  self.mssm.xsec("gg->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        type_info['pdf']['bbSantander'] = {
            -1 : (self.mssm.xsec ("bbSantander->%s::pdfasDown" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bbSantander->%s" % type, parameter1, tan_beta))*self.unit_pb,
            +1 : (self.mssm.xsec ("bbSantander->%s::pdfasUp" % type, parameter1, tan_beta) -
                  self.mssm.xsec("bbSantander->%s" % type, parameter1, tan_beta))*self.unit_pb,
             0 : 0,
             }
        # Supposedly negligble compared to scale
        type_info['pdf']['bb4F'] = {
            -1 : 0,
             +1 : 0,
             0 : 0,
             }

    def query(self, parameter1, tan_beta, ana_type): #parameter1 = mu in case of lowmH and mA in all other scenarios 
        
        output = {}
        
        if ana_type=='Htaunu' :
            higgs_types = [ 'Hp' ]
         
            # Build emtpy dictionaries for each Higgs type
            output = {
                'parameter1' : parameter1,
                'tan_beta' : tan_beta,
                'higgses' : {
                    'Hp' : {}
                    }
                }
         
            for higgs_type in higgs_types:
                self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_tHpb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_taunu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                #self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_muHp(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                
        else :
            higgs_types = [ 'h', 'A', 'H' ]
            
            # Build emtpy dictionaries for each Higgs type
            output = {
                'parameter1' : parameter1,
                'tan_beta' : tan_beta,
                'higgses' : {
                    'h' : {},
                    'A' : {},
                    'H' : {}
                    }
                }
            for higgs_type in higgs_types:
                self._add_br_htt(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_hmm(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_br_hbb(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                if ana_type=='Hhh' or ana_type=='AZh' or ana_type=='HhhAndAZh' :
                    self._add_br_Hhh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                    self._add_br_AZh(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_mass(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_xsec(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_mu(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
                self._add_pdf(parameter1, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            

        #print output
        return output
    
