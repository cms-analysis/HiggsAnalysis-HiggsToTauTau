#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to reload the MORIOND analysis with main analysis [Moriond-bin-by-bin] and two cross-check analyses [Moriond, Moriond-mvis]. ARGs corresponds to the masses, for which to setup the structure.")
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analyses", dest="analyses", default="moriond moriond-bin-by-bin moriond-mvis moriond-2012d morions-hcp moriond-incl",
                  help="Type of analyses to be considered for updating. Lower case is required. [Default: \"moriond moriond-bin-by-bin moriond-mvis moriond-hcp moriond-2012 moriond-incl\"]")
parser.add_option("--full-update", dest="full_update", default=False, action="store_true",
                  help="update everything from scratch. If not specified use the following options to specify which parts of the reload you want to run. [Default: False]")
parser.add_option("--update-cvs", dest="update_cvs", default=False, action="store_true",
                  help="update root input files from cvs and rescale all input files by SM Higgs cross section. [Default: False]")
parser.add_option("--update-setup", dest="update_setup", default=False, action="store_true",
                  help="update setup directories for the indicated main and cross check analyses. [Default: False]")
parser.add_option("--update-datacards", dest="update_datacards", default=False, action="store_true",
                  help="update skip datacards. [Default: False]")
parser.add_option("--update-limits", dest="update_limits", default=False, action="store_true",
                  help="update directory structure for limit calculation. [Default: False]")
parser.add_option("--fit-result", dest="fit_result", default="",  type="string",
                  help="The full path to the result file of the fit (mlfit.txt) if it exists already fro pruning of bin-by-bin uncertainties. If empty the fit will be performed within this script. ATTENTION: this can take a few hours depending on the number of additional bin-by-bin uncertainties. [Default: \"\"]")


## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import glob


## masses
masses = args[0]
## periods
periods = options.periods.split()
for idx in range(len(periods)) : periods[idx] = periods[idx].rstrip(',')
## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## analyses
analyses = options.analyses.split()
for idx in range(len(analyses)) : analyses[idx] = analyses[idx].rstrip(',')
## CMSSW_BASE
cmssw_base=os.environ['CMSSW_BASE']
## setup a backup directory
os.system("mkdir -p backup")

## directory mapping in cvs auxiliaries/datacards/collected
aux = {
    'em' : ['MIT'],
    'et' : ['Wisconsin', 'Imperial'],
    'mt' : ['Wisconsin', 'Imperial'],
    'mm' : ['Htt_MuMu_Unblinded'],
    'tt' : ['Htt_FullHad']
    }

setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/setup"
    
if options.update_cvs :
    print "##"
    print "## update input files from cvs:"
    print "##"
    for chn in channels :
        print "... copy files for channel:", chn
        for file in glob.glob("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/htt_{CHN}*-sm-*.root".format(CMSSW_BASE=cmssw_base, CHN=chn)) :
            os.system("rm %s" % file)  
        for dir in aux[chn] :
            pattern = "7TeV" if dir == "Imperial" else "" 
            os.system("cp {CMSSW_BASE}/src/auxiliaries/datacards/collected/{DIR}/htt_{CHN}*-sm-{PATTERN}*.root {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/".format(
                CMSSW_BASE=cmssw_base,
                DIR=dir,
                CHN=chn,
                PATTERN=pattern
                ))
    ## scale to SM cross section
    for chn in channels :
        for file in glob.glob("{SETUP}/{CHN}/*-sm-*.root".format(SETUP=setup, CHN=chn)) :
            os.system("scale2SM.py -i {FILE} -s 'ggH, qqH, VH' {MASSES}".format(
                FILE=file,
                MASSES=masses
                ))
                
if options.update_setup :
    print "##"
    print "## update setup directories:"
    print "##"    
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/setups".format(CMSSW_BASE=cmssw_base)
    if os.path.exists(dir) :
        os.system("mv -r {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        ##
        ## MORIOND
        ##
        if ana == 'moriond' :
            pass
        ##
        ## MORIOND-BIN-BY-BIN
        ##
        if ana == 'moriond-bin-by-bin' :
            ## setup bbb uncertainties
            os.system("add_bbb_errors.py 'et,mt,em,mm:7TeV,8TeV:01,03,05:ZMM,ZTT,TTJ,Diboson,ZL,ZLL,Fakes,QCD,W' --input-dir {DIR}/moriond --output-dir {DIR}/{ANA} --threshold 0.10".format(
                DIR=dir,
                ANA=ana
                ))
            ## setup bbb uncertainty pruning
            fit_result = "" if options.fit_result == "" else "--fit-result %s" % optsions.fit_result
            debug = "--debug" if fit_result == "" else ""
            os.system("prune_bbb_errors.py --byPull {FIT} {DEBUG} --pull-threshold 0.30".format(FIT=fit_result, DEBUG=debug))
        ##
        ## MODIOND-MVIS
        ##
        if ana == 'moriond-incl' :
            os.system("mv {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}-mvis.root {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                DIR=dir,
                CHN=chn,
                PER=per
                ))
        ##
        ## MODIOND-HCP
        ##            
        if ana == 'morions-hcp' :
            os.system("mv {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}-hcp.root {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                DIR=dir,
                CHN=chn,
                PER=per
                ))
        ##
        ## MODIOND-2012D
        ##            
        if ana == 'morions-2012d' :
            os.system("mv {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}-2012d.root {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                DIR=dir,
                CHN=chn,
                PER=per
                ))
        ##
        ## MODIOND-INCLUSIVE
        ##            
        if ana == 'morions-incl' :
            os.system("mv {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}-inclusive.root {DIR}/moriond-mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                DIR=dir,
                CHN=chn,
                PER=per
                ))                        

if options.update_datacards :
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/aux".format(CMSSW_BASE=cmssw_base)
    if os.path.exists(dir) :
        os.system("mv -r {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir {DIR}".format(DIR=dir))
    for ana in analyses :
        print "setup datacards for:", ana, "sm"
        per = "8TeV" if ana == 'modiond-2012d' else options.periods
        os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {MASSES}".format(
            CMSSW_BASE=cmssw_base,
            ANA=ana,
            DIR=dir,
            PER=per,
            CHN=options.channels,
            MASSES=masses
            ))

if options.update_limits :
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/LIMITS".format(CMSSW_BASE=cmssw_base)
    if os.path.exists(dir) :
        os.system("mv -r {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir {DIR}".format(DIR=dir))
    for ana in analyses :
        print "setup limits structure for:", ana, "sm"
        if ana == 'moriond' :
            os.system("cvs2local.py -i aux/sm/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {MASSES}".format(
                ANA=ana,
                PER=options.periods,
                CHN=options.channels,
                MASSES=masses
                ))
        else :
            per = "8TeV" if ana == 'modiond-2012d' else options.periods
            label = "" if not '-' in ana else "-l "+ana[ana.find('-')+1:]
            os.system("setup-htt.py -i aux/sm/{ANA} -o {DIR}/{ANA} -p '{PER} '-a sm -c '{CHN}' {LABEL} {MASSES}".format(
                ANA=ana,
                DIR=dir,
                PER=per,
                CHN=chn,
                LABEL=label,
                MASSES=masses
                ))
