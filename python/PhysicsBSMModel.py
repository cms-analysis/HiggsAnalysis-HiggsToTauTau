## --------------------------------------------------------------------------------------------------------------------------------------------------
##
## This is a first toy version of a physics model t play around with bbH-ggH fits. The best way to use it at the moment would be to run it in the
## points of the observed limits (in the current implementation), of to leave any further multiplication by MSSM cross section out and to run it
## resulting in a model independent cross section limit. This would be even simpler, no multiplication by MSSM xsec were be necessary. Also tanb
## could be left floating in principle, but this is only manageable in a degenerate mass scheme.
##
## How to use this little toy:
##
## text2workspace.py htt_cmb_7TeV-400.txt -m 400 -P HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:floatingMSSMXSHiggs --PO modes=ggH,bbH --PO tanb=30
## combine -M MultiDimFit htt_cmb_7TeV-400.root --robustFit 1 --algo=singles --cl=0.68
##
## --------------------------------------------------------------------------------------------------------------------------------------------------

import os

from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel 
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools

class MSSMLikeHiggsModel(PhysicsModel):
    def getHiggsSignalYieldScale(self, production, decay, energy):
            raise RuntimeError, "Not implemented"
    def getYieldScale(self,bin,process):
        """
        split in production and decay channels; call getHiggsSignalYieldScale; return 1 for backgrounds
        """
        if not self.DC.isSignal[process]: return 1
        processSource = process
        decaySource   = self.options.fileName+":"+bin # by default, decay comes from the datacard name or bin label
        if "_" in process: (processSource, decaySource) = process.split("_")
        if processSource not in ["ggH", "bbH" ]:
            raise RuntimeError, "Validation Error: signal process %s not among the allowed ones." % processSource
        foundDecay = None
        for D in [ "hbb", "htt", "hmm" ]:
            if D in decaySource:
                if foundDecay: raise RuntimeError, "Validation Error: decay string %s contains multiple known decay names" % decaySource
                foundDecay = D
        if not foundDecay: raise RuntimeError, "Validation Error: decay string %s does not contain any known decay name" % decaySource
        foundEnergy = None
        for D in [ "7TeV", "8TeV" ]:
            if D in decaySource:
                if foundEnergy: raise RuntimeError, "Validation Error: decay string %s contains multiple known energies" % decaySource
                foundEnergy = D
        if not foundEnergy:
            foundEnergy = "7TeV" ## To ensure backward compatibility
            print "Warning: decay string %s does not contain any known energy, assuming %s" % (decaySource, foundEnergy)
        return self.getHiggsSignalYieldScale(processSource, foundDecay, foundEnergy)

class FloatingMSSMXSHiggs(MSSMLikeHiggsModel):
    """
    float ggH and bbH independently
    """
    def __init__(self):
        MSSMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.tanb = None
        self.modes = [ "ggH", "bbH" ]
        self.mARange = []
    def setPhysicsOptions(self,physOptions):
        """
        options are: tanb, modes, mARange
        """
        for po in physOptions:
            if po.startswith("tanb="): self.tanb = po.replace("tanb=", "")
            if po.startswith("modes="): self.modes = po.replace("modes=","").split(",")
            if po.startswith("mARange="):
                self.mARange = po.replace("mARange=","").split(":")
                if len(self.mARange) != 2:
                    raise RuntimeError, "Definition of mA range requires two extrema, separated by ':'"
                elif float(self.mARange[0]) >= float(self.mARange[1]):
                    raise RuntimeError, "Extrema for mA range defined with inverterd order. Second element must be larger than first element"
    def doParametersOfInterest(self):
        """
        create POI and other parameters, and define the POI set. Evaluate cross section for given values of mA and tanb
        """
        # --- Evaluate Cross Sections for given values of tanb and mA ---
        mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH="HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-7TeV-nnlo.root"))
        mssm_xsec = mssm_scan.query(self.options.mass, float(self.tanb))
        self.modelBuilder.doVar("bbH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['santander']*mssm_xsec['higgses']['A']['BR']))
        self.modelBuilder.doVar("ggH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['ggF'      ]*mssm_xsec['higgses']['A']['BR']))
        # --- Signal Strength as only POI --- 
        if "ggH" in self.modes: self.modelBuilder.doVar("r_ggH[1,0,20]");
        if "bbH" in self.modes: self.modelBuilder.doVar("r_bbH[1,0,20]");
        poi = ",".join(["r_"+m for m in self.modes])
        # --- Higgs Mass as other parameter ----
        if self.modelBuilder.out.var("MH"):
            if len(self.mHRange):
                print 'MH will be left floating within', self.mARange[0], 'and', self.mARange[1]
                self.modelBuilder.out.var("MH").setRange(float(self.mARange[0]),float(self.mARange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
                poi+=',MH'
            else:
                print 'MH will be assumed to be', self.options.mass
                self.modelBuilder.out.var("MH").removeRange()
                self.modelBuilder.out.var("MH").setVal(self.options.mass)
        else:
            if len(self.mARange):
                print 'MH will be left floating within', self.mARange[0], 'and', self.mARange[1]
                self.modelBuilder.doVar("MH[%s,%s]" % (self.mARange[0],self.mARange[1]))
                poi+=',MH'
            else:
                print 'MH (not there before) will be assumed to be', self.options.mass
                self.modelBuilder.doVar("MH[%g]" % self.options.mass)
        ## define set of POIs
        self.modelBuilder.doSet("POI",poi)
    def getHiggsSignalYieldScale(self,production,decay, energy):
        if production == "ggH" or production == "bbH":
            self.modelBuilder.factory_('expr::%s_yield("@0*@1", r_%s, %s_xsec)' % (production, production, production))
            return "%s_yield" % production
        #if production == "bbH": return ("r_bbH" if "bbH" in self.modes else 1)
        #if production == "qqH": return ("r_qqH" if "qqH" in self.modes else 1)
        #if production == "ttH": return ("r_ttH" if "ttH" in self.modes else 1)
        #if production in [ "WH", "ZH", "VH" ]: return ("r_VH" if "VH" in self.modes else 1)
        raise RuntimeError, "Unknown production mode '%s'" % production

floatingMSSMXSHiggs = FloatingMSSMXSHiggs()
