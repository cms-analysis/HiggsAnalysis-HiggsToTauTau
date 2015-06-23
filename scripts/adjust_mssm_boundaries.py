#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--xs-path",dest="xsPath", default="$CMSSW_BASE/src/higgsContributions/", type="string", help="")
agroup.add_option("--nll-path",dest="nllPath", default="$CMSSW_BASE/src/LIMITS150428-mssm/bbb-asimov-mhmodp-NLL/mt/", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp",type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--reference-mass", dest="referenceMass", default="A", type="string", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
agroup.add_option("--forbidden-region-level", dest="forbiddenRegionLevel", default=100, type="float", help="")

parser.add_option_group(agroup)

(options, args) = parser.parse_args()

import ROOT as r
import os

# constructing the cross-section file, that determines the contributions of the Higgs bosons to (mA,tanb) points
os.system("rm {xspath}higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution))
os.system("hadd {xspath}higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.root {xspath}higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.mass*.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution))

# constructing the file with CLs histograms
os.system("rm {nllpath}NLLHistogram.Full.root".format(nllpath=options.nllPath))
os.system("hadd {nllpath}NLLHistogram.Full.root {nllpath}*/NLL*.root".format(nllpath=options.nllPath))

# extracting contour of forbidden region.

nllfile = r.TFile("{nllpath}NLLHistogram.Full.root".format(nllpath=options.nllPath), "READ")
xsfile = r.TFile("{xspath}higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.root".format(xspath=options.xsPath, model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution), "READ")

xsboundaries = open("mssm_multidim_fit_boundaries.py", "w")
xsboundaries.write("mssm_multidim_fit_boundaries = {\n")
xsboundaries.write("## key=mass   first value=ggH; second value=bbH\n")
ggcmb = xsfile.Get("ggcmb")
bbcmb = xsfile.Get("bbcmb")

qmuHist2D_as = nllfile.Get("qmuHist2D_as")

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
masslist = forbidden.GetX()
tanblist = forbidden.GetY()

originalmasslist = [90+10*m for m in range(92)]
listofcompletedmasses = []

index = 0
mass = masslist[index]
tanb = tanblist[index]
while mass >= 90.0:
	currentBin = ggcmb.FindBin(mass, tanb)
	binnedmass = int(mass)/10*10
	if not (binnedmass in listofcompletedmasses):
		listofcompletedmasses.append(binnedmass)
		xsboundaries.write('("ggH-bbH", "{mass}")  : ({ggh}, {bbh}),\n'.format(mass=binnedmass, ggh=ggcmb.GetBinContent(currentBin), bbh=bbcmb.GetBinContent(currentBin)))
	index += 1
	mass = masslist[index]
	tanb = tanblist[index]

remainingmasslist = [m for m in originalmasslist if m not in listofcompletedmasses]

for m in remainingmasslist:
	currentBin = ggcmb.FindBin(m, 60)
	xsboundaries.write('("ggH-bbH", "{mass}")  : ({ggh}, {bbh}),\n'.format(mass=m, ggh=ggcmb.GetBinContent(currentBin), bbh=bbcmb.GetBinContent(currentBin)))
	
xsboundaries.write("}\n")
xsboundaries.close()

cmssw_base = os.environ["CMSSW_BASE"]

backupped = 0
for File in os.listdir("{cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/python/".format(cmssw_base=cmssw_base)):
	if  File.endswith("mssm_multidim_fit_boundaries.py.old"): backupped += 1
print backupped
if backupped == 0: os.system("mv {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/python/mssm_multidim_fit_boundaries.py {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/python/mssm_multidim_fit_boundaries.py.old".format(cmssw_base=cmssw_base))
os.system("mv mssm_multidim_fit_boundaries.py {cmssw_base}/src/HiggsAnalysis/HiggsToTauTau/python/".format(cmssw_base=cmssw_base))

