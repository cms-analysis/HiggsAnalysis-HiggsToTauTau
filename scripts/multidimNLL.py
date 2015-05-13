#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--nll-path",dest="nllPath", default="", type="string", help="")
agroup.add_option("--ggH-bbH-path",dest="ggHbbHPath", default="", type="string", help="")
agroup.add_option("--ggH-bbH-path-asimov", dest="ggHbbHPathAsimov", default="", type="string", help="")
parser.add_option_group(agroup)

(options, args) = parser.parse_args()

if options.nllPath == "":
	print "Define the path to the NLLHistogramFull.root file."
	exit(1)
if options.ggHbbHPath == "":
	print "Define the path to the folder with the model independent 2-dim fits for data."
	exit(1)
if options.ggHbbHPathAsimov == "":
	print "Define the path to the folder with the model independent 2-dim fits for expected background."
	exit(1)

import ROOT as r
from array import array
import sys as s
import os
import glob as g
import math

nllfile = r.TFile(options.nllPath, "UPDATE")
ggcmb = nllfile.Get("ggcmb")
bbcmb = nllfile.Get("bbcmb")

deltaNLLforqmu = r.TH2D()
ggcmb.Copy(deltaNLLforqmu)
deltaNLLforqmu.Reset()
deltaNLLforqmu.SetName("deltaNLLforqmu")
deltaNLLforqmu.SetTitle('#DeltaNLL values of q_{#mu} for (m_{A}, tan#beta) plane; m_{A}; tan#beta')

deltaNLLforqA = r.TH2D()
ggcmb.Copy(deltaNLLforqA)
deltaNLLforqA.Reset()
deltaNLLforqA.SetName("deltaNLLforqA")
deltaNLLforqA.SetTitle('#DeltaNLL values of q_{A} for (m_{A}, tan#beta) plane; m_{A}; tan#beta')

nllfile.WriteTObject(deltaNLLforqmu, '')
nllfile.WriteTObject(deltaNLLforqA, '')

CLshistNLL = r.TH2D()
ggcmb.Copy(CLshistNLL)
CLshistNLL.Reset()
CLshistNLL.SetName("CLshistNLL")
CLshistNLL.SetTitle("CLs for (m_{A}, tan#beta) plane; m_{A}; tan#beta")

