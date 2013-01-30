#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to reload the MORIOND analysis with main analysis [std, bin-by-bin] and four cross-check analyses [mvis, incl, hcp, 2012d]. ARGs corresponds to the masses, for which to setup the structure.")
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et tt\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analyses", dest="analyses", default="std, bin-by-bin, mvis, 2012d, hcp, inclusive",
                  help="Type of analyses to be considered for updating. Lower case is required. [Default: \"std, bin-by-bin, mvis, hcp, 2012d, inclusive\"]")
parser.add_option("--index", dest="index", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--inputs-mm", dest="inputs_mm", default="KIT", type="choice", choices=['KIT'],
                  help="Input files for htt_mm analysis. [Default: \"KIT\"]")
parser.add_option("--inputs-em", dest="inputs_em", default="MIT", type="choice", choices=['MIT', 'Imperial'],
                  help="Input files for htt_em analysis. [Default: \"MIT\"]")
parser.add_option("--inputs-et", dest="inputs_et", default="Wisconsin", type="choice", choices=['Wisconsin', 'Imperial', 'LLR', 'CERN', 'MIT'],
                  help="Input files for htt_et analysis. [Default: \"Wisconsin\"]")
parser.add_option("--inputs-mt", dest="inputs_mt", default="Wisconsin", type="choice", choices=['Wisconsin', 'Imperial', 'LLR', 'CERN'],
                  help="Input files for htt_mt analysis. [Default: \"Wisconsin\"]")
parser.add_option("--inputs-tt", dest="inputs_tt", default="MIT", type="choice", choices=['CERN', 'MIT'],
                  help="Configuration for root input files. At the moment there is a choice for et,mt between Imperial and Wisconsin. [Default: \"Wisconsin\"]")
parser.add_option("--update-all", dest="update_all", default=False, action="store_true",
                  help="update everything from scratch. If not specified use the following options to specify, which parts of the reload you want to run. [Default: False]")
parser.add_option("--update-cvs", dest="update_cvs", default=False, action="store_true",
                  help="update root input files from cvs and rescale all input files by SM Higgs cross section. [Default: False]")
parser.add_option("--update-setups", dest="update_setup", default=False, action="store_true",
                  help="update setups directory for the indicated analyses. [Default: False]")
parser.add_option("--update-aux", dest="update_datacards", default=False, action="store_true",
                  help="update aux directory for the indicated analyses. [Default: False]")
parser.add_option("--update-LIMITS", dest="update_limits", default=False, action="store_true",
                  help="update LIMITS directory for the indicated analyses. [Default: False]")
parser.add_option("--fit-result", dest="fit_result", default="",  type="string",
                  help="The full path to the result file of the fit (mlfit.txt) if it exists already for pruning of bin-by-bin uncertainties. If empty the fit will be performed within this script. ATTENTION: this can take a few hours depending on the number of additional bin-by-bin uncertainties. [Default: \"\"]")


## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    #parser.print_usage()
    args.append("110-145:5")
    #exit(1)

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

## define inputs from cvs; Note: not all ianalyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.moriond_analyses_cfg import htt_mm, htt_em, htt_et, htt_mt, htt_tt
directories['mm'] = htt_mm(options.inputs_mm)
directories['em'] = htt_em(options.inputs_em)
directories['et'] = htt_et(options.inputs_et)
directories['mt'] = htt_mt(options.inputs_mt)
directories['tt'] = htt_tt(options.inputs_tt)

## postfix pattern for input files
patterns = {
    'std'        : '',
    'bin-by-bin' : '',
    'mvis'       : '-mvis', 
    'inclusive'  : '-inclusive',
    '2012d'      : '-2012d',
    'hcp'        : '-hcp',
    }

setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/setup"

if options.update_all :
    options.update_cvs=True
    options.update_setup=True
    options.update_datacards=True
    options.update_limits=True
    
