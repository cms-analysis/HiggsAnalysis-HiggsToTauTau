#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--log-mass",dest="logMass", default=False, action="store_true", help="")
agroup.add_option("--mass", dest="mass", type="float", help="")
agroup.add_option("--model-file",dest="modelFile", default="$CMSSW_BASE/src/auxiliaries/models/out.mhmodp-8TeV-tanbHigh-nnlo.root", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp", type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--reference-mass", dest="referenceMass", default="A", type="string", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")
(options, args) = parser.parse_args()

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

massDiff1 = r.TH2D('massDiff1', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
massDiff2 = r.TH2D('massDiff2', ";{massname}; tan#beta".format(massname=massaxisname), masspoints, masslist, fulltanbpoints, fulltanblist)
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

	ggAXsBR.Fill(float(mass), float(tanb), ggA)
	ggHXsBR.Fill(float(mass), float(tanb), ggH)
	gghXsBR.Fill(float(mass), float(tanb), ggh)

	bbAXsBR.Fill(float(mass), float(tanb), bbA)
	bbHXsBR.Fill(float(mass), float(tanb), bbH)
	bbhXsBR.Fill(float(mass), float(tanb), bbh)

	mdiff1, mdiff2 = 0,0
	contr1, contr2, refcontr = False, False, False
	counter1, counter2, refcounter = 0,0,0
	gg1, gg2, ggref = 0,0,0
	bb1, bb2, bbref = 0,0,0

	if options.referenceMass == "A":
		mdiff1 = abs((float(truemass)-massh)/float(truemass))
		mdiff2 = abs((float(truemass)-massH)/float(truemass))

		contr1 = options.higgsContribution.find("h") != -1
		contr2 = options.higgsContribution.find("H") != -1
		refcontr = options.higgsContribution.find("A") != -1

		counter1, counter2, refcounter = 1, 2, 4
		gg1, gg2, ggref = ggh, ggH, ggA
		bb1, bb2, bbref = bbh, bbH, bbA

	if options.referenceMass == "H":
		mdiff1 = abs((massH-massh)/massH)
		mdiff2 = abs((massH-float(truemass))/massH)

		contr1 = options.higgsContribution.find("h") != -1
		contr2 = options.higgsContribution.find("A") != -1
		refcontr = options.higgsContribution.find("H") != -1

		counter1, counter2, refcounter = 1, 4, 2
		gg1, gg2, ggref = ggh, ggA, ggH
		bb1, bb2, bbref = bbh, bbA, bbH

	if options.referenceMass == "h":
		mdiff1 = abs((massh-float(truemass))/massh)
		mdiff2 = abs((massh-massH)/massh)

		contr1 = options.higgsContribution.find("A") != -1
		contr2 = options.higgsContribution.find("H") != -1
		refcontr = options.higgsContribution.find("h") != -1

		counter1, counter2, refcounter = 4, 2, 1
		gg1, gg2, ggref = ggA, ggH, ggh
		bb1, bb2, bbref = bbA, bbH, bbh


	massDiff1.Fill(float(mass), float(tanb), mdiff1)
	massDiff2.Fill(float(mass), float(tanb), mdiff2)

	contribution, ggcmbXs, bbcmbXs = 0,0,0
	if mdiff1 <= options.massTolerance and contr1:
		contribution += counter1
		ggcmbXs += gg1
		bbcmbXs += bb1
	if mdiff2 <= options.massTolerance and contr2:
		contribution += counter2
		ggcmbXs += gg2
		bbcmbXs += bb2
	if refcontr:
		contribution += refcounter
		ggcmbXs += ggref
		bbcmbXs += bbref

	cluster.Fill(float(mass), float(tanb), contribution)
	ggcmb.Fill(float(mass), float(tanb), ggcmbXs)
	bbcmb.Fill(float(mass), float(tanb), bbcmbXs)

hisfile = r.TFile("$CMSSW_BASE/src/higgsContributions/higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.mass{mass}.{log}root".format(model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution, mass=options.mass, log="logMass." if options.logMass else ""), "RECREATE")

massDiff2.Write()
massDiff1.Write()
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