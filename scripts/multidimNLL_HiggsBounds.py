#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--nll-path",dest="nllPath", default="", type="string", help="")
agroup.add_option("--ggH-bbH-path",dest="ggHbbHPath", default="", type="string", help="")
agroup.add_option("--bg-path",dest="BGPath", default="", type="string", help="")
agroup.add_option("--xs-path",dest="xsPath", default="$CMSSW_BASE/src/higgsContributions/", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp",type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--tolerance-denumerator-max", dest="toleranceDenumeratorMax", default=False, action="store_true", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
agroup.add_option("--forbidden-region-level", dest="forbiddenRegionLevel", default=100, type="float", help="")
agroup.add_option("--analysis", dest="analysis", default="plain", type="string", help="")
agroup.add_option("--expected", dest="expected", default=False, action="store_true", help="")
agroup.add_option("--weighted-hb", dest="weightedHB", default=False, action="store_true", help="")
agroup.add_option("--full-nll-subtracted", dest="fullNLLSubtracted", default=False, action="store_true", help="")
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
bgfile = 0
if not options.expected: bgfile = r.TFile(options.BGPath, "READ")
xsfileA = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}{Max}.referenceA.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, contr=options.higgsContribution, Max=".MaxDenumerator" if options.toleranceDenumeratorMax else ""), "READ")
xsfileH = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}{Max}.referenceH.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, contr=options.higgsContribution, Max=".MaxDenumerator" if options.toleranceDenumeratorMax else ""), "READ")
xsfileh = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}{Max}.referenceh.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, contr=options.higgsContribution, Max=".MaxDenumerator" if options.toleranceDenumeratorMax else ""), "READ")

ggcmbA = xsfileA.Get("ggcmb")
bbcmbA = xsfileA.Get("bbcmb")

ggcmbH = xsfileH.Get("ggcmb")
bbcmbH = xsfileH.Get("bbcmb")

ggcmbh = xsfileh.Get("ggcmb")
bbcmbh = xsfileh.Get("bbcmb")

massclusterhistA = xsfileA.Get("masscluster")
massclusterhistH = xsfileH.Get("masscluster")
massclusterhisth = xsfileh.Get("masscluster")

clusterA = xsfileA.Get("cluster")
clusterH = xsfileH.Get("cluster")
clusterh = xsfileh.Get("cluster")

qmuHist2D_as = nllfile.Get("qmuHist2D_as")
qmuHist2D = nllfile.Get("qmuHist2D")
NLLmuFixedforqmu = nllfile.Get("NLLmuFixedforqmu")
NLLmuGlobalforqmu = nllfile.Get("NLLmuGlobalforqmu")

