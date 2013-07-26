#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup all datacards and directories.'")
##
## GENERAL OPTIONS
##
parser.add_option("-c", "--channels", dest="channels", default="ee mm em mt et tt hbb", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hbb. [Default: \"ee mm em et mt tt hbb\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analyses", dest="analyses", default="std, pruned",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"std, bin-by-bin, pruned\" [Default: \"std, pruned\"]")
#parser.add_option("--split-categories", dest="split_categories", default=False, action="store_true",
#                  help="Using split categories, means categories 0, 1, 2, 3, 6, 7 instead of 8, 9 [Default: False]")
parser.add_option("--fit-tails", dest="fit_tails", default=False, action="store_true",
                  help="Fitting of the MSSM m(tautau) tails for certain backgrounds [Default: False]")
parser.add_option("--label", dest="index", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--fit-result", dest="fit_result", default="",  type="string",
                  help="The full path to the result file of the fit (mlfit.txt) if it exists already for pruning of bin-by-bin uncertainties. If empty the fit will be performed within this script. ATTENTION: this can take a few hours depending on the number of additional bin-by-bin uncertainties. [Default: \"\"]")
parser.add_option("--drop-list", dest="drop_list", default="",  type="string",
                  help="The full path to the result file of the pruning if it exists already for pruning of bin-by-bin uncertainties. If empty the pruning will be performed including a mlfit within this script. ATTENTION: this can take a few hours depending on the number of additional bin-by-bin uncertainties. [Default: \"\"]")
parser.add_option("-m", "--masses", dest="masses", default="100-200:20", type="string",
                  help="List of masses for which the datacards are set up. [Default: \"100-200:20\"]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. [Default: \"\"]")
##
## INPUTS OPTIONS
##
parser.add_option("--inputs-ee", dest="inputs_ee", default="KIT", type="choice", choices=['KIT'],
                  help="Input files for htt_ee analysis. [Default: \"KIT\"]")
parser.add_option("--inputs-mm", dest="inputs_mm", default="KIT", type="choice", choices=['KIT'],
                  help="Input files for htt_mm analysis. [Default: \"KIT\"]")
parser.add_option("--inputs-em", dest="inputs_em", default="MIT", type="choice", choices=['MIT', 'Imperial'],
                  help="Input files for htt_em analysis. [Default: \"MIT\"]")
parser.add_option("--inputs-et", dest="inputs_et", default="Imperial", type="choice", choices=['Wisconsin', 'Imperial', 'CERN'],
                  help="Input files for htt_et analysis. [Default: \"Imperial\"]")
parser.add_option("--inputs-mt", dest="inputs_mt", default="Imperial", type="choice", choices=['Wisconsin', 'Imperial', 'LLR', 'CERN', 'MIT'],
                  help="Input files for htt_mt analysis. [Default: \"Imperial\"]")
parser.add_option("--inputs-tt", dest="inputs_tt", default="MIT", type="choice", choices=['CERN', 'MIT'],
                  help="Input files for htt_tt analysis. [Default: \"MIT\"]")
parser.add_option("--inputs-hbb", dest="inputs_hbb", default="DESY", type="choice", choices=['DESY'],
                  help="Input files for hbb analysis. [Default: \"MIT\"]")
##
## SKIP/UPDATE OPTIONS
##
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
parser.add_option("--skip-pruning", dest="skip_pruning", default=False, action="store_true",
                  help="Skip pruning step when doing --setup-aux. [Default: False]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

#if len(args) < 1 :
#     parser.print_usage()
#     exit(1)

import os
import glob 
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

## masses
masses = options.masses.split()
for idx in range(len(masses)) : masses[idx] = masses[idx].rstrip(',')
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
os.system("mkdir -p MSSM_backup")

##define inputs from cvs; Note: not all analyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.moriond_analyses_cfg import htt_mm, htt_em, htt_et, htt_mt, htt_tt, htt_tt
directories['mm'] = htt_mm(options.inputs_mm)
directories['em'] = htt_em(options.inputs_em)
#directories['ee'] = htt_ee(options.inputs_ee)
directories['et'] = htt_et(options.inputs_et)
directories['mt'] = htt_mt(options.inputs_mt)
directories['tt'] = htt_tt(options.inputs_tt)

## postfix pattern for input files
patterns = {
    'std'        : '',
    'bin-by-bin' : '',
    'pruned'     : '',
    #'mvis'       : '-mvis', 
    #'inclusive'  : '-inclusive',
    #'2012d'      : '-2012d',
    #'hcp'        : '-hcp',
    }

## full channel name  for input files
fullname = {
    'mm'   : 'htt_mm',
    'mt'   : 'htt_mt',
    'ee'   : 'htt_ee',
    'em'   : 'htt_em',
    'et'   : 'htt_et', 
    'tt'   : 'htt_tt',
    'hbb'  : 'hbb',
    }

if options.update_all :
    options.update_cvs=True
    options.update_setup=True
    options.update_datacards=True
    options.update_limits=True


setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/setup"

##
## START 
##
if options.update_cvs :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## copy specialized file names to common file name convention
    for chn in channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/{FULLNAME}*.root".format(CMSSW_BASE=cmssw_base, CHN=chn, FULLNAME=fullname[chn])) :
            os.system("rm %s" % file)
        for per in periods :
            if chn == 'tt' :
                    if per == '7TeV' :
                        continue
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = patterns[ana]
                #source="{CMSSW_BASE}/src/auxiliaries/datacards/mssm/{FULLNAME}/{FULLNAME}*-mssm-{PER}-[01]{PATTERN}.root".format(
                source="{CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/{FULLNAME}*-mssm-{PER}-[01]{PATTERN}.root".format(
                    CMSSW_BASE=cmssw_base,
                    CHN=chn,
                    PER=per,
                    DIR=directories[chn][per],  
                    PATTERN=pattern,
                    FULLNAME=fullname[chn]
                    )
                for file in glob.glob(source) :
                    os.system("cp {SOURCE} {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/".format(
                        SOURCE=file,
                        CMSSW_BASE=cmssw_base,
                        CHN=chn
                        ))
            if chn=="mm" :
                ## copy postfit inputs for mm to test directory
                #os.system("cp {CMSSW_BASE}/src/auxiliaries/datacards/mssm/htt_mm/htt_mm*-mssm-[78]TeV-[01]-msv.root {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/mm/".format( 
                os.system("cp {CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/htt_mm*-mssm-[78]TeV-[01]-msv.root {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/mm/".format(
                    DIR=directories[chn][per],
                    CMSSW_BASE=cmssw_base         
                    ))
    ## scaling of root files 
    ##acceptance correction
    print "INFO: Acceptance correction scaling"
    os.system("python HiggsAnalysis/HiggsToTauTau/scripts/scale2accept.py -i {SETUP} -c '{CHN}' -p '{PER}' 90 100-200:20 130 250-500:50 600-1000:100".format(
        CHN=options.channels,
        PER=options.periods,
        SETUP=setup
        ))
    #os.system("python HiggsAnalysis/HiggsToTauTau/scripts/scale2accept.py -i {SETUP} -c hbb -p 7TeV 90 100-200:20 130 250-350:50".format(
    #    SETUP=setup
    #    ))
    

if options.update_setup:
    print "##"
    print "## update setups directory:"
    print "##"    
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/MSSM_setups{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX='' if options.index == '' else '_'+options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/MSSM_backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/MSSM_backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/MSSM_backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
       
        #### NEW TO BE TESTED!!
        if options.fit_tails:     
            print "INFO: Fitting of the background tails"
            if "7TeV" in periods :
                if options.channels.find("em") > -1:
                    #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'Fakes_fine_binning' -k '9' --range 150 --rebin".format( 
                    #    DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'Fakes_fine_binning' -k '8' --range 150 --rangelast 2000 --rebin".format( 
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'EWK_fine_binning' -k '9' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'EWK_fine_binning' -k '8' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'ttbar_fine_binning' -k '8' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'ttbar_fine_binning' -k '9' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                if options.channels.find("et") > -1:
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'QCD_fine_binning' -k '9' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'QCD_fine_binning' -k '8' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                     #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'TT_fine_binning' -k '9' --range 200 --rebin".format(
                     #    DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'TT_fine_binning' -k '8' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                     #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'W_fine_binning' -k '9' --range 120 --rebin".format(
                     #    DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'W_fine_binning' -k '8' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9")) 
                if options.channels.find("mt") > -1:
                    #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'QCD_fine_binning' -k '9' --range 120 --rebin".format(
                    #    DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'QCD_fine_binning' -k '8' --range 120 --rebin".format(
                    #    DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'W_fine_binning' -k '{CATEGORIES}' --range 200 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'TT_fine_binning' -k '{CATEGORIES}' --range 200 --rebin".format(
                        DIR=dir, ANA=ana, PER="7TeV", CATEGORIES="8 9"))
            if "8TeV" in periods :
                if options.channels.find("em") > -1:
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'Fakes_fine_binning' -k '9' --range 200 --rangelast 2000 --rebin".format( 
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'Fakes_fine_binning' -k '8' --range 200 --rangelast 2000 --rebin".format( 
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'EWK_fine_binning' -k '9' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'EWK_fine_binning' -k '8' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'ttbar_fine_binning' -k '8' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-{PER}-0.root -c em -e {PER} -b 'ttbar_fine_binning' -k '9' --range 200 --rangelast 2000 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                if options.channels.find("et") > -1:
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'QCD_fine_binning' -k '9' --range 120 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'QCD_fine_binning' -k '8' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'TT_fine_binning' -k '9' --range 150 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'TT_fine_binning' -k '8' --range 120 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'W_fine_binning' -k '9' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-{PER}-0.root -c et -e {PER} -b 'W_fine_binning' -k '8' --range 200 --rebin".format(
                         DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9")) 
                if options.channels.find("mt") > -1:
                    #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'QCD_fine_binning' -k '9' --range 100 --rangelast 800 --rebin".format(
                    #    DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    #os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'QCD_fine_binning' -k '8' --range 100 --rangelast 800 --rebin".format(
                    #    DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'W_fine_binning' -k '{CATEGORIES}' --range 200 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))           
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-{PER}-0.root -c mt -e {PER} -b 'TT_fine_binning' -k '{CATEGORIES}' --range 200 --rebin".format(
                        DIR=dir, ANA=ana, PER="8TeV", CATEGORIES="8 9"))           
                if options.channels.find("tt") > -1:
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '8 9' --range 200 --rebin".format(
                        DIR=dir, ANA=ana))
        ##################
         
        if ana == 'std' :
            pass      
        if ana == 'bin-by-bin'  or ana == 'pruned' :
            ##bin-by-bin uncertainties
            print "INFO: Adding bin-by-bin uncertainties"
            if 'ee' in channels :
                ## setup bbb uncertainties for ee 
                os.system("add_bbb_errors.py 'ee:7TeV,8TeV:08,09:WJets,QCD,TTJ,ZTT,ZEE,Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mm' in channels :
                ## setup bbb uncertainties for mm 
                os.system("add_bbb_errors.py 'mm:7TeV,8TeV:08,09:WJets,QCD,TTJ,ZTT,ZMM,Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'em' in channels :
                ## setup bbb uncertainties for em 
                os.system("add_bbb_errors.py 'em:7TeV,8TeV:08,09:Fakes,EWK,ttbar,Ztt' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                ANA=ana
                ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'et' in channels :
                ## setup bbb uncertainties for et
                os.system("add_bbb_errors.py 'et:7TeV,8TeV:08:TT,QCD,W,ZTT,ZL,ZJ,VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("add_bbb_errors.py 'et:7TeV,8TeV:09:TT,QCD,W,ZTT,ZLL,VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mt' in channels :
                ## setup bbb uncertainties for mt
                os.system("add_bbb_errors.py 'mt:7TeV,8TeV:08:TT,QCD,W,ZTT,ZL,ZJ,VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("add_bbb_errors.py 'mt:7TeV,8TeV:09:TT,QCD,W,ZTT,ZLL,VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'tt' in channels :
                ## setup bbb uncertainties for tt
                os.system("add_bbb_errors.py 'tt:8TeV:08:QCD,ZTT,TT,W,VV,ZL,ZJ' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana)) # ZL not working here
                os.system("add_bbb_errors.py 'tt:8TeV:09:QCD,ZTT,TT,W,VV,ZJ' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana)) 
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        ##     if 'hbb' in channels:
##                 ## setup bbb uncertainties for hbb (???)
##                 os.system("add_bbb_errors.py 'hbb:8TeV:01,03,05:ZL,ZJ,QCD>W'  --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10 --mssm".format(
##                     DIR=dir,
##                     ANA=ana
##                     ))
##                 os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
##                 os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))

if options.update_datacards :
    print "##"
    print "## update aux directory:"
    print "##"
    dir = "{CMSSW_BASE}/src/MSSM_aux{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX='' if options.index == '' else '_'+options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/MSSM_backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/MSSM_backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/MSSM_backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    ##creation of datacards
    for ana in analyses :
        os.system("setup-datacards.py -i {CMSSW_BASE}/src/MSSM_setups{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a mssm -c '{CHN}' {CATEGORIES} {MASSES}".format(
            INDEX='' if options.index == '' else '_'+options.index,
            CMSSW_BASE=cmssw_base,
            ANA=ana,
            DIR=dir,
            PER=options.periods,
            CHN=options.channels,
            MASSES=options.masses,
            CATEGORIES=""
            ))
        if ana == "pruned" :
            if not options.skip_pruning :
                os.system("rm -r pruning_results")
                print "...pruning bbb uncertainties:"
                if options.drop_list == "" :
                    ## setup bbb uncertainty pruning
                    os.system("setup-htt.py -i {DIR}/{ANA} -o pruning_results -p '{PER}' -a mssm -c '{CHN}' {CATEGORIES} 160".format(
                        DIR=dir,               
                        ANA=ana,
                        PER=options.periods,
                        CHN=options.channels,
                        CATEGORIES="" 
                        ))
                    ## maximum-likelihood-fit
                    os.system("limit.py --max-likelihood --stable --rMin -5 --rMax 5 pruning_results/cmb/160")               
                    ## setup bbb uncertainty pruning
                    os.system("python HiggsAnalysis/HiggsToTauTau/scripts/prune-uncerts-htt.py --mass 160 --fit-results='pruning_results/cmb/160/out/mlfit.txt' --threshold=0.3 --whitelist='_bin_' pruning_results/cmb/160")
                ## commenting out of pruned uncertainties
                for chn in channels :
                    print "python HiggsAnalysis/CombinedLimit/scripts/commentUncerts.py --drop-list='{DROP_LIST}' MSSM_aux{INDEX}/{ANA}/mssm/{FULLNAME}".format(
                        DROP_LIST = 'uncertainty-pruning-drop.txt' if options.drop_list == "" else options.drop_list,
                        INDEX='' if options.index == '' else '_'+options.index,                
                        ANA=ana,
                        FULLNAME=fullname[chn]
                        )
                    os.system("python HiggsAnalysis/CombinedLimit/scripts/commentUncerts.py --drop-list='{DROP_LIST}' MSSM_aux{INDEX}/{ANA}/mssm/{FULLNAME}".format(
                        DROP_LIST = 'uncertainty-pruning-drop.txt' if options.drop_list == "" else options.drop_list,
                        INDEX='' if options.index == '' else '_'+options.index,                
                        ANA=ana,
                        FULLNAME=fullname[chn]
                        ))
                
        ## blinding 
        if options.blind_datacards : 
            for chn in channels :
                os.system("python HiggsAnalysis/HiggsToTauTau/scripts/blindData.py --update-file --extra-templates '{EXTRA_TEMPLATES}' {DIR}/{ANA}/mssm/{CHN}".format(
                    EXTRA_TEMPLATES = options.extra_templates,
                    ANA=ana,
                    DIR=dir,
                    CHN=fullname[chn]
                    ))

if options.update_limits :
    print "##"
    print "## update LIMITS directory:"
    print "##"
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/MSSM_LIMITS{INDEX}".format(CMSSW_BASE=cmssw_base, INDEX='' if options.index == '' else '_'+options.index)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/MSSM_backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/MSSM_backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/MSSM_backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        print "setup limits structure for:", ana, "mssm"
        ## this os a try to live w/o the additional label, which is really annoying once it coem to plotting 
        label = '' #if ana == 'std' else '-l '+ana
        os.system("setup-htt.py -i MSSM_aux{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a mssm -c '{CHN}' {LABEL} {CATEGORIES} {MASSES}".format(
            INDEX='' if options.index == '' else '_'+options.index,                
            ANA=ana,
            DIR=dir,
            PER=options.periods,
            CHN=options.channels,
            LABEL=label,
            MASSES=options.masses,
            CATEGORIES=""
            ))
