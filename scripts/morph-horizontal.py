#!/usr/bin/env python
import os
import re

class Morph:
    def __init__(self,cgs_file,acc_file,xsec_ggf_file,xsec_vbf_file,xsec_tth_file,br_file):
        ## name of the file to contain the main configurable parameters
        self.cgs_file = cgs_file
        ## name of the file to contain the acceptances
        self.acc_file = acc_file
        ## name of the file to contain the gluon gluon fusion cross sections as function of the mass 
        self.xsec_ggf_file = xsec_ggf_file
        ## name of the file to contain the vbf cross sections as function of the mass 
        self.xsec_vbf_file = xsec_vbf_file
        ## name of the file to contain the associated Higgs production cross sections as function of the mass 
        self.xsec_tth_file = xsec_tth_file
        ## name of the file to contain the branching ratio as function of the mass 
        self.br_file = br_file
        ## dictionary of gluon gluon fusion cross section
        self.xsec_ggf = {}
        ## dictionary of vbf cross section
        self.xsec_vbf = {}
        ## dictionary of associated Higgs production cross section
        self.xsec_tth = {}
        ## dictionary of branching ratios
        self.br = {}
        ## name of the input file
        self.input = ""
        ## name of the output file
        self.output = ""        
        ## luminosty to scale to
        self.lumi = ""
        ## step size for the interpolation
        self.deltaM = ""
        ## list of event categories in the input file
        self.categories = []
        ## list of shape uncertainties in the input file
        self.shapes = []        
        ## list of signal samples in the input file
        self.signals = []
        ## list of lower mass values for the interpolation
        self.lowerMass = []
        ## list of upper mass values for the interpolation
        self.upperMass = []
        ## list of lower mass values for the interpolation
        self.lowerAcc = []
        ## list of upper mass values for the interpolation
        self.upperAcc = []

    def read_xsec(self, dict, file):
        f = open(file)
        for line in f:
            line = line.strip().split("\n")[0].strip()   
            if line == "" or line.startswith("#") or line.startswith("%"):
                continue
            else:
                wordarr = line.strip().split()
                ## cross section as function of the mass
                dict[wordarr[0]] = wordarr[1]
        f.close()
            
    def read_BR(self):
        f = open(self.br_file)
        for line in f:
            line = line.strip().split("\n")[0].strip()   
            if line == "" or line.startswith("#") or line.startswith("%"):
                continue
            else:
                wordarr = line.strip().split()
                ## BR as a function of the mass
                self.br[wordarr[0]] = wordarr[2]
        f.close()

    def read_cgs(self):
        f = open(self.cgs_file)
        for line in f:
            line = line.strip().split("\n")[0].strip()
            ## remove all ',\s+' from line, so the group can be a comma
            ## seperated list separated by an arbitrary number of spaces 
            pattern = re.compile(r",\s+")
            line = re.sub(pattern, ",", line)
            if line == "" or line.startswith("#") or line.startswith("%"):
                continue
            else:
                if line.startswith("input:"):
                    self.input = line.lstrip("input:").strip()
                if line.startswith("output:"):
                    self.output = line.lstrip("output:").strip()                
                if line.startswith("lumi:"):
                    self.lumi = line.lstrip("lumi:").strip()
                if line.startswith("deltaM:"):
                    self.deltaM = line.lstrip("deltaM:").strip()
                if line.lower().startswith("signals:"):
                    self.signals = line.lstrip("signals:").strip().split(",")
                if line.lower().startswith("categories:"):
                    self.categories = line.lstrip("categories:").strip().split(",")
                if line.lower().startswith("shapes:"):
                    self.shapes = line.lstrip("shapes:").strip().split(",")                                        
        f.close()
        
    def read_acc(self):
        for signal in self.signals :
            for category in self.categories :
                f = open(self.acc_file)
                for line in f:
                    line = line.strip().split("\n")[0].strip()
                    if line == "" or line.startswith("#") or line.startswith("%"):
                        continue
                    else:
                        wordarr = line.strip().split()
                        if wordarr[0] == signal:
                            if wordarr[1] == category:
                                self.lowerMass.append(wordarr[2])
                                self.upperMass.append(wordarr[3])
                                self.lowerAcc.append(wordarr[4])
                                self.upperAcc.append(wordarr[5])
                f.close()
                self.write_cfg(signal, category)

    def write_cfg(self, signal, category):
        for idx in range(0, len(self.lowerMass)):
            ## compose morphing PSet
            im=0
            points = "## vector of event classes (bins)\n"
            points+= "    points = cms.VPSet(\n"
            while float(self.lowerMass[idx])+(im+1)*float(self.deltaM)<float(self.upperMass[idx]):
                mass = "%.1f" % (float(self.lowerMass[idx])+(im+1)*float(self.deltaM))
                nxsec=0
                if signal == "Higgs_gf_sm":
                    nxsec = self.xsec_ggf[mass]
                if signal == "Higgs_vbf_sm":
                    nxsec = self.xsec_vbf[mass]
                if signal == "Higgs_tth_sm":
                    nxsec = self.xsec_tth[mass]
                if im==0:
                    points+= "         cms.PSet(mass = cms.double({point}), norm = cms.double({xsec}*{br}*{lumi}))\n".format(
                        point=mass, xsec=nxsec, br=self.br[mass], lumi=self.lumi)
                else:
                    points+= "        ,cms.PSet(mass = cms.double({point}), norm = cms.double({xsec}*{br}*{lumi}))\n".format(
                        point=mass, xsec=nxsec, br=self.br[mass], lumi=self.lumi)
                im=im+1
            points+="    )\n"
            ##write main config file for central values           
            cfg = open("morph_{category}_{signal}_mH{lower}-{upper}_cfg.py".format(category=category, signal=signal, lower=self.lowerMass[idx], upper=self.upperMass[idx]), "w")
            cfg.write(
"""import FWCore.ParameterSet.Config as cms
horizontalMorphing = cms.PSet(
    ## define input file
    inputFile  = cms.string("{input}"),
    ## event category
    directory  = cms.string("{category}"),
    ## signal sample
    histName   = cms.string("{signal}_$MASS"), 
    ## lower bound for the interpolation
    lowerBound = cms.double({lowerBound}),    
    ## lower bound acceptance
    lowerAccept= cms.double({lowerAccept}), 
    ## upper bound for the interpolation
    upperBound = cms.double({upperBound}),
    ## upper bound acceptance
    upperAccept= cms.double({upperAccept}), 
    {points})
""".format(
        input=self.input, category=category, signal=signal, lowerBound=self.lowerMass[idx], lowerAccept=self.lowerAcc[idx],
        upperBound=self.upperMass[idx], upperAccept=self.upperAcc[idx], points=points
        ))

            for uncert in self.shapes:
                shape = "_"
                shape+=uncert
                ##write main config file for central values           
                cfg = open("morph_{category}_{signal}_mH{lower}-{upper}{shape}_cfg.py".format(category=category, signal=signal, lower=self.lowerMass[idx], upper=self.upperMass[idx], shape=shape), "w")
                cfg.write(
"""import FWCore.ParameterSet.Config as cms
horizontalMorphing = cms.PSet(
    ## define input file
    inputFile  = cms.string("{input}"),
    ## event category
    directory  = cms.string("{category}"),
    ## signal sample
    histName   = cms.string("{signal}_$MASS{shape}"), 
    ## lower bound for the interpolation
    lowerBound = cms.double({lowerBound}),    
    ## lower bound acceptance
    lowerAccept= cms.double({lowerAccept}), 
    ## upper bound for the interpolation
    upperBound = cms.double({upperBound}),
    ## upper bound acceptance
    upperAccept= cms.double({upperAccept}), 
    {points})
""".format(
        input=self.input, category=category, signal=signal, shape=shape, lowerBound=self.lowerMass[idx], lowerAccept=self.lowerAcc[idx],
        upperBound=self.upperMass[idx], upperAccept=self.upperAcc[idx], points=points
        ))
                
morphing = Morph(cgs_file     ="MitLimits/Higgs2Tau/setup/morph/cgs.config",
                 acc_file     ="MitLimits/Higgs2Tau/setup/morph/acc.config",
                 xsec_ggf_file="MitLimits/Higgs2Tau/setup/morph/ggH.xsec",
                 xsec_vbf_file="MitLimits/Higgs2Tau/setup/morph/qqH.xsec",
                 xsec_tth_file="MitLimits/Higgs2Tau/setup/morph/vtt.xsec",
                 br_file      ="MitLimits/Higgs2Tau/setup/morph/BR.par"
                 )

morphing.read_BR()
morphing.read_xsec(morphing.xsec_ggf, morphing.xsec_ggf_file)
morphing.read_xsec(morphing.xsec_vbf, morphing.xsec_vbf_file)
morphing.read_xsec(morphing.xsec_tth, morphing.xsec_tth_file)
morphing.read_cgs()
morphing.read_acc()

dirList = os.listdir(os.getcwd())
for file in dirList:
    if file.startswith("morph_"):
        print file
        os.system("horizontal-morphing %s" % file)
        os.system("rm %s" % file)
