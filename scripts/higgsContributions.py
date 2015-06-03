#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--log-mass",dest="logMass", default=False, action="store_true", help="")
agroup.add_option("--mass", dest="mass", type="float", help="")
agroup.add_option("--model-file",dest="modelFile", default="$CMSSW_BASE/src/auxiliaries/models/out.mhmodp-8TeV-tanbHigh-nnlo.root", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp", type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
(options, args) = parser.parse_args()

from array import array
import ROOT as r
import os
import numpy as np

masslist = []
truemasslist = []
fulltanblist = np.array([x for x in range(1,62)], dtype='d')
massaxisname = ""

if options.logMass: 
	masslist = np.array([4.5 + x*2.42/100 for x in range(101)], dtype='d')
	truemasslist = np.exp(masslist)
	massaxisname = "logm_{A}"

else :
	masslist = np.array([90+10*m for m in range(93)], dtype='d')
	truemasslist = masslist
	massaxisname = "m_{A}"

masspoints = len(masslist)-1
fulltanbpoints = len(fulltanblist)-1

massDiffh = r.TH2D('massDiffh', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
massDiffH = r.TH2D('massDiffH', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
cluster = r.TH2D('cluster', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)

ggAXsBR = r.TH2D('ggAXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
ggHXsBR = r.TH2D('ggHXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
gghXsBR = r.TH2D('gghXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)

bbAXsBR = r.TH2D('bbAXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
bbHXsBR = r.TH2D('bbHXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
bbhXsBR = r.TH2D('bbhXsBR', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)

ggcmb = r.TH2D('ggcmb', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
bbcmb = r.TH2D('bbcmb', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)

for j in range(fulltanbpoints):
	mass = options.mass
	tanb = fulltanblist[j]
	truemass = 0
	if options.logMass: truemass = np.exp(options.mass)
	else: truemass = options.mass
	os.system("root -l -b -q '$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/macros/mssm_xs.C(\"{model}\", {mass}, {tanb})' > XsBr{mass}.txt".format(model=options.modelFile, mass=truemass, tanb=tanb))
	
	File = open("XsBr{mass}.txt".format(mass=truemass), 'r')
	xs_data = File.readlines()
	
	massH, massh, ggA, ggH, ggh, bbA, bbH, bbh = 0,0,0,0,0,0,0,0
	for line in xs_data:
		if (line.find('-> xsec(ggA)(tautau): ') > -1): ggA = float(line.replace('-> xsec(ggA)(tautau): ', ''))
		elif (line.find('-> xsec(ggH)(tautau): ') > -1): ggH = float(line.replace('-> xsec(ggH)(tautau): ', ''))
		elif (line.find('-> xsec(ggh)(tautau): ') > -1): ggh = float(line.replace('-> xsec(ggh)(tautau): ', ''))
		elif (line.find('-> xsec(bbA)(tautau): ') > -1): bbA = float(line.replace('-> xsec(bbA)(tautau): ', ''))
		elif (line.find('-> xsec(bbH)(tautau): ') > -1): bbH = float(line.replace('-> xsec(bbH)(tautau): ', ''))
		elif (line.find('-> xsec(bbh)(tautau): ') > -1): bbh = float(line.replace('-> xsec(bbh)(tautau): ', ''))
		elif (line.find('Mass H: ') > -1): massH = float(line.replace('Mass H: ',''))
		elif (line.find('Mass h: ') > -1): massh = float(line.replace('Mass h: ',''))
	
	os.system("rm XsBr{mass}.txt".format(mass=truemass))

	mdiffH = abs((float(truemass)-massH)/float(truemass))
	mdiffh = abs((float(truemass)-massh)/float(truemass))

	massDiffH.Fill(float(mass), float(tanb), mdiffH)
	massDiffh.Fill(float(mass), float(tanb), mdiffh)

	ggAXsBR.Fill(float(mass), float(tanb), ggA)
	ggHXsBR.Fill(float(mass), float(tanb), ggH)
	gghXsBR.Fill(float(mass), float(tanb), ggh)

	bbAXsBR.Fill(float(mass), float(tanb), bbA)
	bbHXsBR.Fill(float(mass), float(tanb), bbH)
	bbhXsBR.Fill(float(mass), float(tanb), bbh)

	contribution, ggcmbXs, bbcmbXs = 0,0,0
	if mdiffh <= options.massTolerance and options.higgsContribution.find("h") != -1:
		contribution += 1
		ggcmbXs += ggh
		bbcmbXs += bbh
	if mdiffH <= options.massTolerance and options.higgsContribution.find("H")!= -1:
		contribution += 2
		ggcmbXs += ggH
		bbcmbXs += bbH
	if options.higgsContribution.find("A") != -1:
		contribution += 4
		ggcmbXs += ggA
		bbcmbXs += bbA
	cluster.Fill(float(mass), float(tanb), contribution)
	ggcmb.Fill(float(mass), float(tanb), ggcmbXs)
	bbcmb.Fill(float(mass), float(tanb), bbcmbXs)

hisfile = r.TFile("$CMSSW_BASE/src/higgsContribution.model{model}.tolerance{tolerance}.contr{contr}.mass{mass}.{log}root".format(model=options.model, tolerance=options.massTolerance, contr=options.higgsContribution, mass=options.mass, log="logMass." if options.logMass else ""), "RECREATE")

massDiffH.Write()
massDiffh.Write()
cluster.Write()

ggAXsBR.Write()
ggHXsBR.Write()
gghXsBR.Write()

bbAXsBR.Write()
bbHXsBR.Write()
bbhXsBR.Write()

ggcmb.Write()
bbcmb.Write()

hisfile.Close()