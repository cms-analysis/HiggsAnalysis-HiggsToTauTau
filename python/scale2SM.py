import os
import re

class RescaleSamples:
    def __init__(self, input_file, production_channels, masspoints) :
        ## name of the input file
        self.input_file = input_file
        ## list of mass points to be scaled
        self.masses = masspoints
        ## list of signal channels to be scaled
        self.production_channels = production_channels
        if '/' in input_file :
            input_file = input_file[input_file.rfind('/')+1:]
        matcher = re.compile('v?htt_?\w*.inputs-\w*-(?P<PERIOD>[0-9]*\w*)(-?_?\w*)*.root')
        ecms_str = matcher.match(input_file).group('PERIOD')
        ecms_str = ecms_str[:ecms_str.find('TeV')]
        self.ecms = float(ecms_str)
        
    def xsec(self, production_channel, mass) :
        """
        Loads SM cross sections needed to rescale the input histograms. Returns
        the cross section in pb
        """
        xs = 0
        if production_channel == "VH" :
            production_channel = "WH+ZH"
        if production_channel == "VH_hww" :
            production_channel = "WH+ZH"            
        if production_channel == "VH+" :
            production_channel = "WH+ZH_ttH"
        if production_channel == "SM" :
            production_channel = "ggH"
        if production_channel == "ggH_hww" :
            production_channel = "ggH"
        if production_channel == "VBF" :
            production_channel = "qqH"
        if production_channel == "qqH_hww" :
            production_channel = "qqH"
        if production_channel == 'bbH' :
            ## not yet available
            return xs
        if production_channel.find('+')>-1 :
            sub_channels = production_channel.split('+')
            for sub_channel in sub_channels :
                xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                    CHANNEL=sub_channel, MA=mass, ECMS=self.ecms)).read().split()[2])
        else :
#            print "xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(CHANNEL=production_channel, MA=mass, ECMS=self.ecms)
            xs += float(os.popen("xsec-sm {CHANNEL} {MA} {ECMS} | grep value".format(
                CHANNEL=production_channel, MA=mass, ECMS=self.ecms)).read().split()[2])
        return xs

    def BR(self, mass) :
        """
        Loads SM branching ratios needed to rescale the input histograms. 
        """
        return float(os.popen("xsec-sm BR {MA} | grep value".format(MA=mass)).read().split()[2])

    def rescale(self) :
        """
        Rescales histograms according to productiohn channel, decay channel and mass. The rescaling
        is done using the macro rescalSignal.C in the macros directory of the package. This does take
        automatic care of scaling histograms for signal (central value) and shape uncertainties.
        """
        for production_channel in self.production_channels :
            for mass in self.masses :
                ## determine cross section
                xs = self.xsec(production_channel, mass)
                ## determine BR
                br = self.BR(mass)
                ## determine search pattern for mass re-scaling
                pattern = production_channel+mass
                ## run the rescaling
                os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{SCALE},\"{INPUTFILE}\",\"{PROCESS}\",0\)".format(
                    CMSSW_BASE=os.environ.get("CMSSW_BASE"), SCALE=xs*br, INPUTFILE=self.input_file, PROCESS=pattern))
