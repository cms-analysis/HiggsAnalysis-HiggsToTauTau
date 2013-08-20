#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup all datacards and directories.'")
##
## GENERAL OPTIONS
##
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt. [Default: \"mm em et mt tt\"]")
parser.add_option("-p", "--periods", dest="periods", default="7TeV 8TeV", type="string",
                  help="List of run periods for which the datacards are to be copied. [Default: \"7TeV 8TeV\"]")
parser.add_option("-a", "--analyses", dest="analyses", default="bbb, no-bbb",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"bbb, no-bbb\" [Default: \"bbb, no-bbb\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--tail-fitting", dest="fit_tails", default=False, action="store_true",
                  help="Fitting of the MSSM m(tautau) tails for predefined backgrounds [Default: False]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. [Default: \"\"]")
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
parser.add_option("--update-all", dest="update_all", default=False, action="store_true",
                  help="update everything from scratch. If not specified use the following options to specify, which parts of the reload you want to run. [Default: False]")
parser.add_option("--update-setup", dest="update_setup", default=False, action="store_true",
                  help="update setups directory for the indicated analyses. [Default: False]")
parser.add_option("--update-aux", dest="update_aux", default=False, action="store_true",
                  help="update aux directory for the indicated analyses. [Default: False]")
parser.add_option("--update-LIMITS", dest="update_limits", default=False, action="store_true",
                  help="update LIMITS directory for the indicated analyses. [Default: False]")
parser.add_option("--drop-list", dest="drop_list", default="",  type="string",
                  help="The full path to the result file of the pruning if it exists already for pruning of bin-by-bin uncertainties. If empty the pruning will be performed including a mlfit within this script. ATTENTION: this can take a few hours depending on the number of additional bin-by-bin uncertainties. [Default: \"\"]")


## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    #parser.print_usage()
    args.append("90 130 100-200:20 250-500:50 600-1000:100")
    #exit(1)

import os
import glob 
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

## masses
masses = args
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
os.system("mkdir -p backup")

##define inputs from cvs; Note: not all analyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.summer13_analyses_cfg import htt_mm, htt_em, htt_et, htt_mt, htt_tt, htt_tt
directories['mm'] = htt_mm(options.inputs_mm)
directories['em'] = htt_em(options.inputs_em)
directories['et'] = htt_et(options.inputs_et)
directories['mt'] = htt_mt(options.inputs_mt)
directories['tt'] = htt_tt(options.inputs_tt)

## postfix pattern for input files
patterns = {
    'no-bbb' : '',
    'bbb'    : '',
    }

if options.update_all :
    options.update_setup    = True
    options.update_aux= True
    options.update_limits   = True

print "# --------------------------------------------------------------------------------------"
print "# doMSSM.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels                :", options.channels
print "# --periods                 :", options.periods
print "# --analyses                :", options.analyses
print "# --label                   :", options.label
print "# --drop-list               :", options.drop_list
print "# --tail-fitting            :", options.fit_tails
print "# --blind-datacards         :", options.blind_datacards
print "# --extra-templates         :", options.extra_templates
print "# --------------------------------------------------------------------------------------"
print "# --inputs-mm               :", options.inputs_mm
print "# --inputs-em               :", options.inputs_em
print "# --inputs-et               :", options.inputs_et
print "# --inputs-mt               :", options.inputs_mt
print "# --inputs-tt               :", options.inputs_tt
print "# --------------------------------------------------------------------------------------"
print "# --update-setup            :", options.update_setup
print "# --update-aux              :", options.update_aux
print "# --update-LIMITS           :", options.update_limits
print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
print "# guration parameters.                           "
print "# --------------------------------------------------------------------------------------"

## setup main directory
setup="{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
#setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/setup"

