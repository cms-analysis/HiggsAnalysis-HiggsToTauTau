#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--nll-path",dest="nllPath", default="", type="string", help="")
agroup.add_option("--ggH-bbH-path",dest="ggHbbHPath", default="", type="string", help="")
agroup.add_option("--xs-path",dest="xsPath", default="$CMSSW_BASE/src/higgsContributions/", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp",type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--tolerance-denumerator-max", dest="toleranceDenumeratorMax", default=False, action="store_true", help="")
agroup.add_option("--reference-mass", dest="referenceMass", default="A", type="string", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
agroup.add_option("--forbidden-region-level", dest="forbiddenRegionLevel", default=100, type="float", help="")
agroup.add_option("--analysis", dest="analysis", default="plain", type="string", help="")
agroup.add_option("--light-vs-heavy", dest="lightVsHeavy", default=False, action="store_true", help="")
parser.add_option_group(agroup)

(options, args) = parser.parse_args()

if options.nllPath == "":
	print "Define the path to the NLLHistogramFull.root file."
	exit(1)
if options.ggHbbHPath == "":
	print "Define the path to the folder with the model independent 2-dim fits for data."
	exit(1)

import ROOT as r
from array import array
import sys as s
import os
import glob as g
import math
r.gROOT.SetBatch(True)


def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

##### load correct model
modelFile = r.TFile("auxiliaries/models/out.mhmodp-8TeV-tanbHigh-nnlo.root", "READ")
xs_histo  = modelFile.Get("h_ggF_xsec_h")
BR_histo  = modelFile.Get("h_brtautau_h")
m_histo   = modelFile.Get("h_mh")

#### re-interpretation and direct limit files
nllfile = r.TFile(options.nllPath, "UPDATE")
xsfile = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}{Max}.reference{reference}.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution, Max=".MaxDenumerator" if options.toleranceDenumeratorMax else ""), "READ")
ggcmb = xsfile.Get("ggcmb")
bbcmb = xsfile.Get("bbcmb")

ggAXsBR = xsfile.Get("ggAXsBR")
ggHXsBR = xsfile.Get("ggHXsBR")
gghXsBR = xsfile.Get("gghXsBR")

bbAXsBR = xsfile.Get("bbAXsBR")
bbHXsBR = xsfile.Get("bbHXsBR")
bbhXsBR = xsfile.Get("bbhXsBR")
cluster = xsfile.Get("cluster")

masshhist = xsfile.Get("massh")
massHhist = xsfile.Get("massH")

### mda 
qmuHist2D_as = nllfile.Get("qmuHist2D_as")
qmuHist2D = nllfile.Get("qmuHist2D")
NLLmuFixedforqmu = nllfile.Get("NLLmuFixedforqmu")
NLLmuGlobalforqmu = nllfile.Get("NLLmuGlobalforqmu")

CLsbhistNLL = r.TH2D()
ggcmb.Copy(CLsbhistNLL)
CLsbhistNLL.Reset()
CLsbhistNLL.SetName("CLsbhistNLL")

