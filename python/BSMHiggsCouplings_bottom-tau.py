from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
from HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel import MSSMLikeHiggsModel #PhysicsBSMModel 
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools ##not needed atm
import ROOT, os

## this is a first try for some model in mssm which allows in a model independent way the combination of hbb and htt
## i believe there must be a normalization to something in order to define the contribution of hbb and htt

class CbCtauMSSMHiggs(MSSMLikeHiggsModel):
    "assume the MSSM coupling but let the Higgs mass to float"
    def __init__(self):
        MSSMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.floatMass = False
        #self.mARange  = []
        self.tanb   = 30
        self.cbRange = ['-2','2']
        self.ctauRange = ['-2','2']
        
    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.floatMass = True
                self.mARange = po.replace("higgsMassRange=","").split(",")
                print 'The Higgs mass range:', self.mARange
                if len(self.mARange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema."
                elif float(self.mARange[0]) >= float(self.mARange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first."
            if po.startswith("cbRange="):
                self.cbRange = po.replace("cbRange=","").split(":")
                if len(self.cbRange) != 2:
                    raise RuntimeError, "cb signal strength range requires minimal and maximal value"
                elif float(self.cbRange[0]) >= float(self.cbRange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"
            if po.startswith("ctauRange="):
                self.ctauRange = po.replace("ctauRange=","").split(":")
                if len(self.ctauRange) != 2:
                    raise RuntimeError, "ctau signal strength range requires minimal and maximal value"
                elif float(self.ctauRange[0]) >= float(self.ctauRange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"
    def doParametersOfInterest(self):
        """Create POI out of signal strength and MH"""
        # --- Signal Strength as only POI --- 
        self.modelBuilder.doVar("Cb[1,%s,%s]" % (self.cbRange[0], self.cbRange[1]))
        self.modelBuilder.doVar("Ctau[1,%s,%s]" % (self.ctauRange[0], self.ctauRange[1]))

        if self.floatMass:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setRange(float(self.mARange[0]),float(self.mARange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
            else:
                self.modelBuilder.doVar("MH[%s,%s]" % (self.mARange[0],self.mARange[1])) 
            self.modelBuilder.doSet("POI",'Cb,Ctau,MH')
        else:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setVal(self.options.mass)
                self.modelBuilder.out.var("MH").setConstant(True)
            else:
                self.modelBuilder.doVar("MH[%g]" % self.options.mass) 
            self.modelBuilder.doSet("POI",'Cb,Ctau')
        self.setup()
        
    def setup(self):
        self.decayScaling = {
            'htt':'htautau',
            'hbb':'hbb',
            }
        self.productionScaling = {
            'ggH':'Cb',
            'bbH':'Cb',
            }
        ## get xs and br for MSSM mhmax scenario
##         tanbintervall = "tanbHigh" if self.tanb>=1.0 else "tanbLow"
##         decaySource   = self.options.fileName # by default, energy comes from the datacard name
##         foundDecay = None
##         br=""
##         for D in [ "hbb", "htt", "hmm" ]:
##             if D in decaySource:
##                 if D=="hbb" :
##                     br="BR-bb"
##                 elif D=="htt" :
##                     br="BR"
##                 elif D=="hmm" :
##                     br="BR-mumu"               
##                 if foundDecay: raise RuntimeError, "Validation Error: decay string %s contains multiple known decay names" % decaySource
##                 foundDecay = D
##         if not foundDecay: raise RuntimeError, "Validation Error: decay string %s does not contain any known decay name" % decaySource
##         foundEnergy = None
##         for D in [ "7TeV", "8TeV" ]:
##             if D in decaySource:
##                 if foundEnergy: raise RuntimeError, "Validation Error: decay string %s contains multiple known energies" % decaySource
##                 foundEnergy = D
##         if not foundEnergy:
##             foundEnergy = "7TeV" ## To ensure backward compatibility
##             print "Warning: decay string %s does not contain any known energy, assuming %s" % (decaySource, foundEnergy)
##         path="HiggsAnalysis/HiggsToTauTau/data/out.mhmax-mu+200-{ECMS}-{TANBINTERVALL}-nnlo.root".format(ECMS=foundEnergy, TANBINTERVALL=tanbintervall)
##         mssm_scan = mssm_xsec_tools("{CMSSW_BASE}/src/{PATH}".format(CMSSW_BASE=os.environ['CMSSW_BASE'], PATH=path))
##         mssm_xsec = mssm_scan.query(self.options.mass, float(self.tanb))
##         self.modelBuilder.doVar("bbH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['santander']*mssm_xsec['higgses']['A'][br]))
##         self.modelBuilder.doVar("ggH_xsec[%g]" % (mssm_xsec['higgses']['A']['xsec']['ggF'      ]*mssm_xsec['higgses']['A'][br]))
        
        ##partial widths, not normalized, for decays scaling with b, tau and total
        self.modelBuilder.factory_('expr::CbCtau_Gscal_sumb("@0*@0", Cb)') 
        self.modelBuilder.factory_('expr::CbCtau_Gscal_sumtau("@0*@0", Ctau)') 
        self.modelBuilder.factory_('sum::CbCtau_Gscal_tot(CbCtau_Gscal_sumb, CbCtau_Gscal_sumtau)')
        ## BRs, not normalized: they scale as (coupling)^2 / (totWidth)^2 
        self.modelBuilder.factory_('expr::CbCtau_BRscal_hbb("@0*@0/@1", Cb, CbCtau_Gscal_tot)')
        self.modelBuilder.factory_('expr::CbCtau_BRscal_htautau("@0*@0/@1", Ctau, CbCtau_Gscal_tot)')
        
        self.modelBuilder.out.Print()
    def getHiggsSignalYieldScale(self,production,decay,energy):

        name = "CbCtau_XSBRscal_%s_%s" % (production,decay)
        if self.modelBuilder.out.function(name):
            return name
        
        XSscal = self.productionScaling[production]
        BRscal = self.decayScaling[decay]
        self.modelBuilder.factory_('expr::%s("@0*@0 * @1", %s, CbCtau_BRscal_%s)' % (name, XSscal, BRscal))
        return name

## class CvCfXgHiggs(SMLikeHiggsModel):
##     "assume the SM coupling but let the Higgs mass to float"
##     def __init__(self):
##         SMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
##         self.floatMass = False
##     def setPhysicsOptions(self,physOptions):
##         for po in physOptions:
##             if po.startswith("higgsMassRange="):
##                 self.floatMass = True
##                 self.mHRange = po.replace("higgsMassRange=","").split(",")
##                 print 'The Higgs mass range:', self.mHRange
##                 if len(self.mHRange) != 2:
##                     raise RuntimeError, "Higgs mass range definition requires two extrema."
##                 elif float(self.mHRange[0]) >= float(self.mHRange[1]):
##                     raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first."
##     def doParametersOfInterest(self):
##         """Create POI out of signal strength and MH"""
##         # --- Signal Strength as only POI --- 
##         self.modelBuilder.doVar("CV[1,0.0,1.5]")
##         self.modelBuilder.doVar("CF[1,-1.5,1.5]")
##         self.modelBuilder.doVar("XG[0,-4,4]")
##         if self.floatMass:
##             if self.modelBuilder.out.var("MH"):
##                 self.modelBuilder.out.var("MH").setRange(float(self.mHRange[0]),float(self.mHRange[1]))
##                 self.modelBuilder.out.var("MH").setConstant(False)
##             else:
##                 self.modelBuilder.doVar("MH[%s,%s]" % (self.mHRange[0],self.mHRange[1])) 
##             self.modelBuilder.doSet("POI",'CV,CF,XG,MH')
##         else:
##             if self.modelBuilder.out.var("MH"):
##                 self.modelBuilder.out.var("MH").setVal(self.options.mass)
##                 self.modelBuilder.out.var("MH").setConstant(True)
##             else:
##                 self.modelBuilder.doVar("MH[%g]" % self.options.mass) 
##             self.modelBuilder.doSet("POI",'CV,CF,XG')
##         self.SMH = SMHiggsBuilder(self.modelBuilder)
##         self.setup()
##     def setup(self):
##         ## Add some common ingredients
##         datadir = os.environ['CMSSW_BASE']+'/src/HiggsAnalysis/CombinedLimit/data/lhc-hxswg'
##         self.SMH.textToSpline( 'mb', os.path.join(datadir, 'running_constants.txt'), ycol=2 );
##         mb = self.modelBuilder.out.function('mb')
##         mH = self.modelBuilder.out.var('MH')
##         CF = self.modelBuilder.out.var('CF')
##         CV = self.modelBuilder.out.var('CV')
##         XG = self.modelBuilder.out.var('XG')

##         RHggCvCfXg = ROOT.RooScaleHGamGamLOSMPlusX('CvCfXg_cgammaSq', 'LO SM Hgamgam scaling', mH, CF, CV, mb, CF, XG)
##         self.modelBuilder.out._import(RHggCvCfXg)
##         #Rgluglu = ROOT.RooScaleHGluGluLOSMPlusX('Rgluglu', 'LO SM Hgluglu scaling', mH, CF, mb, CF)
##         #self.modelBuilder.out._import(Rgluglu)
        
##         ## partial witdhs, normalized to the SM one, for decays scaling with F, V and total
##         for d in [ "htt", "hbb", "hcc", "hww", "hzz", "hgluglu", "htoptop", "hgg", "hZg", "hmm", "hss" ]:
##             self.SMH.makeBR(d)
##         self.modelBuilder.factory_('expr::CvCfXg_Gscal_sumf("@0*@0 * (@1+@2+@3+@4+@5+@6+@7)", CF, SM_BR_hbb, SM_BR_htt, SM_BR_hcc, SM_BR_htoptop, SM_BR_hgluglu, SM_BR_hmm, SM_BR_hss)') 
##         self.modelBuilder.factory_('expr::CvCfXg_Gscal_sumv("@0*@0 * (@1+@2+@3)", CV, SM_BR_hww, SM_BR_hzz, SM_BR_hZg)') 
##         self.modelBuilder.factory_('expr::CvCfXg_Gscal_gg("@0 * @1", CvCfXg_cgammaSq, SM_BR_hgg)') 
##         self.modelBuilder.factory_('sum::CvCfXg_Gscal_tot(CvCfXg_Gscal_sumf, CvCfXg_Gscal_sumv, CvCfXg_Gscal_gg)')
##         ## BRs, normalized to the SM ones: they scale as (coupling/coupling_SM)^2 / (totWidth/totWidthSM)^2 
##         self.modelBuilder.factory_('expr::CvCfXg_BRscal_hgg("@0/@1", CvCfXg_cgammaSq, CvCfXg_Gscal_tot)')
##         self.modelBuilder.factory_('expr::CvCfXg_BRscal_hf("@0*@0/@1", CF, CvCfXg_Gscal_tot)')
##         self.modelBuilder.factory_('expr::CvCfXg_BRscal_hv("@0*@0/@1", CV, CvCfXg_Gscal_tot)')
        
##         self.modelBuilder.out.Print()
##     def getHiggsSignalYieldScale(self,production,decay,energy):
##         name = "CvCfXg_XSBRscal_%s_%s" % (production,decay)
##         if self.modelBuilder.out.function(name) == None: 
##             XSscal = 'CF' if production in ["ggH","ttH"] else 'CV'
##             BRscal = "hgg"
##             if decay in ["hww", "hzz"]: BRscal = "hv"
##             if decay in ["hbb", "htt"]: BRscal = "hf"
##             self.modelBuilder.factory_('expr::%s("@0*@0 * @1", %s, CvCfXg_BRscal_%s)' % (name, XSscal, BRscal))
##         return name


## this is the entry point for text2workspace.py
CbCtauMSSMHiggs = CbCtauMSSMHiggs()