if options.update_cvs :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## copy specialized files names to common file name convention
    auxiliaries=cmssw_base+"/src/auxiliaries/datacards/collected/Imperial"
    for chn in ['et', 'mt', 'em'] :
        for ana in analyses :
            ## specials for Imperial
            specials = {
                'std'        : '-moriond-andrew',
                'bin-by-bin' : '-moriond-andrew',
                'mvis'       : '-mvis-moriond-andrew',
                'inclusive'  : '-inclusive-moriond-andrew',
                '2012d'      : '-2012d-andrew',
                'hcp'        : '-hcp-andrew',
                }
            os.system("cp {BASE}/htt_{CHN}.inputs-sm-8TeV{SPECIAL}.root {BASE}/htt_{CHN}.inputs-sm-8TeV{ANA}.root".format(
                BASE=auxiliaries,
                CHN=chn,
                SPECIAL=specials[ana],
                ANA=patterns[ana]
                ))
    ## copy postfit inputs for mm to test directory
    os.system("cp {CMSSW_BASE}/src/auxiliaries/datacards/collected/Htt_MuMu_Unblinded/htt_mm*-sm-[78]TeV-postfit-*.root {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/mm/".format(
        CMSSW_BASE=cmssw_base
        ))  
    for chn in channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/htt_{CHN}*-sm-*.root".format(CMSSW_BASE=cmssw_base, CHN=chn)) :
            os.system("rm %s" % file)
        for per in periods :
            for ana in analyses :
                pattern = patterns[ana]
                ## for 'hcp' 7TeV is equivalent to central analysis
                if ana  == 'hcp' :
                    if per == '7TeV' :
                        pattern=''
                ## for 2012d skip 7TeV inputs
                if ana == '2012d' :
                    if per == '7TeV' :
                        continue
                source="{CMSSW_BASE}/src/auxiliaries/datacards/collected/{DIR}/htt_{CHN}*-sm-{PER}{PATTERN}.root".format(
                    CMSSW_BASE=cmssw_base,
                    DIR=directories[chn][per],
                    CHN=chn,
                    PER=per,
                    PATTERN=pattern
                    )
                for file in glob.glob(source) :
                    os.system("cp {SOURCE} {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/".format(
                        SOURCE=file,
                        CMSSW_BASE=cmssw_base,
                        CHN=chn
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
    print "## update setups directory:"
    print "##"    
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/setups{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX=options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        ##
        ## MORIOND
        ##
        if ana == 'std' :
            pass
        ##
        ## MORIOND-BIN-BY-BIN
        ##
        if ana == 'bin-by-bin' :
            os.system("cp {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
            if 'mm' in channels :
                ## setup bbb uncertainties for mm (172)
                os.system("add_bbb_errors.py 'mm:7TeV,8TeV:01,03,05:ZTT,TTJ' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'em' in channels :
                ## setup bbb uncertainties for em (103)
                os.system("add_bbb_errors.py 'em:7TeV,8TeV:01,03,05:Fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'et' in channels :
                ## setup bbb uncertainties for et (207)
                os.system("add_bbb_errors.py 'et:7TeV,8TeV:01,03,05:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mt' in channels :
                ## setup bbb uncertainties for mt (203)
                os.system("add_bbb_errors.py 'mt:7TeV,8TeV:01,03,05:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'tt' in channels :
                ## setup bbb uncertainties for tt (72)
                os.system("add_bbb_errors.py 'tt:8TeV:00,01:ZTT,QCD' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        ##
        ## MODIOND-MVIS
        ##
        if ana == 'mvis' :
            for chn in channels :
                for per in periods :
                    if chn == 'tt' :
                        if per == '8TeV' :
                            continue
                    os.system("mv {DIR}/mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}-mvis.root {DIR}/mvis/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                        DIR=dir,
                        CHN=chn,
                        PER=per
                        ))
        ##
        ## MODIOND-HCP
        ##            
        if ana == 'hcp' :
            for chn in channels :
                os.system("mv {DIR}/hcp/{CHN}/htt_{CHN}.inputs-sm-8TeV-hcp.root {DIR}/hcp/{CHN}/htt_{CHN}.inputs-sm-8TeV.root".format(
                    DIR=dir,
                    CHN=chn
                    ))
        ##
        ## MODIOND-2012D
        ##            
        if ana == '2012d' :
            for chn in channels :
                os.system("mv {DIR}/2012d/{CHN}/htt_{CHN}.inputs-sm-8TeV-2012d.root {DIR}/2012d/{CHN}/htt_{CHN}.inputs-sm-8TeV.root".format(
                    DIR=dir,
                    CHN=chn
                    ))
        ##
        ## MODIOND-INCLUSIVE
        ##            
        if ana == 'inclusive' :
            for chn in channels :
                for per in periods :
                    os.system("mv {DIR}/inclusive/{CHN}/htt_{CHN}.inputs-sm-{PER}-inclusive.root {DIR}/inclusive/{CHN}/htt_{CHN}.inputs-sm-{PER}.root".format(
                        DIR=dir,
                        CHN=chn,
                        PER=per
                        ))                        

if options.update_datacards :
    print "##"
    print "## update aux directory:"
    print "##"    
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/aux{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX=options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        print "setup datacards for:", ana, "sm"
        per = "8TeV" if ana == '2012d' else options.periods
        os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {MASSES}".format(
            CMSSW_BASE=cmssw_base,
            ANA=ana,
            DIR=dir,
            PER=per,
            CHN=options.channels,
            MASSES=masses
            ))
        ## if ana == "bin-by-bin" :
##             print "...pruning bbb uncertainties:"
##             ## setup bbb uncertainty pruning
##             os.system("python {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/scripts/prune_bbb_errors.py -c '{CHN}' --byPull {FIT} {DEBUG} --pull-threshold 0.30 {DIR}/{ANA}/sm".format(
##                 CMSSW_BASE=cmssw_base,
##                 FIT="" if options.fit_result == "" else "--fit-result %s" % options.fit_result,
##                 DEBUG="--debug" if options.fit_result == "" else "",
##                 CHN=options.channels,
##                 DIR=dir,
##                 ANA=ana
##                 ))

if options.update_limits :
    print "##"
    print "## update LIMITS directory:"
    print "##"
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/LIMITS{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX=options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        print "setup limits structure for:", ana, "sm"
        if ana == 'inclusive' :
            os.system("cvs2local.py -i aux/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {MASSES}".format(
                ANA=ana,
                DIR=dir,
                PER=options.periods,
                CHN=options.channels,
                MASSES=masses
                ))
        else :
            per = "8TeV" if ana == '2012d' else options.periods
            label = '' if ana == 'std' else '-l '+ana
            os.system("setup-htt.py -i aux/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {LABEL} {MASSES}".format(
                ANA=ana,
                DIR=dir,
                PER=per,
                CHN=options.channels,
                LABEL=label,
                MASSES=masses
                ))