def histcreation(path):
	originalmasslist = [90+10*m for m in range(92)]
	originaltanblist = [x for x in range(1,61)]

	deltaNLLforqmu = r.TH2D()
	deltaNLLhist = r.TH2D()
	fullNLLhist = r.TH2D()
	globalNLLhist = r.TH2D()
	NLLdiff2D = r.TH2D()
	rNLLdiff2D = r.TH2D()

	ggcmb.Copy(deltaNLLforqmu)
	ggcmb.Copy(deltaNLLhist)
	ggcmb.Copy(fullNLLhist)
	ggcmb.Copy(globalNLLhist)
	ggcmb.Copy(NLLdiff2D)
	ggcmb.Copy(rNLLdiff2D)

	deltaNLLforqmu.Reset()
	deltaNLLhist.Reset()
	fullNLLhist.Reset()
	globalNLLhist.Reset()
	NLLdiff2D.Reset()
	rNLLdiff2D.Reset()

	### mda
	deltaNLLforqmu.SetName("deltaNLLforqmu")

	### mia
	deltaNLLhist.SetName("deltaNLLhist")
	globalNLLhist.SetName("globalNLLhist")
	fullNLLhist.SetName("fullNLLhist")
	
	NLLdiff2D.SetName("NLLdiff2D")
	rNLLdiff2D.SetName("rNLLdiff2D")
        
	combinedCluster = r.TH2D()         
	ggcmb.Copy(combinedCluster)
	combinedCluster.Reset()
	combinedCluster.SetName("combinedCluster")

	globalminformass_A = []

	### find global minium for all mA tanb	
	for mass in originalmasslist :
		for tanb in originaltanblist:
			
			bin = xs_histo.FindBin(mass, tanb)
			mass_h = m_histo.GetBinContent(bin)
			xs_BR = xs_histo.GetBinContent(bin)*BR_histo.GetBinContent(bin)
			scale=0
			if(xs_BR!=0) : scale = ((19.27+1.578+0.4153+0.7046)*0.0632)/(xs_BR)
			else : scale = 1				
			diff=999
			save_scale=999
			for SMHscale in frange(0, 21, 2) :
				if abs(float(SMHscale)/10-scale) < diff:
					diff=abs(float(SMHscale)/10-scale)
					save_scale=float(SMHscale)/10
			if mass_h < 119 : save_scale = 0.0
			ggHbbHdatapath = path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".",""))) + "{mass}/database_{mass}.out".format(mass=mass)		
			database = open(ggHbbHdatapath, 'r')
			globalNLLstring = database.readline()
			globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))
			globalminformass_A.append(globalNLL)

	print "min:", min(globalminformass_A)

        ### loop over all mA tanb and fill histograms
        for mass in originalmasslist:
		for tanb in originaltanblist:
			bin = xs_histo.FindBin(mass, tanb)
			mass_h = m_histo.GetBinContent(bin)
			xs_BR = xs_histo.GetBinContent(bin)*BR_histo.GetBinContent(bin)
			scale=0
			if(xs_BR!=0) : scale = ((19.27+1.578+0.4153+0.7046)*0.0632)/(xs_BR)
			else : scale = 1
			#print mass, tanb, "scale", scale
	
	                ### find correct scale
			diff=999
			save_scale=999
			for SMHscale in frange(0, 21, 2) :
				#print SMHscale, scale, abs(scale-float(SMHscale)/10)
				if abs(float(SMHscale)/10-scale) < diff:
					diff=abs(float(SMHscale)/10-scale)
					save_scale=float(SMHscale)/10 
			if mass_h < 119 : save_scale = 0.0
                    	ggHbbHmasspath = path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".","")))+ "{MASS}/{analysis}-MSSMvsSM-{SMHscale}-asimov-ggH-bbH-scan-GGH-BBH-{MASS}.root".format(MASS=mass, SMHscale=str(save_scale).replace(".",""), analysis=options.analysis)
			ggHbbHdatapath = path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".",""))) + "{MASS}/database_{MASS}.out".format(MASS=mass)
			database = open(ggHbbHdatapath, 'r')
			globalNLL_mass = float((database.readline()).replace("Absolute value at minimum (best fit): ",""))

			#print mass, tanb, "globalNLL", globalNLL
                    
                        ggHbbHfile = r.TFile(ggHbbHmasspath, "READ")
                        scan2D_delta = ggHbbHfile.Get("scan2D_delta")
                    
                        massbin = ggcmb.GetXaxis().FindBin(float(mass))
                        tanbbin = ggcmb.GetYaxis().FindBin(float(tanb))
                    
                        ggHxs = ggcmb.GetBinContent(massbin,tanbbin)
                        bbHxs = bbcmb.GetBinContent(massbin,tanbbin)
                        
                        #gluAXs = ggAXsBR.GetBinContent(massbin, tanbbin)
                        #gluHXs = ggHXsBR.GetBinContent(massbin, tanbbin)
                        #gluhXs = gghXsBR.GetBinContent(massbin, tanbbin)
                        
                        #botAXs = bbAXsBR.GetBinContent(massbin, tanbbin)
                        #botHXs = bbHXsBR.GetBinContent(massbin, tanbbin)
                        #bothXs = bbhXsBR.GetBinContent(massbin, tanbbin)
                        
                        #massh = int(masshhist.GetBinContent(massbin, tanbbin))/10*10 if (masshhist.GetBinContent(massbin, tanbbin) >= 90) else 90
                        #massH = int(massHhist.GetBinContent(massbin, tanbbin))/10*10 if (massHhist.GetBinContent(massbin, tanbbin) >= 90) else 90

                        #ggHbbHfile_forA = r.TFile(path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".",""))) + "{massA}/{analysis}-MSSMvsSM-{SMHscale}-asimov-ggH-bbH-scan-GGH-BBH-{massA}.root".format(massA=mass, SMHscale=str(save_scale).replace(".",""), analysis=options.analysis), "READ")
                        #ggHbbHfile_forH = r.TFile(path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".",""))) + "{massH}/{analysis}-MSSMvsSM-{SMHscale}-asimov-ggH-bbH-scan-GGH-BBH-{massH}.root".format(massH=massH, SMHscale=str(save_scale).replace(".",""), analysis=options.analysis), "READ")
                        #ggHbbHfile_forh = r.TFile(path.replace("-00-", "-{SCALE}-".format(SCALE=str(save_scale).replace(".",""))) + "{massh}/{analysis}-MSSMvsSM-{SMHscale}-asimov-ggH-bbH-scan-GGH-BBH-{massh}.root".format(massh=massh, SMHscale=str(save_scale).replace(".",""), analysis=options.analysis), "READ")
                 
                        #scan2D_delta_forA = ggHbbHfile_forA.Get("scan2D_delta")
                        #scan2D_delta_forH = ggHbbHfile_forH.Get("scan2D_delta")
                        #scan2D_delta_forh = ggHbbHfile_forh.Get("scan2D_delta")
                        
                        #xsBin_forA = scan2D_delta_forA.FindBin(gluAXs, botAXs)
                        #xsBin_forH = scan2D_delta_forH.FindBin(gluHXs, botHXs)
                        #xsBin_forh = scan2D_delta_forh.FindBin(gluhXs, bothXs)
                        
                        #if xsBin_forA > 40000: xsBin_forA = 40000
                        #if xsBin_forH > 40000: xsBin_forH = 40000
                        #if xsBin_forh > 40000: xsBin_forh = 40000
                        #deltaNLL_forA = scan2D_delta_forA.GetBinContent(xsBin_forA)
                        #deltaNLL_forH = scan2D_delta_forH.GetBinContent(xsBin_forH)
                        #deltaNLL_forh = scan2D_delta_forh.GetBinContent(xsBin_forh)

                        
			xsBin = scan2D_delta.FindBin(ggHxs, bbHxs)
			if xsBin > 40000: xsBin = 40000 # needed to avoid overflow bins, where no NLL values are found -> Set to the last value at that mass.

			### mda with offset in global minimum 
                        NLLmu = NLLmuFixedforqmu.GetBinContent(massbin,tanbbin)
                        DeltaNLLmu = qmuHist2D.GetBinContent(massbin, tanbbin)/2.0
                                                
			deltaNLL = scan2D_delta.GetBinContent(xsBin)
			

			### mda
			
                        NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, NLLmu - min(globalminformass_A))
                        deltaNLLforqmu.SetBinContent(massbin, tanbbin, DeltaNLLmu)

			### mia
                        globalNLLhist.SetBinContent(massbin, tanbbin, globalNLL_mass)
			
                        fullNLLhist.SetBinContent(massbin,tanbbin, deltaNLL + globalNLL_mass - min(globalminformass_A))
                        deltaNLLhist.SetBinContent(massbin,tanbbin, deltaNLL)

			if mass==700 and tanb==20 :
				print save_scale 
				print deltaNLL,   globalNLL_mass, min(globalminformass_A), deltaNLL + globalNLL_mass - min(globalminformass_A)
				print DeltaNLLmu, NLLmu,          min(globalminformass_A), NLLmu - min(globalminformass_A)
			#print massbin, tanbbin, deltaNLL, globalNLL, min(globalminformass_A), deltaNLL + globalNLL - min(globalminformass_A)

			### cluster
                        combinedCluster.SetBinContent(massbin, tanbbin, cluster.GetBinContent(massbin, tanbbin))
			
			
			
	nllfile.WriteTObject(NLLmuFixedforqmu,'')
	nllfile.WriteTObject(NLLmuGlobalforqmu,'')
	nllfile.WriteTObject(deltaNLLforqmu, '')

	nllfile.WriteTObject(deltaNLLhist,'')
	nllfile.WriteTObject(fullNLLhist,'')
	nllfile.WriteTObject(globalNLLhist, '')
	nllfile.WriteTObject(NLLdiff2D,'')
	nllfile.WriteTObject(rNLLdiff2D,'')

	nllfile.WriteTObject(combinedCluster,'')

	modelFile.Close()
	ggHbbHfile.Close()
	





histcreation(options.ggHbbHPath)

xbins = ggcmb.GetNbinsX()
ybins = ggcmb.GetNbinsY()

qmuNLL = nllfile.Get("deltaNLLhist")

for i in range(1,xbins+1):
	for j in range(1,ybins+1):
		qmu = 2*qmuNLL.GetBinContent(i,j)
		if qmu < 0: qmu = 0
		CLsb = 1 - r.Math.normal_cdf(r.TMath.Sqrt(qmu))
		if not math.isnan(CLsb): CLsbhistNLL.SetBinContent(i,j, CLsb)

nllfile.WriteTObject(CLsbhistNLL,'')

nllfile.Close()