CLsbhistNLL = r.TH2D()
ggcmbA.Copy(CLsbhistNLL)
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
	combinedCluster = r.TH2D()
	combinedClusterMass = r.TH2D()
	NLLdiff2D = r.TH2D()
	rNLLdiff2D = r.TH2D()

	ggcmbA.Copy(deltaNLLforqmu)
	ggcmbA.Copy(deltaNLLhist)
	ggcmbA.Copy(fullNLLhist)
	ggcmbA.Copy(globalNLLhist)
	ggcmbA.Copy(combinedCluster)
	ggcmbA.Copy(combinedClusterMass)
	ggcmbA.Copy(NLLdiff2D)
	ggcmbA.Copy(rNLLdiff2D)

	deltaNLLforqmu.Reset()
	deltaNLLhist.Reset()
	fullNLLhist.Reset()
	globalNLLhist.Reset()
	combinedCluster.Reset()
	combinedClusterMass.Reset()
	NLLdiff2D.Reset()
	rNLLdiff2D.Reset()

	deltaNLLforqmu.SetName("deltaNLLforqmu")
	deltaNLLhist.SetName("deltaNLLhist")
	globalNLLhist.SetName("globalNLLhist")
	combinedCluster.SetName("combinedCluster")
	combinedClusterMass.SetName("combinedClusterMass")
	fullNLLhist.SetName("fullNLLhist")
	NLLdiff2D.SetName("NLLdiff2D")
	rNLLdiff2D.SetName("rNLLdiff2D")

	deltaNLLhistA = r.TH2D()
	deltaNLLhistH = r.TH2D()
	deltaNLLhisth = r.TH2D()

	ggcmbA.Copy(deltaNLLhistA)
	ggcmbA.Copy(deltaNLLhistH)
	ggcmbA.Copy(deltaNLLhisth)

	deltaNLLhistA.Reset()
	deltaNLLhistH.Reset()
	deltaNLLhisth.Reset()

	deltaNLLhistA.SetName("deltaNLLhistA")
	deltaNLLhistH.SetName("deltaNLLhistH")
	deltaNLLhisth.SetName("deltaNLLhisth")

	globalminformass = []
	for mass in listofcompletedmasses:
		ggHbbHdatapath = path + "{mass}/database_{mass}.out".format(mass=mass)
		database = open(ggHbbHdatapath, 'r')
		globalminformass.append(float((database.readline()).replace("Absolute value at minimum (best fit): ","")))
	for i in range(len(listofcompletedmasses)):
		mass = listofcompletedmasses[i]
		tanbmax = listofmaxtanb[i]
		massbin = ggcmbA.GetXaxis().FindBin(float(mass))

		for tanb in originaltanblist:
			tanbbin = ggcmbA.GetYaxis().FindBin(float(tanb)) 
			if tanb <= tanbmax:
				massclusterA = int(massclusterhistA.GetBinContent(massbin,tanbbin))/10*10 if massclusterhistA.GetBinContent(massbin,tanbbin) >= 90 else 90
				massclusterH = int(massclusterhistH.GetBinContent(massbin,tanbbin))/10*10 if massclusterhistH.GetBinContent(massbin,tanbbin) >= 90 else 90
				massclusterh = int(massclusterhisth.GetBinContent(massbin,tanbbin))/10*10 if massclusterhisth.GetBinContent(massbin,tanbbin) >= 90 else 90

				ggHbbHmasspathA = path + "{mass}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=massclusterA, analysis=options.analysis)
				ggHbbHdatapathA = path + "{mass}/database_{mass}.out".format(mass=massclusterA)

				ggHbbHmasspathH = path + "{mass}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=massclusterH, analysis=options.analysis)
				ggHbbHdatapathH = path + "{mass}/database_{mass}.out".format(mass=massclusterH)

				ggHbbHmasspathh = path + "{mass}/{analysis}-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=massclusterh, analysis=options.analysis)
				ggHbbHdatapathh = path + "{mass}/database_{mass}.out".format(mass=massclusterh)

				databaseA = open(ggHbbHdatapathA, 'r')
				globalNLLA = float((databaseA.readline()).replace("Absolute value at minimum (best fit): ",""))

				databaseH = open(ggHbbHdatapathH, 'r')
				globalNLLH = float((databaseH.readline()).replace("Absolute value at minimum (best fit): ",""))

				databaseh = open(ggHbbHdatapathh, 'r')
				globalNLLh = float((databaseh.readline()).replace("Absolute value at minimum (best fit): ",""))

				globalNLLlist = [globalNLLA, globalNLLH, globalNLLh]

				ggHbbHfileA = r.TFile(ggHbbHmasspathA, "READ")
				scan2D_deltaA = ggHbbHfileA.Get("scan2D_delta")
				ggXsA = ggcmbA.GetBinContent(massbin, tanbbin)
				bbXsA = bbcmbA.GetBinContent(massbin, tanbbin)
				xsBinA = scan2D_deltaA.FindBin(ggXsA,bbXsA) if scan2D_deltaA.FindBin(ggXsA,bbXsA) <= 40000 else 40000
				deltaNLLA = scan2D_deltaA.GetBinContent(xsBinA)
				deltaNLLhistA.SetBinContent(massbin, tanbbin, deltaNLLA)

				ggHbbHfileH = r.TFile(ggHbbHmasspathH, "READ")
				scan2D_deltaH = ggHbbHfileH.Get("scan2D_delta")
				ggXsH = ggcmbH.GetBinContent(massbin, tanbbin)
				bbXsH = bbcmbH.GetBinContent(massbin, tanbbin)
				xsBinH = scan2D_deltaH.FindBin(ggXsH,bbXsH) if scan2D_deltaH.FindBin(ggXsH,bbXsH) <= 40000 else 40000
				deltaNLLH = scan2D_deltaH.GetBinContent(xsBinH)
				deltaNLLhistH.SetBinContent(massbin, tanbbin, deltaNLLH)

				ggHbbHfileh = r.TFile(ggHbbHmasspathh, "READ")
				scan2D_deltah = ggHbbHfileh.Get("scan2D_delta")
				ggXsh = ggcmbh.GetBinContent(massbin, tanbbin)
				bbXsh = bbcmbh.GetBinContent(massbin, tanbbin)
				xsBinh = scan2D_deltah.FindBin(ggXsh,bbXsh) if scan2D_deltah.FindBin(ggXsh,bbXsh) <= 40000 else 40000
				deltaNLLh = scan2D_deltah.GetBinContent(xsBinh)
				deltaNLLhisth.SetBinContent(massbin, tanbbin, deltaNLLh)
				
				masslist = [massclusterA, massclusterH, massclusterh]
				deltaNLLlist = [deltaNLLA, deltaNLLH, deltaNLLh]
				fullNLLlist = [deltaNLLA+globalNLLA, deltaNLLH+globalNLLH, deltaNLLh+globalNLLh]
				deltaNLLbest = 0
				fullNLLbest = 0
				deltaNLLbestIndex = 0
				globalNLLbest = 0
				if options.expected:
					deltaNLLbest = max(deltaNLLlist)
					deltaNLLbestIndex = deltaNLLlist.index(deltaNLLbest)
					globalNLLbest = globalNLLlist[deltaNLLbestIndex]
					fulNLLbest = fullNLLlist[deltaNLLbestIndex]
				else:
					bg_deltaNLLhistA = bgfile.Get("deltaNLLhistA")
					bg_deltaNLLhistH = bgfile.Get("deltaNLLhistH")
					bg_deltaNLLhisth = bgfile.Get("deltaNLLhisth")

					bg_deltaNLLA = bg_deltaNLLhistA.GetBinContent(massbin, tanbbin)
					bg_deltaNLLH = bg_deltaNLLhistH.GetBinContent(massbin, tanbbin)
					bg_deltaNLLh = bg_deltaNLLhisth.GetBinContent(massbin, tanbbin)
					bg_deltaNLLlist = [bg_deltaNLLA,bg_deltaNLLH,bg_deltaNLLh]
					if options.weightedHB:
						bg_sum = (bg_deltaNLLA+bg_deltaNLLH+bg_deltaNLLh)
						if abs(bg_sum) <= 0.001:
							bg_sum = 0.001
							globalNLLbest = min(globalminformass)
						else:
							globalNLLbest = (globalNLLA*bg_deltaNLLA+globalNLLH*bg_deltaNLLH+globalNLLh*bg_deltaNLLh)/bg_sum
							deltaNLLbest = (deltaNLLA*bg_deltaNLLA+deltaNLLH*bg_deltaNLLH+deltaNLLh*bg_deltaNLLh)/bg_sum
							if globalNLLbest >= 0: globalNLLbest = min(globalminformass)
							fullNLLbest = deltaNLLbest + globalNLLbest
					elif options.fullNLLSubtracted:
						bg_sum = (bg_deltaNLLA+bg_deltaNLLH+bg_deltaNLLh)
						if abs(bg_sum) <= 0.001:
							bg_sum = 0.001
							globalNLLbest = min(globalminformass)
						else:
							globalNLLbest = (globalNLLA*bg_deltaNLLA+globalNLLH*bg_deltaNLLH+globalNLLh*bg_deltaNLLh)/bg_sum
							fullNLLbest = fullNLLlist[0]
							deltaNLLbest = fullNLLbest - globalNLLbest
					else:
						bg_deltaNLLbest = max(bg_deltaNLLlist)
						deltaNLLbestIndex = bg_deltaNLLlist.index(bg_deltaNLLbest)
						deltaNLLbest = deltaNLLlist[deltaNLLbestIndex]
						globalNLLbest = globalNLLlist[deltaNLLbestIndex]
						fullNLLbest = fullNLLlist[deltaNLLbestIndex]
				
				clusterlist = [clusterA, clusterH, clusterh]
				clusterbest = clusterlist[deltaNLLbestIndex]
				massbest = masslist[deltaNLLbestIndex]

				NLLmu = NLLmuFixedforqmu.GetBinContent(massbin,tanbbin)
				DeltaNLLmu = qmuHist2D.GetBinContent(massbin, tanbbin)/2.0

				NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, NLLmu - min(globalminformass))
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, DeltaNLLmu)

				globalNLLhist.SetBinContent(massbin, tanbbin, globalNLLbest)
				deltaNLLhist.SetBinContent(massbin,tanbbin, deltaNLLbest)
				fullNLLhist.SetBinContent(massbin,tanbbin, fullNLLbest - min(globalminformass))
				combinedCluster.SetBinContent(massbin, tanbbin, clusterbest.GetBinContent(massbin, tanbbin))
				combinedClusterMass.SetBinContent(massbin, tanbbin, massbest)
			else:
				globalNLLhist.SetBinContent(massbin, tanbbin, min(globalminformass))
				NLLmuGlobalforqmu.SetBinContent(massbin, tanbbin, min(globalminformass))
				NLLmuFixedforqmu.SetBinContent(massbin,tanbbin, 100000)
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhist.SetBinContent(massbin,tanbbin, 100000)
				fullNLLhist.SetBinContent(massbin,tanbbin, 100000)
				combinedCluster.SetBinContent(massbin, tanbbin, 0)
				combinedClusterMass.SetBinContent(massbin, tanbbin, 0)
				deltaNLLhistA.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhistH.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhisth.SetBinContent(massbin, tanbbin, 100000)

	nllfile.WriteTObject(NLLmuFixedforqmu,'')
	nllfile.WriteTObject(NLLmuGlobalforqmu,'')
	nllfile.WriteTObject(deltaNLLforqmu, '')

	nllfile.WriteTObject(deltaNLLhist,'')
	nllfile.WriteTObject(fullNLLhist,'')
	nllfile.WriteTObject(globalNLLhist, '')
	nllfile.WriteTObject(NLLdiff2D,'')
	nllfile.WriteTObject(rNLLdiff2D,'')

	nllfile.WriteTObject(combinedCluster,'')
	nllfile.WriteTObject(combinedClusterMass,'')

	nllfile.WriteTObject(deltaNLLhistA,'')
	nllfile.WriteTObject(deltaNLLhistH,'')
	nllfile.WriteTObject(deltaNLLhisth,'')

	ggHbbHfileA.Close()
	ggHbbHfileH.Close()
	ggHbbHfileh.Close()

histcreation(options.ggHbbHPath)

xbins = ggcmbA.GetNbinsX()
ybins = ggcmbA.GetNbinsY()

qmuNLL = nllfile.Get("deltaNLLhist")

for i in range(1,xbins+1):
	for j in range(1,ybins+1):
		qmu = 2*qmuNLL.GetBinContent(i,j)
		if qmu < 0: qmu = 0
		CLsb = 1 - r.Math.normal_cdf(r.TMath.Sqrt(qmu))
		if not math.isnan(CLsb): CLsbhistNLL.SetBinContent(i,j, CLsb)

nllfile.WriteTObject(CLsbhistNLL,'')

nllfile.Close()