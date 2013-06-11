import ROOT
import os

class feyn_higgs_mssm:
    """
    Description:
    Class for determination of masses, cross-sections and branchingratios for a given higgs model.
    Arguments are mA, tanb, model, fmodel and period
      - model is from  'sm', 'mssm'.
      - fmodel is from 'mhmax', 'gluph', 'saeff'
      - period is from '7TeV', '8TeV'
    Allowed channels for get_xs are gg[h,H,A], qq[h,H,A]
    Allowed channels for get_br are [h,H,A]tt, [h,H,A]mm, [h,H,A]bb
    """
    def __init__(self, mA, tanb, model, fmodel, period):
        self.mA = mA
        self.tanb = tanb
        self.model = model
        if fmodel == '':
            fmodel = 'mhmax'
        path = os.getenv("CMSSW_BASE")+'/src/HiggsAnalysis/HiggsToTauTau/data/feyn-higgs-mssm-scan-'+fmodel+'-'+period
        if self.tanb < 10:
            self.scan = feyn_higgs_scan(path+'-fine.root', "mssm_scan", 90, 1, 10, 96, 50, 1010) 
        else:
            self.scan = feyn_higgs_scan(path+'.root', "mssm_scan", 70, 1, 71, 96, 50, 1010)
    def get_mh(self):
        mh = self.scan.mass("mh", self.mA, self.tanb)
        return mh
    def get_mH(self):
        mH = self.scan.mass("mH", self.mA, self.tanb)
        return mH
    def get_xs(self, channel):
        """
        This function returns the cross-section for a given production-channel.
        """
        xs = self.scan.get(channel, self.model, "xs",  self.mA, self.tanb)
        return xs
    def get_br(self, channel):
        """
        This function returns the branchingratio for a given decay-channel.
        """
        br = self.scan.get(channel, self.model, "br",  self.mA, self.tanb)
        return br

class feyn_higgs_scan:
    """
    Description:

    Basic class to determine branchingratios, cross-sections and masses of higgses.
    As input it takes the name of the rootfile and the TTree to be used as well as the
    parameters for the tanb and mA range.
    """
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
        
