#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--nll-path",dest="nllPath", default="", type="string", help="")
agroup.add_option("--ggH-bbH-path",dest="ggHbbHPath", default="", type="string", help="")
agroup.add_option("--nll-offset", dest="nllOffSet", default="", type="string", help="")
agroup.add_option("--xs-path",dest="xsPath", default="$CMSSW_BASE/src/higgsContributions/", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp",type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--reference-mass", dest="referenceMass", default="A", type="string", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
agroup.add_option("--forbidden-region-level", dest="forbiddenRegionLevel", default=100, type="float", help="")
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

nllfile = r.TFile(options.nllPath, "UPDATE")
xsfile = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution), "READ")
ggcmb = xsfile.Get("ggcmb")
bbcmb = xsfile.Get("bbcmb")

qmuHist2D_as = nllfile.Get("qmuHist2D_as")
qmuHist2D = nllfile.Get("qmuHist2D")
NLLmuFixedforqmu = nllfile.Get("NLLmuFixedforqmu")
NLLmuGlobalforqmu = nllfile.Get("NLLmuGlobalforqmu")

CLsbhistNLL = r.TH2D()
ggcmb.Copy(CLsbhistNLL)
CLsbhistNLL.Reset()
CLsbhistNLL.SetName("CLsbhistNLL")

def histcreation(path):
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
	originaltanblist = [x for x in range(61)]
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
	
	tanbbins = ggcmb.GetNbinsY()

	globalminformass = []
	
	for i in range(len(listofcompletedmasses)):
		mass = listofcompletedmasses[i]
		ggHbbHdatapath = path + "{mass}/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))
		globalminformass.append(globalNLL)

	if options.nllOffSet == "":  nllOffSet = min(globalminformass)
	else: nllOffSet = -1*float(options.nllOffSet)

	for i in range(len(listofcompletedmasses)):
		mass = listofcompletedmasses[i]
		tanbmax = listofmaxtanb[i]
		ggHbbHmasspath = ""
		string = path + "{mass}/".format(mass=mass)
		for file in g.glob(string+"*-{mass}.root".format(mass=mass)):
			ggHbbHmasspath = file
		ggHbbHmasspath = path + "{mass}/bbb-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=mass)
		ggHbbHdatapath = path + "{mass}/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))

		ggHbbHfile = r.TFile(ggHbbHmasspath, "READ")
		scan2D_delta = ggHbbHfile.Get("scan2D_delta")
		massbin = ggcmb.GetXaxis().FindBin(float(mass))

		for tanb in originaltanblist:
			tanbbin = ggcmb.GetYaxis().FindBin(float(tanb))
			if tanb <= tanbmax:
				globalNLLhist.SetBinContent(massbin, tanbbin, globalNLL)
				ggHxs = ggcmb.GetBinContent(massbin,tanbbin)
				bbHxs = bbcmb.GetBinContent(massbin,tanbbin)

				NLLmu = NLLmuFixedforqmu.GetBinContent(massbin,tanbbin)
				DeltaNLLmu = qmuHist2D.GetBinContent(massbin, tanbbin)/2.0
			
				NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, NLLmu - nllOffSet)
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, DeltaNLLmu)

				xsBin = scan2D_delta.FindBin(ggHxs, bbHxs)
				if xsBin > 40600: xsBin = 40600 # needed to avoid overflow bins, where no NLL values are found -> Set to the last value at that mass.
				deltaNLL = scan2D_delta.GetBinContent(xsBin)

				deltaNLLhist.SetBinContent(massbin,tanbbin, deltaNLL)
				fullNLLhist.SetBinContent(massbin,tanbbin, deltaNLL + globalNLL -nllOffSet)
			else:
				globalNLLhist.SetBinContent(massbin, tanbbin, min(globalminformass))
				NLLmuGlobalforqmu.SetBinContent(massbin, tanbbin, min(globalminformass))
				NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLforqmu.SetBinContent(massbin, tanbbin, 100000)
				deltaNLLhist.SetBinContent(massbin,tanbbin, 100000)
				fullNLLhist.SetBinContent(massbin,tanbbin, 100000)

	nllfile.WriteTObject(NLLmuFixedforqmu,'')
	nllfile.WriteTObject(NLLmuGlobalforqmu,'')
	nllfile.WriteTObject(deltaNLLforqmu, '')

	nllfile.WriteTObject(deltaNLLhist,'')
	nllfile.WriteTObject(fullNLLhist,'')
	nllfile.WriteTObject(globalNLLhist, '')
	nllfile.WriteTObject(NLLdiff2D,'')
	nllfile.WriteTObject(rNLLdiff2D,'')

	ggHbbHfile.Close()

histcreation(options.ggHbbHPath)

xbins = ggcmb.GetNbinsX()
ybins = ggcmb.GetNbinsY()

qmuNLL = nllfile.Get("deltaNLLhist")

for i in range(1,xbins+1):
	for j in range(1,ybins+1):
		qmu = qmuNLL.GetBinContent(i,j)
		if qmu < 0: qmu = 0
		CLsb = 1 - r.Math.normal_cdf(r.TMath.Sqrt(qmu))
		if not math.isnan(CLsb): CLsbhistNLL.SetBinContent(i,j, CLsb)

nllfile.WriteTObject(CLsbhistNLL,'')

nllfile.Close()