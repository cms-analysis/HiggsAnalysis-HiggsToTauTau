
import ROOT

import math

class mssm_xsec_tools():

    def __init__(self, inputFileName):
        self.inputFileName_ = inputFileName
        self.inputFile_ = ROOT.TFile(self.inputFileName_)

        self.unit_pb = 1.
        self.unit_fb = self.unit_pb*1.e-3

    @staticmethod
    def _add_in_quadrature(*xs):
        return math.sqrt(sum(x*x for x in xs))

    def lookup_value(self, mA, tan_beta, histo):
        try:
            histo = self.inputFile_.Get(histo)
            bin = histo.FindBin(mA, tan_beta)
            return histo.GetBinContent(bin)
        except AttributeError:
            print "Failed to load histogram '%s' from file %s !!" % (histo, inputFileName_)

    @staticmethod
    def santander_matching(mass, xsec_4f, xsec_5f):
        t = ROOT.TMath.Log(mass/4.75) - 2.0
        return (1.0/(1.0 + t))*(xsec_4f + t*xsec_5f)

    @staticmethod
    def santander_error_matching(mass, x_4f, x_5f):
        t = ROOT.TMath.Log(mass/4.75) - 2.0
        return (1.0/(1.0 + t))*(x_4f + t*x_5f)

    def _add_br_htt(self, mA, tan_beta, input):
        " Lookup the branching ratio for a given higgs type "
        # Unpack
        type, type_info = input
        type_info['BR'] = self.lookup_value(mA, tan_beta, "h_brtautau_%s" % type)

    def _add_br_hmm(self, mA, tan_beta, input):
        " Lookup the branching ratio for A/H/h->mumu"
        # Unpack
        type, type_info = input
        type_info['BR-mumu'] = self.lookup_value(mA, tan_beta, "h_brmumu_%s" % type)

    def _add_br_hbb(self, mA, tan_beta, input):
        " Lookup the branching ratio for A/H/h->bb"
        # Unpack
        type, type_info = input
        type_info['BR-bb'] = self.lookup_value(mA, tan_beta, "h_brbb_%s" % type)  

    def _add_mass(self, mA, tan_beta, input):
        " Lookup the mass for a given higgs type "
        type, type_info = input
        if type == 'A':
            type_info['mass'] = mA
            return
        type_info['mass'] = self.lookup_value(mA, tan_beta, "h_m%s" % type)

    def _add_xsec(self, mA, tan_beta, input):
        type, type_info = input
        type_info.setdefault('xsec', {})
        for prod_type, unit in [ ('ggF', self.unit_pb), ('bbH', self.unit_fb), ('bbH4f', self.unit_fb) ]:
            type_info['xsec'][prod_type] = unit*self.lookup_value(mA, tan_beta, "h_%s_xsec_%s" % (prod_type, type))

    def _add_santander(self, input):
        # Type gives Higgs type
        type, type_info = input
        mass_of_this_type = type_info['mass']
        xsec_4f = type_info['xsec']['bbH4f']
        xsec_5f = type_info['xsec']['bbH']
        type_info['xsec']['santander'] = mssm_xsec_tools.santander_matching(mass_of_this_type, xsec_4f, xsec_5f)

        # Add errors.
        mu_up_4f = type_info['mu']['bbH4f'][1]
        mu_up_5f = type_info['mu']['bbH'][1]
        pdf_up_5f = type_info['pdf']['bbH'][1]
        
        mu_down_4f = type_info['mu']['bbH4f'][-1]
        mu_down_5f = type_info['mu']['bbH'][-1]
        pdf_down_5f = type_info['pdf']['bbH'][-1]

        # Separate uncertainties
        type_info['mu']['santander'] = {
            0 : 0,
            1 : mssm_xsec_tools.santander_error_matching(
                mass_of_this_type, mu_up_4f, mu_up_5f),
            -1 : mssm_xsec_tools.santander_error_matching(
                mass_of_this_type, mu_down_4f, mu_down_5f),
        }

        # CV: Apply PDF uncertainty to 5 flavor calculation only
        #     as in C++ version https://twiki.cern.ch/twiki/pub/LHCPhysics/MSSMNeutral/mssm_xs_tools.C
        #    (functions 'GiveXsec_UncDown_Santander_A', 'GiveXsec_UncDown_Santander_H', 'GiveXsec_UncDown_Santander_h')
        t = ROOT.TMath.Log(mass_of_this_type/4.75) - 2.0
        type_info['pdf']['santander'] = {
            0 : 0,
            1 : (1.0/(1.0 + t))*pdf_up_5f,
            -1 : (1.0/(1.0 + t))*pdf_down_5f
        }

    def _add_mu(self, mA, tan_beta, input):
        type, type_info = input
        type_info.setdefault('mu', {})
        for prod_type in ['bbH']:
            type_info['mu'][prod_type] = {
                -1 : self.lookup_value(mA, tan_beta, 'h_%s_mudown_%s' % (prod_type, type))*self.unit_fb,
                +1 : self.lookup_value(mA, tan_beta, 'h_%s_muup_%s' % (prod_type, type))*self.unit_fb,
                 0 : 0,
            }
            type_info['mu']['bbH4f'] = {
                -1 : (self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s_low' % type) -
                      self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_fb,
                +1 : (self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s_high' % type) -
                      self.lookup_value(mA, tan_beta, 'h_bbH4f_xsec_%s' % type))*self.unit_fb,
                 0 : 0,
            }
            type_info['mu']['ggF'] = {
                -1 : (self.lookup_value(mA, tan_beta, 'h_ggF_xsec20_%s' % type) -
                      self.lookup_value(mA, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                +1 : (self.lookup_value(mA, tan_beta, 'h_ggF_xsec05_%s' % type) -
                      self.lookup_value(mA, tan_beta, 'h_ggF_xsec_%s' % type))*self.unit_pb,
                 0 : 0,
            }


    def _add_pdf(self, mA, tan_beta, input):
        type, type_info = input
        type_info.setdefault('pdf', {})
        for prod_type in ['bbH']:
            type_info['pdf'][prod_type] = {
                -1 : self.lookup_value(mA, tan_beta, 'h_%s_pdfalphas68down_%s' % (prod_type, type))*self.unit_fb,
                +1 : self.lookup_value(mA, tan_beta, 'h_%s_pdfalphas68up_%s'   % (prod_type, type))*self.unit_fb,
                 0 : 0,
                }
            # Supposedly negligble compared to scale
            type_info['pdf']['bbH4f'] = {
                -1 : 0,
                +1 : 0,
                 0 : 0,
            }
        ggF_alphasdown = self.lookup_value(mA, tan_beta, 'h_ggF_alphasdown_%s' % type)
        ggF_pdfdown = self.lookup_value(mA, tan_beta, 'h_ggF_pdfdown_%s' % type)

        ggF_alphasup = self.lookup_value(mA, tan_beta, 'h_ggF_alphasup_%s' % type)
        ggF_pdfup = self.lookup_value(mA, tan_beta, 'h_ggF_pdfup_%s' % type)

        type_info['pdf']['ggF'] = {
            -1 : mssm_xsec_tools._add_in_quadrature(ggF_alphasdown, ggF_pdfdown)*self.unit_pb,
            +1 : mssm_xsec_tools._add_in_quadrature(ggF_alphasup, ggF_pdfup)*self.unit_pb,
             0 : 0,
        }

    def query(self, mA, tan_beta):

        higgs_types = [ 'h', 'A', 'H' ]
        
        # Build emtpy dictionaries for each Higgs type
        output = {
            'mA' : mA,
            'tan_beta' : tan_beta,
            'higgses' : {
                'h' : {},
                'A' : {},
                'H' : {}
            }
        }

        for higgs_type in higgs_types:
            self._add_br_htt(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_hmm(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_br_hbb(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_mass(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_xsec(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_mu(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_pdf(mA, tan_beta, (higgs_type, output['higgses'][higgs_type]))
            self._add_santander((higgs_type, output['higgses'][higgs_type]))
        
        return output
