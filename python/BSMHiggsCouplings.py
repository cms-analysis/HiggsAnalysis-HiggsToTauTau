from HiggsAnalysis.CombinedLimit.PhysicsModel import PhysicsModel
from HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel import MSSMLikeHiggsModel #PhysicsBSMModel
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools ##not needed atm
import ROOT, os

## this is a first try for some model in mssm which allows in a model independent way the combination of hbb and htt
## i believe there must be a normalization to something in order to define the contribution of hbb and htt

class CbCtauMSSMHiggs(MSSMLikeHiggsModel):
    "testing Cb and Ctau. MH is fixed for now. In ggH loop assume SM for all but Cb. Everything normalized to SM."
    
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
        self.SMH = SMHiggsBuilder(self.modelBuilder)
        self.setup()

        
    def setup(self):
        self.decayScaling = {
            'htt':'htautau',
            'hbb':'hbb',
            }
        self.productionScaling = {
            'bbH':'Cb',
            }       
        # scalings of the loops
      ##   self.BSMscaling('ggH', Cb='Cb', Ctau='Ctau')
##         self.BSMscaling('hgg', Cb='Cb', Ctau='Ctau')
##         self.BSMscaling('hzg', Cb='Cb', Ctau='Ctau')
        self.SMH.makeScaling('ggH', Cb='Cb', Ctop='1')
        self.SMH.makeScaling('hgg', Cb='Cb', Ctop='1', CW='1', Ctau='Ctau')
        self.SMH.makeScaling('hzg', Cb='Cb', Ctop='1', CW='1', Ctau='Ctau')

        ##partial widths, normalized to SM, for decays scaling with b, tau and total
        for d in [ "htt", "hbb", "hcc", "hww", "hzz", "hgluglu", "htoptop", "hgg", "hzg", "hmm", "hss"]:
            self.SMH.makeBR(d)
        self.modelBuilder.factory_('expr::CbCtau_Gscal_sumb("@0*@0 * @1", Cb, SM_BR_hbb)') 
        self.modelBuilder.factory_('expr::CbCtau_Gscal_sumtau("@0*@0 * @1", Ctau, SM_BR_htt)')
        self.modelBuilder.factory_('expr::CbCtau_Gscal_gg("@0 * @1", Scaling_hgg, SM_BR_hgg)') 
        self.modelBuilder.factory_('expr::CbCtau_Gscal_Zg("@0 * @1", Scaling_hzg, SM_BR_hzg)')
        self.modelBuilder.factory_('sum::CbCtau_Gscal_tot(CbCtau_Gscal_sumb, CbCtau_Gscal_sumtau, CbCtau_Gscal_gg, CbCtau_Gscal_Zg, SM_BR_hcc, SM_BR_htoptop, SM_BR_hgluglu, SM_BR_hmm, SM_BR_hss, SM_BR_hww, SM_BR_hzz)')
        ## BRs, normalized to SM: they scale as (coupling/partial_SM)^2 / (totWidth/total_SM)^2 
        self.modelBuilder.factory_('expr::CbCtau_BRscal_hbb("@0*@0/@1", Cb, CbCtau_Gscal_tot)')
        self.modelBuilder.factory_('expr::CbCtau_BRscal_htautau("@0*@0/@1", Ctau, CbCtau_Gscal_tot)')       
        self.modelBuilder.out.Print()

        
    def getHiggsSignalYieldScale(self,production,decay,energy):

        #print production, decay, energy 
        name = "CbCtau_XSBRscal_%s_%s" % (production,decay)
        
        #Special case that depends on Energy
        if production == 'ggH':
            self.productionScaling[production] = 'Scaling_ggH_' + energy
            name += '_%(energy)s' % locals()

        if self.modelBuilder.out.function(name):
            #print "name", name
            return name
        
        XSscal = self.productionScaling[production]
        BRscal = self.decayScaling[decay]
        self.modelBuilder.factory_('expr::%s("@0*@0 * @1", %s, CbCtau_BRscal_%s)' % (name, XSscal, BRscal))
        #print "name", name
        return name



###more classes

