#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

parser = OptionParser(usage="usage: %prog [options] input_path",
                      description="This is a script to build up the necessary enviroment for post-fit plots - including the max-likelihood calculation. ARG corresponds to the mass directory where to fin the datacards for the max-likelihood fit.")
parser.add_option("--rMin", dest="rMin", default="-5.", type="string", help="Minimum value of signal strenth. [Default: -5.]")
parser.add_option("--rMax", dest="rMax", default="5.", type="string", help="Maximum value of signal strenth. [Default: 5.]")
parser.add_option("-s", "--skip", dest="skip", default=False, action="store_true", help="Skip the limit calculation in case it has been done already. [Default: False]")
parser.add_option("-a", "--analysis", dest="analysis", default="sm", type="string", help="Type of analysis (sm or mssm). Lower case is required. [Default: \"sm\"]")
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
    system("limit.py --max-likelihood --stable --rMin %s --rMax %s %s" % (options.rMin, options.rMax, dir))

if options.analysis == "sm" :
    system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_sm.txt" % dir)
    system("cp -v %s/*.txt ./datacards" % dir)
    system("cp -v %s/../common/*TeV.root ./root" % dir)
    ## for mm override the histograms as used for the limit calculation in favour of something more human readible
    #os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-sm-8TeV-postfit-msv.root ./root/htt_mm.input_8TeV.root")
    #os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-sm-7TeV-postfit-msv.root ./root/htt_mm.input_7TeV.root")

if options.analysis == "mssm" :
    system("cp -v %s/out/mlfit.txt ./fitresults/mlfit_mssm.txt" % dir)
    system("cp -v %s/*.txt ./datacards" % dir)
    system("cp -v %s/../common/hbb.input_[78]TeV-[01].root ./root" % dir)
    system("cp -v %s/../common/htt_*.inputs-mssm-[78]TeV-0.root ./root" % dir)
    ## for mm override the histograms as used for the limit calculation in favour of something more human readible
    #os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-mssm-8TeV-0-postfit-msv.root ./root/htt_mm.inputs-mssm-8TeV-0.root")
    #os.system("cp -v $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/mm/htt_mm.inputs-mssm-7TeV-0-postfit-msv.root ./root/htt_mm.inputs-mssm-7TeV-0.root")

