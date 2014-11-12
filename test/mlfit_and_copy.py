#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to build up the necessary enviroment for postfit plots - including the max-likelihood calculation. ARG corresponds to the mass directory where to find the datacards that will be used or that have been used for the max-likelihood fit.")
parser.add_option("--rMin", dest="rMin", default="-5.", type="string", help="Minimum value of signal strenth. [Default: -5.]")
parser.add_option("--rMax", dest="rMax", default="5.", type="string", help="Maximum value of signal strenth. [Default: 5.]")
parser.add_option("-s", "--skip", dest="skip", default=False, action="store_true", help="Skip the limit calculation in case it has been done already. [Default: False]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="string", help="Type of analysis (sm or mssm). Lower case is required. [Default: \"sm\"]")
parser.add_option("--mm-discriminator", dest="mm_discriminator", default=False, action="store_true", help="Show the actual mm discriminator instead of the more intuitive msvfit plot. [Default: False]")
parser.add_option("--mA", dest="mA", default="160", type="string", help="Mass of pseudoscalar mA only needed for mssm. [Default: '160']")
parser.add_option("--tanb", dest="tanb", default="8", type="string", help="Tanb only needed for mssm. [Default: '8']")
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import sys

dir = args[0]

print "Fitting %s : %s" % (options.analysis, dir)

def system(command):
    """ Version that dies immediately on a command failure """
    result = os.system(command)
    if result:
        sys.exit(result)

system("mkdir -p datacards")
system("mkdir -p root")
system("mkdir -p fitresults")
if not options.skip :
    if options.analysis == "sm" :
        system("limit.py --max-likelihood --stable --rMin %s --rMax %s %s" % (options.rMin, options.rMax, dir))
    if options.analysis == "mssm" :    
        system("limit.py --max-likelihood --stable --rMin %s --rMax %s --physics-model 'tmp=HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:floatingMSSMXSHiggs' --physics-model-options 'modes=ggH;ggHRange=-5:5' %s" % (options.rMin, options.rMax, dir))
    if options.analysis == "Hhh" :
        system("limit.py --max-likelihood --stable --rMin %s --rMax %s --physics-model 'tmp=HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel' --physics-model-options=\'map=^.*h(bb|tt|cc|mm).*/ggHTohhTo2Tau2B$:r[1,-5,5];map=^.*/ggHTohhTo2Tau2B_h(bb|tt|cc|mm)$:r[1,-5,5];map=^.*/ggAToZhToLLBB(\d+\.*\d*)*$:AZhLLBB=AZhLLBB[1,-500,500];map=^.*/ggAToZhToLLTauTau(\d+\.*\d*)*$:AZhLLTauTau=AZhLLTauTau[1,-500,500];map=^.*/bbH(\d+\.*\d*)*$:bbH=bbH[1,-500,500] \' %s" %(options.rMin,options.rMax,dir))


if options.analysis == "sm" :
    system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_sm.txt" % dir)
    system("cp -v %s/*.txt ./datacards" % dir)
    system("cp -v %s/../common/*TeV.root ./root" % dir)
    ## for mm override the histograms as used for the limit calculation in favour of something more human readible
    ##os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-sm-8TeV-postfit-msv.root ./root/htt_mm.input_8TeV.root")
    ##os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-sm-7TeV-postfit-msv.root ./root/htt_mm.input_7TeV.root")

if options.analysis == "mssm" :
    system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_mssm.txt" % dir)
    system("cp -v %s/*.txt ./datacards" % dir)   
    ##system("cp -v %s/../common/hbb.input_[78]TeV-[01].root ./root" % dir)
    system("cp -v %s/../common/htt_*.inputs-mssm-[78]TeV-0.root ./root" % (dir))    
    ## for mm override the histograms as used for the limit calculation in favour of something more human readible
    ## note these files MUST be located in the same directory structure as the input files which are used for the
    ## max-likelihood calculation. 
    if not options.mm_discriminator :
        os.system("cp -v %s/../common/htt_mm.inputs-mssm-8TeV-0-msv.root ./root/htt_mm.inputs-mssm-8TeV-0.root" % (dir))
        os.system("cp -v %s/../common/htt_mm.inputs-mssm-7TeV-0-msv.root ./root/htt_mm.inputs-mssm-7TeV-0.root" % (dir))

if options.analysis == "Hhh" :
    system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_Hhh.txt" % dir)
    system("cp -v %s/*.txt ./datacards" % dir)
    system("cp -v %s/../common/htt_*.input_8TeV.root ./root" % (dir))
    
    optcards = ""  
    for datacard in os.listdir("datacards"):
        if datacard.endswith(".txt"):
            optcards += datacard[:datacard.find(".txt")]
            optcards += "=datacards/"
            ## add datacard for combination
            optcards += datacard
            optcards += " "
    print optcards
    system("combineCards.py -S %s > datacards/tmp.txt" % optcards)
    system("perl -pi -e 's/datacards//g' datacards/{DATACARD}".format(DATACARD="tmp.txt"))
    system("perl -pi -e 's/common/root/g' datacards/{DATACARD}".format(DATACARD="tmp.txt"))
    system("python {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/python/tanb_grid_new.py --ana-type {ANA} --model mhmodp --parameter1 {MA} --tanb {TANB} datacards/{PATH}".format(
        CMSSW_BASE=os.environ['CMSSW_BASE'],
        ANA=options.analysis,
        MA=options.mA,
        TANB=options.tanb,
        PATH="tmp.txt"
        ))
    system("rm datacards/tmp*")