def histcreation(path, asimov=""):

	if asimov == "": NLLmuFixedforqmu = nllfile.Get("NLLmuFixedforqmu")
	else : NLLmuFixedforqmu  = nllfile.Get("NLLmuFixedforqA")

	deltaNLLhist = r.TH2D()
	fullNLLhist = r.TH2D()
	globalNLLhist = r.TH2D()
	NLLdiff2D = r.TH2D()
	rNLLdiff2D = r.TH2D()

	ggcmb.Copy(deltaNLLhist)
	ggcmb.Copy(fullNLLhist)
	ggcmb.Copy(globalNLLhist)
	ggcmb.Copy(NLLdiff2D)
	ggcmb.Copy(rNLLdiff2D)


	deltaNLLhist.Reset()
	fullNLLhist.Reset()
	globalNLLhist.Reset()
	NLLdiff2D.Reset()
	rNLLdiff2D.Reset()


	deltaNLLhist.SetName("deltaNLLhist"+asimov)
	deltaNLLhist.SetTitle("#DeltaNLL for (m_{A}, tan#beta) plane; m_{A}; tan#beta")
	deltaNLLhist.GetZaxis().SetRangeUser(0.001,100000)

	globalNLLhist.SetName("globalNLLhist"+asimov)
	globalNLLhist.SetTitle("global fit NLL for (m_{A}, tan#beta) plane; m_{A}; tan#beta")

	fullNLLhist.SetName("fullNLLhist"+asimov)
	fullNLLhist.SetTitle("full NLL for (m_{A}, tan#beta) plane; m_{A}; tan#beta")

	NLLdiff2D.SetName("NLLdiff2D"+asimov)
	NLLdiff2D.SetTitle("Difference between the full NLL of the two approaches for (m_{A}, tan#beta) plane;  m_{A}; tan#beta")

	rNLLdiff2D.SetName("rNLLdiff2D"+asimov)
	rNLLdiff2D.SetTitle("rel. Difference between the full NLL of the two approaches for (m_{A}, tan#beta) plane;  m_{A}; tan#beta")

	tanbbins = ggcmb.GetNbinsY()

	masslist = os.listdir(path)
	masslist.remove('common')
	globalminformass = []
	for mass in masslist:
		ggHbbHdatapath = path + mass + "/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))
		globalminformass.append(globalNLL)
	nllOffSet = min(globalminformass)
	
	for mass in masslist:
		ggHbbHmasspath = path + mass + "/bbb-asimov-ggH-bbH-scan-GGH-BBH-{mass}.root".format(mass=mass)
		ggHbbHdatapath = path + mass + "/database_{mass}.out".format(mass=mass)

		database = open(ggHbbHdatapath, 'r')
		globalNLLstring = database.readline()
		globalNLL = float(globalNLLstring.replace("Absolute value at minimum (best fit): ",""))

		ggHbbHfile = r.TFile(ggHbbHmasspath, "READ")
		scan2D_delta = ggHbbHfile.Get("scan2D_delta")
		massbin = ggcmb.GetXaxis().FindBin(float(mass))

		for tanbbin in range(1,tanbbins+1):
			ggHxs = ggcmb.GetBinContent(massbin,tanbbin)
			bbHxs = bbcmb.GetBinContent(massbin,tanbbin)

			NLLmu = NLLmuFixedforqmu.GetBinContent(massbin,tanbbin)
			NLLmuMin = NLLmuFixedforqmu.GetMinimum()
			NLLmuFixedforqmu.SetBinContent(massbin, tanbbin, NLLmu - NLLmuMin)

			xsBin = scan2D_delta.FindBin(ggHxs, bbHxs)
			deltaNLL = scan2D_delta.GetBinContent(xsBin)
			#print "model dependent: ", NLLmu, " modelindependent: ", (deltaNLL+globalNLL)
			if deltaNLL < 10000000:
				deltaNLLhist.SetBinContent(massbin,tanbbin, deltaNLL)
				globalNLLhist.SetBinContent(massbin, tanbbin, globalNLL)
				fullNLLhist.SetBinContent(massbin,tanbbin, deltaNLL+globalNLL-nllOffSet)

	nllfile.WriteTObject(NLLmuFixedforqmu,'')

	nllfile.WriteTObject(deltaNLLhist,'')
	nllfile.WriteTObject(fullNLLhist,'')
	nllfile.WriteTObject(globalNLLhist, '')
	nllfile.WriteTObject(NLLdiff2D,'')
	nllfile.WriteTObject(rNLLdiff2D,'')

	ggHbbHfile.Close()

histcreation(options.ggHbbHPath)
histcreation(options.ggHbbHPathAsimov, "_as")

xbins = ggcmb.GetNbinsX()
ybins = ggcmb.GetNbinsY()

qmuNLL = nllfile.Get("deltaNLLhist")
qANLL = nllfile.Get("deltaNLLhist_as")

for i in range(1,xbins+1):
	for j in range(1,ybins+1):
		qmu = qmuNLL.GetBinContent(i,j)
		qA = qANLL.GetBinContent(i,j)
		CLsb = 1 - r.Math.normal_cdf(r.TMath.Sqrt(qmu))
		CLb = r.Math.normal_cdf(r.TMath.Sqrt(qA)-r.TMath.Sqrt(qmu))
		if CLb == 0: CLs = 0
		else: CLs = CLsb/(1.*CLb)
		if not math.isnan(CLs): CLshistNLL.SetBinContent(i,j, CLs)

nllfile.WriteTObject(CLshistNLL,'')

nllfile.Close()