if options.update_setup :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## remove existing cash
    if os.path.exists("{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)):
        os.system("rm -r {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))
    os.system("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))

    for chn in channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{SETUP}/{CHN}/*inputs-mssm-*.root".format(SETUP=setup, CHN=chn)) :
            os.system("rm %s" % file)        
        ## define postfix for tail fitting
        tailfit = ''
        if options.fit_tails :
            if chn != 'mm' :
                tailfit = '-fb'
        for per in periods :
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = ''
                if ana in patterns.keys() :
                    pattern = patterns[ana]
                input ="{CHN}.inputs-mssm-{PER}-0{PATTERN}{TAILFIT}.root".format(
                    CHN='htt_'+chn,
                    PER=per,
                    PATTERN=pattern,
                    TAILFIT=tailfit,
                    )
                output="{CHN}.inputs-mssm-{PER}-0.root".format(
                    CHN='htt_'+chn,
                    PER=per,
                    )                
                source="{CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/{FILE}".format(
                    CMSSW_BASE=cmssw_base,
                    DIR=directories[chn][per],
                    FILE=input,
                    )
                for file in glob.glob(source) :
                    if not os.path.exists("{SETUP}/{CHN}/{FILE}".format(SETUP=setup, CHN=chn, FILE=output)) :
                        os.system("cp -v {SOURCE} {SETUP}/{CHN}/{FILE}".format(
                            SOURCE=source,
                            SETUP=setup,
                            CHN=chn,
                            FILE=output
                            ))
            if chn=="mm" :
                ## copy postfit inputs for mm to test directory
                input ="{CHN}.inputs-mssm-{PER}-0{PATTERN}{TAILFIT}-msv.root".format(
                    CHN='htt_'+chn,
                    PER=per,
                    PATTERN=pattern,
                    TAILFIT=tailfit,
                    )
                output="{CHN}.inputs-mssm-{PER}-0-msv.root".format(
                    CHN='htt_'+chn,
                    PER=per,
                    )                
                source="{CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/{FILE}".format(
                    CMSSW_BASE=cmssw_base,
                    DIR=directories[chn][per],  
                    CHN='htt_'+chn,
                    FILE=input,
                    )
                for file in glob.glob(source) :
                    if not os.path.exists("{SETUP}/{CHN}/{FILE}".format(SETUP=setup, CHN=chn, FILE=output)) :
                        os.system("cp -v {SOURCE} {SETUP}/{CHN}/{FILE}".format(
                            SOURCE=file,
                            SETUP=setup,
                            CHN=chn,
                            FILE=output,
                            ))
    ## scale by acceptance correction. This needs to be done for all available masses independent
    ## from args to guarantee that the tanb_grid templates are properly scaled.
    os.system("scale2accept.py -i {SETUP} -c '{CHN}' -p '{PER}' 90 100-200:20 130 250-500:50 600-1000:100".format(
        SETUP=setup,
        CHN=options.channels,
        PER=options.periods,
        ))
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/setups{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        if options.fit_tails:     
            if '7TeV' in periods :
                if 'em' in channels :
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'Fakes_fine_binning' -k '8' --range 150 --rangelast 2000 ".format( 
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'EWK_fine_binning' -k '9' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'EWK_fine_binning' -k '8' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning' -k '9' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning' -k '8' --range 150 ".format(
                        DIR=dir, ANA=ana))
                if 'et' in channels :
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_fine_binning' -k '8' --range 200 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_fine_binning' -k '8' --range 200 ".format(
                         DIR=dir, ANA=ana)) 
                    ## tail fit for QCD shape uncertainties
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_7TeVDown_fine_binning' -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_7TeVUp_fine_binning'   -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                if 'mt' in channels :
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_fine_binning' -k '9' --range 120 --rangelast 2000".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_fine_binning' -k '8' --range 150 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_fine_binning' -k '8' --range 200 ".format(
                        DIR=dir, ANA=ana))
                    ## tail fit for QCD shape uncertainties
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_7TeVDown_fine_binning' -k '8' --range 150 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_7TeVUp_fine_binning'   -k '8' --range 150 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_7TeVDown_fine_binning' -k '9' --range 120 --rangelast 2000 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_7TeVUp_fine_binning'   -k '9' --range 120 --rangelast 2000 --no-uncerts".format(
                        DIR=dir, ANA=ana))
            if "8TeV" in periods :
                if 'em' in channels :
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'Fakes_fine_binning' -k '8' --range 200 --rangelast 2000 ".format( 
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'EWK_fine_binning' -k '9' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'EWK_fine_binning' -k '8' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning' -k '9' --range 200 --rangelast 2000 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning' -k '8' --range 150 ".format(
                        DIR=dir, ANA=ana))
                if 'et' in channels :
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '9' --range 120 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '8' --range 120 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'TT_fine_binning' -k '9' --range 150 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'TT_fine_binning' -k '8' --range 120 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '9' --range 150 ".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '8' --range 200 ".format(
                         DIR=dir, ANA=ana)) 
                    ## tail fit for QCD shape uncertainties
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_8TeVDown_fine_binning' -k '8' --range 120 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_8TeVUp_fine_binning'   -k '8' --range 120 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_8TeVDown_fine_binning' -k '9' --range 120 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_8TeVUp_fine_binning'   -k '9' --range 120 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                if 'mt' in channels : 
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '8' --range 200 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '9' --range 150 ".format(
                        DIR=dir, ANA=ana))           
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '8' --range 150 ".format(
                        DIR=dir, ANA=ana))           
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'TT_fine_binning' -k '9' --range 200 ".format(
                        DIR=dir, ANA=ana))           
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'TT_fine_binning' -k '8' --range 200 ".format(
                        DIR=dir, ANA=ana))           
                    ## tail fit for QCD shape uncertainties
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_8TeVDown_fine_binning' -k '8' --range 200 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_8TeVUp_fine_binning'   -k '8' --range 200 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                if options.channels.find("tt") > -1:
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '9' --range 200 ".format(
                        DIR=dir, ANA=ana))
                    os.system("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '8' --range 200 ".format(
                        DIR=dir, ANA=ana))
                os.system("rm rootlogon.C")
        if ana == 'no-bbb' :
            print "##"
            print "## update no-bbb directory in setup:"
            print "##"
        if ana == 'bbb' :
            print "##"
            print "## update bbb    directory in setup:"
            print "##"
            if 'ee' in channels :
                ## setup bbb uncertainties for ee 
                os.system("add_bbb_errors.py 'ee:7TeV,8TeV:08,09:QCD,TTJ,ZTT,ZEE,WJets>Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mm' in channels :
                ## setup bbb uncertainties for mm  
                os.system("add_bbb_errors.py 'mm:7TeV:08:QCD,TTJ,ZTT,ZMM,WJets>Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("add_bbb_errors.py 'mm:7TeV:09:QCD,TTJ,ZTT,ZMM,Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("add_bbb_errors.py 'mm:8TeV:08,09:QCD,TTJ,ZTT,ZMM,WJets>Dibosons' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'em' in channels :
                ## setup bbb uncertainties for em 
                os.system("add_bbb_errors.py 'em:7TeV,8TeV:08,09:Fakes,EWK,ttbar,Ztt' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                ANA=ana
                ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'et' in channels :
                ## setup bbb uncertainties for et
                os.system("add_bbb_errors.py 'et:7TeV,8TeV:08,09:TT,QCD,ZTT,W+ZL+ZJ>VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mt' in channels :
                ## setup bbb uncertainties for mt
                os.system("add_bbb_errors.py 'mt:7TeV,8TeV:08,09:TT,QCD,ZTT,W+ZL+ZJ>VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'tt' in channels :
                ## setup bbb uncertainties for tt 
                os.system("add_bbb_errors.py 'tt:8TeV:08,09:ZTT,TT,QCD,W+ZL+ZJ>VV' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.05 --mssm".format(
                    DIR=dir,
                    ANA=ana
                    ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana)) 

if options.update_aux :
    print "##"
    print "## update aux directory:"
    print "##"
    dir = "{CMSSW_BASE}/src/aux{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a mssm -c '{CHN}' {MASSES}".format(
            CMSSW_BASE=cmssw_base,
            LABEL=options.label,
            ANA=ana,
            DIR=dir,
            PER=options.periods,
            CHN=options.channels,
            MASSES=' '.join(masses),
            ))
        if ana == "bbb" :
            if options.drop_list != '' :
                for subdir in glob.glob("{DIR}/{ANA}/mssm/*".format(DIR=dir, ANA=ana)) :
                    print '...comment bbb uncertainties for', subdir
                    os.system("commentUncerts.py --drop-list={DROP} {SUB}".format(DROP=options.drop_list, SUB=subdir))            
        ## blind datacards 
        if options.blind_datacards : 
            for chn in channels :
                os.system("blindData.py --update-file --extra-templates '{EXTRA_TEMPLATES}' {DIR}/{ANA}/mssm/{CHN}".format(
                    EXTRA_TEMPLATES = options.extra_templates,
                    DIR=dir,
                    ANA=ana,
                    CHN='htt_'+chn
                    ))

if options.update_limits :
    print "##"
    print "## update LIMITS directory:"
    print "##"
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/LIMITS{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        print "setup limits structure for:", ana
        os.system("setup-htt.py -i aux{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a mssm -c '{CHN}' {LABEL} {MASSES}".format(
            INDEX=options.label,                
            ANA=ana,
            DIR=dir,
            PER=options.periods,
            CHN=options.channels,
            LABEL=options.label,
            MASSES=' '.join(masses),
            ))
