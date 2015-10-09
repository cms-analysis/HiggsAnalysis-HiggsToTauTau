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

qmuHist2D_as = nllfile.Get("qmuHist2D_as")
qmuHist2D = nllfile.Get("qmuHist2D")
NLLmuFixedforqmu = nllfile.Get("NLLmuFixedforqmu")
NLLmuGlobalforqmu = nllfile.Get("NLLmuGlobalforqmu")

CLsbhistNLL = r.TH2D()
ggcmb.Copy(CLsbhistNLL)
CLsbhistNLL.Reset()
CLsbhistNLL.SetName("CLsbhistNLL")

def histcreation(path):
	canvas = r.TCanvas("c","c",400,400)
	canvas.cd()
	hist_copy = r.TH2D()
	qmuHist2D_as.Copy(hist_copy)
	hist_copy.SetContour(1)
	hist_copy.SetContourLevel(0,options.forbiddenRegionLevel)
	hist_copy.Draw("CONT LIST")
	hist_copy.SetLineWidth(2)
	r.gPad.Update()
	conts = r.gROOT.GetListOfSpecials().FindObject("contours")
	curve = r.TGraph()
	curve = conts.First().First()
	forbidden = curve.Clone()
	contourmasslist = forbidden.GetX()
	contourtanblist = forbidden.GetY()

	originalmasslist = [90+10*m for m in range(92)]
	originaltanblist = [x for x in range(1,62)]
	listofcompletedmasses = []
	listofmaxtanb = []

	index = 0
	M = contourmasslist[index]
	T = contourtanblist[index]
	while M >= 90.0:
		binnedmass = int(M)/10*10
		if not (binnedmass in listofcompletedmasses):
			listofcompletedmasses.append(binnedmass)
			listofmaxtanb.append(int(T))
		index += 1
		M = contourmasslist[index]
		T = contourtanblist[index]

	remainingmasslist = [m for m in originalmasslist if m not in listofcompletedmasses]
	for mass in remainingmasslist:
		listofcompletedmasses.append(mass)
		listofmaxtanb.append(60)

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

	deltaNLLforqmu.SetName("deltaNLLforqmu")
	deltaNLLhist.SetName("deltaNLLhist")
	globalNLLhist.SetName("globalNLLhist")
	fullNLLhist.SetName("fullNLLhist")
	NLLdiff2D.SetName("NLLdiff2D")
	rNLLdiff2D.SetName("rNLLdiff2D")

	deltaNLLhist_heavy = r.TH2D()
	deltaNLLhist_light = r.TH2D()
	combinedCluster = r.TH2D()

	ggcmb.Copy(deltaNLLhist_heavy)
	ggcmb.Copy(deltaNLLhist_light)
	ggcmb.Copy(combinedCluster)


	deltaNLLhist_heavy.Reset()
	deltaNLLhist_light.Reset()
	combinedCluster.Reset()

	deltaNLLhist_heavy.SetName("deltaNLLhist_heavy")
	deltaNLLhist_light.SetName("deltaNLLhist_light")
	combinedCluster.SetName("combinedCluster")

	tanbbins = ggcmb.GetNbinsY()

	globalminformass_A = []

	for i in range(len(listofcompletedmasses)):
		mass = listofcompletedmasses[i]
		ggHbbHdatapath = path + "{mass}/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))
		globalminformass_A.append(globalNLL)

	print "min:", min(globalminformass_A)
	
	for i in range(len(listofcompletedmasses)):
		mass = listofcompletedmasses[i]
		tanbmax = listofmaxtanb[i]
		ggHbbHmasspath = path + "{mass}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=mass, analysis=options.analysis)
		ggHbbHdatapath = path + "{mass}/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))

		#print mass, tanbmax,  "globalNLL", globalNLL

		ggHbbHfile = r.TFile(ggHbbHmasspath, "READ")
		scan2D_delta = ggHbbHfile.Get("scan2D_delta")
		massbin = ggcmb.GetXaxis().FindBin(float(mass))

		for tanb in originaltanblist:
			tanbbin = ggcmb.GetYaxis().FindBin(float(tanb)) 
			if tanb <= tanbmax:
				globalNLLhist.SetBinContent(massbin, tanbbin, globalNLL)
				ggHxs = ggcmb.GetBinContent(massbin,tanbbin)
				bbHxs = bbcmb.GetBinContent(massbin,tanbbin)
				
				gluAXs = ggAXsBR.GetBinContent(massbin, tanbbin)
				gluHXs = ggHXsBR.GetBinContent(massbin, tanbbin)
				gluhXs = gghXsBR.GetBinContent(massbin, tanbbin)

				botAXs = bbAXsBR.GetBinContent(massbin, tanbbin)
				botHXs = bbHXsBR.GetBinContent(massbin, tanbbin)
				bothXs = bbhXsBR.GetBinContent(massbin, tanbbin)
				
				massh = int(masshhist.GetBinContent(massbin, tanbbin))/10*10 if (masshhist.GetBinContent(massbin, tanbbin) >= 90) else 90
				massH = int(massHhist.GetBinContent(massbin, tanbbin))/10*10 if (massHhist.GetBinContent(massbin, tanbbin) >= 90) else 90

				ggHbbHfile_forA = r.TFile(path + "{massA}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{massA}.root".format(massA=mass, analysis=options.analysis), "READ")
				ggHbbHfile_forH = r.TFile(path + "{massH}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{massH}.root".format(massH=massH, analysis=options.analysis), "READ")
				ggHbbHfile_forh = r.TFile(path + "{massh}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{massh}.root".format(massh=massh, analysis=options.analysis), "READ")

				scan2D_delta_forA = ggHbbHfile_forA.Get("scan2D_delta")
				scan2D_delta_forH = ggHbbHfile_forH.Get("scan2D_delta")
				scan2D_delta_forh = ggHbbHfile_forh.Get("scan2D_delta")

				xsBin_forA = scan2D_delta_forA.FindBin(gluAXs, botAXs)
				xsBin_forH = scan2D_delta_forH.FindBin(gluHXs, botHXs)
				xsBin_forh = scan2D_delta_forh.FindBin(gluhXs, bothXs)

				if xsBin_forA > 40000: xsBin_forA = 40000
				if xsBin_forH > 40000: xsBin_forH = 40000
				if xsBin_forh > 40000: xsBin_forh = 40000
				deltaNLL_forA = scan2D_delta_forA.GetBinContent(xsBin_forA)
				deltaNLL_forH = scan2D_delta_forH.GetBinContent(xsBin_forH)
				deltaNLL_forh = scan2D_delta_forh.GetBinContent(xsBin_forh)

				deltaNLLhist_heavy.SetBinContent(massbin, tanbbin, deltaNLL_forA + deltaNLL_forH)
				deltaNLLhist_light.SetBinContent(massbin, tanbbin, deltaNLL_forh)

				NLLmu = NLLmuFixedforqmu.GetBinContent(massbin,tanbbin)
				DeltaNLLmu = qmuHist2D.GetBinContent(massbin, tanbbin)/2.0
			
				NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, NLLmu - min(globalminformass_A))
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, DeltaNLLmu)
				xsBin = scan2D_delta.FindBin(ggHxs, bbHxs)
				if xsBin > 40000: xsBin = 40000 # needed to avoid overflow bins, where no NLL values are found -> Set to the last value at that mass.
				if options.lightVsHeavy:
					lightVsHeavy = ((scan2D_delta.GetBinContent(xsBin) < deltaNLL_forh) and cluster.GetBinContent(massbin, tanbbin) == 6)
					deltaNLL = deltaNLL_forh if lightVsHeavy else scan2D_delta.GetBinContent(xsBin)
					combinedCluster.SetBinContent(massbin, tanbbin, 1 if lightVsHeavy else 6)

					database2 = open(path + "{massh}/database_{massh}.out".format(massh=massh), 'r')
					globalNLLstring2 = database2.readline()
					globalNLL2 = float(globalNLLstring2.replace("Absolute value at minimum (best fit): ","")) 
					globalNLL = globalNLL2 if lightVsHeavy else globalNLL
					globalNLLhist.SetBinContent(massbin, tanbbin, globalNLL)
					
				else:	
					deltaNLL = scan2D_delta.GetBinContent(xsBin)
					combinedCluster.SetBinContent(massbin, tanbbin, cluster.GetBinContent(massbin, tanbbin))

				deltaNLLhist.SetBinContent(massbin,tanbbin, deltaNLL)
				fullNLLhist.SetBinContent(massbin,tanbbin, deltaNLL + globalNLL - min(globalminformass_A))

				if mass==700 and tanb==20 :
					print deltaNLL,   globalNLL,      min(globalminformass_A), deltaNLL + globalNLL - min(globalminformass_A)
					print DeltaNLLmu, NLLmu,          min(globalminformass_A), NLLmu - min(globalminformass_A)
				#print massbin, tanbbin, deltaNLL, globalNLL, min(globalminformass_A), deltaNLL + globalNLL - min(globalminformass_A)
			else:
				globalNLLhist.SetBinContent(massbin, tanbbin, min(globalminformass_A))
				NLLmuGlobalforqmu.SetBinContent(massbin, tanbbin, min(globalminformass_A))
				NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhist.SetBinContent(massbin,tanbbin, 100000)
				fullNLLhist.SetBinContent(massbin,tanbbin, 100000)
				deltaNLLhist_heavy.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhist_light.SetBinContent(massbin, tanbbin, 100000)
				combinedCluster.SetBinContent(massbin, tanbbin, cluster.GetBinContent(massbin, tanbbin))

	nllfile.WriteTObject(NLLmuFixedforqmu,'')
	nllfile.WriteTObject(NLLmuGlobalforqmu,'')
	nllfile.WriteTObject(deltaNLLforqmu, '')

	nllfile.WriteTObject(deltaNLLhist,'')
	nllfile.WriteTObject(fullNLLhist,'')
	nllfile.WriteTObject(globalNLLhist, '')
	nllfile.WriteTObject(NLLdiff2D,'')
	nllfile.WriteTObject(rNLLdiff2D,'')

	nllfile.WriteTObject(deltaNLLhist_heavy,'')
	nllfile.WriteTObject(deltaNLLhist_light,'')
	nllfile.WriteTObject(combinedCluster,'')

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