class ClCqMSSMHiggs(MSSMLikeHiggsModel):
    "testing Cl and Cq. MH is fixed for now. Everything normalized to SM."
    
    def __init__(self):
        MSSMLikeHiggsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.floatMass = False
        #self.mARange  = []
        self.tanb   = 30
        self.clRange = ['-2','2']
        self.cqRange = ['-2','2']

        
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
            if po.startswith("clRange="):
                self.clRange = po.replace("clRange=","").split(":")
                if len(self.clRange) != 2:
                    raise RuntimeError, "cl signal strength range requires minimal and maximal value"
                elif float(self.clRange[0]) >= float(self.clRange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"
            if po.startswith("cqRange="):
                self.cqRange = po.replace("cqRange=","").split(":")
                if len(self.cqRange) != 2:
                    raise RuntimeError, "cq signal strength range requires minimal and maximal value"
                elif float(self.cqRange[0]) >= float(self.cqRange[1]):
                    raise RuntimeError, "minimal and maximal range swapped. Second value must be larger first one"

                
    def doParametersOfInterest(self):
        """Create POI out of signal strength and MH"""
        # --- Signal Strength as only POI --- 
        self.modelBuilder.doVar("Cl[1,%s,%s]" % (self.clRange[0], self.clRange[1]))
        self.modelBuilder.doVar("Cq[1,%s,%s]" % (self.cqRange[0], self.cqRange[1]))

        if self.floatMass:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setRange(float(self.mARange[0]),float(self.mARange[1]))
                self.modelBuilder.out.var("MH").setConstant(False)
            else:
                self.modelBuilder.doVar("MH[%s,%s]" % (self.mARange[0],self.mARange[1])) 
            self.modelBuilder.doSet("POI",'Cl,Cq,MH')
        else:
            if self.modelBuilder.out.var("MH"):
                self.modelBuilder.out.var("MH").setVal(self.options.mass)
                self.modelBuilder.out.var("MH").setConstant(True)
            else:
                self.modelBuilder.doVar("MH[%g]" % self.options.mass) 
            self.modelBuilder.doSet("POI",'Cl,Cq')
        self.SMH = SMHiggsBuilder(self.modelBuilder)
        self.setup()

        
  ##   def setup(self):
##         self.decayScaling = {
##             'htt':'htautau',
##             'hbb':'hbb',
##             'hmm':'hmm',
##             }
##         self.productionScaling = {
##             'bbH':'Cq',
##             'ggH':'Cq',
##             }       
##         # scalings of the loops
##         self.SMH.makeScaling('hgg', Cb='Cq', Ctop='Cq', CW='1', Ctau='Cl')
##         self.SMH.makeScaling('hzg', Cb='Cq', Ctop='Cq', CW='1', Ctau='Cl')

##         ##partial widths, normalized to SM, for decays scaling with b, tau and total
##         for d in [ "htt", "hbb", "hcc", "hww", "hzz", "hgluglu", "htoptop", "hgg", "hzg", "hmm", "hss"]:
##             self.SMH.makeBR(d)
##         self.modelBuilder.factory_('expr::ClCq_Gscal_sumq("@0*@0 * (@1+@2+@3+@4+@5+@6+@7)", Cq, SM_BR_hbb, SM_BR_hcc, SM_BR_htoptop, SM_BR_hss)') 
##         self.modelBuilder.factory_('expr::ClCq_Gscal_suml("@0*@0 * @1", Cl, SM_BR_htt, SM_BR_hmm)')
##         self.modelBuilder.factory_('expr::ClCq_Gscal_gg("@0 * @1", Scaling_hgg, SM_BR_hgg)') 
##         self.modelBuilder.factory_('expr::ClCq_Gscal_Zg("@0 * @1", Scaling_hzg, SM_BR_hzg)')
##         self.modelBuilder.factory_('sum::ClCq_Gscal_tot(ClCq_Gscal_sumq, ClCq_Gscal_suml, ClCq_Gscal_gg, ClCq_Gscal_Zg, SM_BR_hgluglu, SM_BR_hww, SM_BR_hzz)')
##         ## BRs, normalized to SM: they scale as (coupling/partial_SM)^2 / (totWidth/total_SM)^2 - only used datacards needed
##         self.modelBuilder.factory_('expr::ClCq_BRscal_hbb("@0*@0/@1", Cq, ClCq_Gscal_tot)')
##         self.modelBuilder.factory_('expr::ClCq_BRscal_hmm("@0*@0/@1", Cl, ClCq_Gscal_tot)')
##         self.modelBuilder.factory_('expr::ClCq_BRscal_htautau("@0*@0/@1", Cl, ClCq_Gscal_tot)')       
##         self.modelBuilder.out.Print()

    def setup(self): ##not normalized to SM = no assumptions on total width
        self.decayScaling = {
            'htt':'htautau',
            'hbb':'hbb',
            'hmm':'hmm',
            }
        self.productionScaling = {
            'bbH':'Cq',
            'ggH':'Cq',
            }       

        ##partial widths, normalized to SM, for decays scaling with b, tau and total
        ## BRs, normalized to SM: they scale as (coupling/partial_SM)^2 / (totWidth/total_SM)^2 - only used datacards needed
        self.modelBuilder.factory_('expr::ClCq_BRscal_hbb("@0*@0", Cq)')
        self.modelBuilder.factory_('expr::ClCq_BRscal_hmm("@0*@0", Cl)')
        self.modelBuilder.factory_('expr::ClCq_BRscal_htautau("@0*@0", Cl)')       
        self.modelBuilder.out.Print()

        
    def getHiggsSignalYieldScale(self,production,decay,energy):

        #print production, decay, energy 
        name = "ClCq_XSBRscal_%s_%s" % (production,decay)

        if self.modelBuilder.out.function(name):
            #print "name", name
            return name
        
        XSscal = self.productionScaling[production]
        BRscal = self.decayScaling[decay]
        self.modelBuilder.factory_('expr::%s("@0*@0 * @1", %s, ClCq_BRscal_%s)' % (name, XSscal, BRscal))
        #print "name", name
        return name






    
  ##   def BSMscaling(self,what, Cb='Cb', Ctau='Ctau'):
##         prefix = 'SM_%(what)s_' % locals()
##         if  what == 'ggH':
##             structure = {'sigma_tt':2, 'sigma_bb':3, 'sigma_tb':4}
##             for sqrts in ('7TeV', '8TeV'):
##                 for qty, column in structure.iteritems():
##                     rooName = prefix+qty+'_'+sqrts
##                     self.SMH.textToSpline(rooName, os.path.join(self.SMH.coupPath, 'ggH_%(sqrts)s.txt'%locals()), ycol=column )
##                 scalingName = 'Scaling_'+what+'_'+sqrts
##                 #print 'Building '+scalingName
##                 rooExpr = 'expr::%(scalingName)s(\
## "(1*1)*@1  + (@0*@0)*@2 + (1*@0)*@3",\
##  %(Cb)s,\
##  %(prefix)ssigma_tt_%(sqrts)s, %(prefix)ssigma_bb_%(sqrts)s, %(prefix)ssigma_tb_%(sqrts)s\
## )'%locals()
##                 #print  rooExpr
##                 self.modelBuilder.factory_(rooExpr)
##         elif what in ['hgg', 'hzg']:
##             fileFor = {'hgg':'Gamma_Hgammagamma.txt',
##                        'hzg':'Gamma_HZgamma.txt'}
##             structure = {'Gamma_tt':2, 'Gamma_bb':3, 'Gamma_WW':4,
##                          'Gamma_tb':5, 'Gamma_tW':6, 'Gamma_bW':7,
##                          'Gamma_ll':8,
##                          'Gamma_tl':9, 'Gamma_bl':10, 'Gamma_lW':11}
##             for qty, column in structure.iteritems():
##                 rooName = prefix+qty
##                 self.SMH.textToSpline(rooName, os.path.join(self.SMH.coupPath, fileFor[what]), ycol=column )
##             scalingName = 'Scaling_'+what
## #            print 'Building '+scalingName
##             rooExpr = 'expr::%(scalingName)s(\
## "(1*1)*@2  + (@0*@0)*@3 + (1*1)*@4 + (1*@0)*@5 + (1*1)*@6 + (@0*1)*@7 + (@1*@1)*@8 + (1*@1)*@9 + (@0*@1)*@10 + (1*@1)*@11",\
##  %(Cb)s, %(Ctau)s,\
##  %(prefix)sGamma_tt, %(prefix)sGamma_bb, %(prefix)sGamma_WW,\
##  %(prefix)sGamma_tb, %(prefix)sGamma_tW, %(prefix)sGamma_bW,\
##  %(prefix)sGamma_ll,\
##  %(prefix)sGamma_tl, %(prefix)sGamma_bl, %(prefix)sGamma_lW\
## )'%locals()
## #            print  rooExpr
##             self.modelBuilder.factory_(rooExpr)
##         else:
##             raise RuntimeError, "There is no scaling defined for %(what)s" % locals()










## this is the entry point for text2workspace.py
CbCtauMSSMHiggs = CbCtauMSSMHiggs()
ClCqMSSMHiggs = ClCqMSSMHiggs()
