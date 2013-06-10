import ROOT
import os

class feyn_higgs_mssm:
    """
    Class for determination of masses, crosssections and branchingratios for a given higgs model.
    Arguments are mA, tanb and model, with model being 'sm', 'mssm'.
    """
    def __init__(self, mA, tanb, model):
        self.mA = mA
        self.tanb = tanb
        self.model = model
        fmodel = 'mhmax-7TeV'
        path = os.getenv("CMSSW_BASE")+'/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-'+fmodel+'-fine.root'
        if tanb < 10:
            self.scan = feyn_higgs_scan(path, "mssm_scan", 90, 1, 10, 96, 50, 1010) 
        else:
            self.scan = feyn_higgs_scan(path, "mssm_scan", 70, 1, 71, 96, 50, 1010)
        self.mh = self.scan.mass("mh", self.mA, self.tanb)
        self.mH = self.scan.mass("mH", self.mA, self.tanb)
    def get_mh(self):
        return self.mh
    def get_mH(self):
        return self.mH
    def get_xs(self, channel):
        " return xs for a given channel "
        xs = self.scan.get(channel, self.model, "xs",  self.mA, self.tanb)
        return xs
    def get_br(self, channel):
        " return br for a given channel "
        br = self.scan.get(channel, self.model, "br",  self.mA, self.tanb)
        return br

class feyn_higgs_scan:
    def __init__(self, filename, treename, ntanb, mintanb, maxtanb, nmA, minmA, maxmA):
        self.mintanb = mintanb
        self.maxtanb = maxtanb
        self.steptanb = (maxtanb-mintanb)/float(ntanb)
        self.minmA = minmA
        self.maxmA = maxmA
        self.stepmA = (maxmA-minmA)/float(nmA)
        self.hproject = ROOT.TH2F("hproject", "hproject", nmA, minmA, maxmA, ntanb, mintanb, maxtanb)
        self.file = ROOT.TFile(filename, 'read')
        if self.file.IsZombie():
            print "Error: Could not open file"
        self.tree = self.file.Get(treename)

    def project(self, var):
        self.hproject.Reset()
        for idx in range(0, self.tree.GetEntries()):
            self.tree.GetEvent(idx)
            self.hproject.Fill(self.tree.mA + self.stepmA/2., self.tree.tanb+self.steptanb/2., getattr(self.tree,var))

    def mass(self, var, mA, tanb):
        """ Extraction of mass from TTree """
        mass = 0.
        for idx in range(0,self.tree.GetEntries()):
            self.tree.GetEvent(idx)
            if self.tree.mA == mA and self.tree.tanb == tanb:
                mass = getattr(self.tree,var)
                break
        return mass

    def get(self, variable, model, type, mA, tanb):
        """ extract value of 'variable' from rootfiles """
        self.project(type+'_'+model+'_'+variable)
        if self.minmA <= mA and mA < self.maxmA and self.mintanb <= tanb and tanb < self.maxtanb:
            return self.hproject.GetBinContent(self.hproject.FindBin(mA, tanb))
        else:
            return -999
        
