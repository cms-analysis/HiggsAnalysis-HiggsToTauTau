#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.LimitsConfig import configuration
from HiggsAnalysis.HiggsToTauTau.UncertAdaptor import UncertAdaptor
from HiggsAnalysis.HiggsToTauTau.horizontal_morphing import Morph
from HiggsAnalysis.HiggsToTauTau.AsimovDatacard import *
from HiggsAnalysis.HiggsToTauTau.scale2SM import RescaleSamples
from HiggsAnalysis.HiggsToTauTau.utils import is_number
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 
from HiggsAnalysis.HiggsToTauTau.utils import get_shape_systematics

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to reload the Summer13 analysis for the main analyses [bbb, no-bbb] and potential cross check analyses [mvis, incl]. ARGs corresponds to the masses, for which to setup the structure.")
parser.add_option("-a", "--analyses", dest="analyses", default="no-bbb, bbb",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"no-bbb, bbb, bbb:hww-sig, no-bbb:hww-sig, mvis, inclusive\" [Default: \"no-bbb, bbb\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. [Default: \"\"]")
parser.add_option("--ignore-during-scaling", dest="do_not_scales", default="mm vhtt", type="string",
                  help="List of channels, which the scaling by cross seciton times BR should not be applied. The list should be embraced by call-ons and separeted by whitespace or comma. [Default: \"vhtt mm\"]")
parser.add_option("--new-merging", dest="new_merging", default=False, action="store_true",
                  help="added to test the new merging introduced by Andrew. [Default: False]")
parser.add_option("--new-merging-threshold", dest="new_merging_threshold", default="0.5", type="string",
                  help="Threshold for the new merging by Andrew. [Default: \"0.5\"]")
parser.add_option("--drop-normalize-bbb", dest="drop_normalize_bbb", default=False, action="store_true",
                  help="Normalize yield to stay constand when adding bbb shape uncertainties. [Default: False]")
parser.add_option("--update-all", dest="update_all", default=False, action="store_true",
                  help="update everything from scratch. If not specified use the following options to specify, which parts of the reload you want to run. [Default: False]")
parser.add_option("--update-setup", dest="update_setup", default=False, action="store_true",
                  help="update root input files from cvs and rescale all input files by SM Higgs cross section. [Default: False]")
parser.add_option("--update-aux", dest="update_aux", default=False, action="store_true",
                  help="update aux directory for the indicated analyses. [Default: False]")
parser.add_option("--update-LIMITS", dest="update_limits", default=False, action="store_true",
                  help="update LIMITS directory for the indicated analyses. [Default: False]")
parser.add_option("--drop-list", dest="drop_list", default="",  type="string",
                  help="The full path to the list of uncertainties to be dropped from the datacards due to pruning. If this string is empty no prunig will be applied. [Default: \"\"]")
parser.add_option("-c", "--config", dest="config", default="",
                  help="Additional configuration file to be used for the setup [Default: \"\"]")
parser.add_option("--model",dest="model",default="",
                  help="Setup directory structure for model-dependent limits in bins of a different variable than mass. Possible choices are lowmH and 2HDM [Default:\"\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    #parser.print_usage()
    if options.model=="2HDM" :
        args.append("0_1:0.1")
    else :
        args.append("220_350:10")
    #exit(1)

import os
import re
import glob 
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
from HiggsAnalysis.HiggsToTauTau.utils import get_channel_dirs

## masses
masses = args
## do_not_scales
do_not_scales = options.do_not_scales.split()
for idx in range(len(do_not_scales)) : do_not_scales[idx] = do_not_scales[idx].rstrip(',')
## analyses
analyses = options.analyses.split()
for idx in range(len(analyses)) : analyses[idx] = analyses[idx].rstrip(',')
## CMSSW_BASE
cmssw_base=os.environ['CMSSW_BASE']
## setup a backup directory
os.system("mkdir -p backup")
## configuration
config=configuration('AZh', options.config)

## define inputs from cvs; Note: not all analyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.summer13_analyses_cfg import htt_AZh
for chn in config.channels:
    directories[chn] = locals()['htt_'+chn](config.inputs[chn])

## postfix pattern for input files
patterns = {
    'no-bbb'         : '',
    'bbb'            : '',
    }

if options.update_all :
    options.update_setup     = True
    options.update_aux       = True
    options.update_limits    = True

masspoints = parseArgs(args)
masspoints = [str(points) for points in masspoints]

print "# --------------------------------------------------------------------------------------"
print "# doAZh.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels                :", ' '.join(config.channels)
print "# --periods                 :", ' '.join(config.periods)
print "# --analyses                :", options.analyses
print "# --label                   :", options.label
print "# --drop-list               :", options.drop_list
print "# --ignore-during-scaling   :", options.do_not_scales
print "# --new-merging             :", options.new_merging
print "# --new-merging-threshold   :", options.new_merging_threshold
print "# --drop-bbb-normalisation  :", options.drop_normalize_bbb
print "# --blind-datacards         :", options.blind_datacards
print "# --extra-templates         :", options.extra_templates
print "# --------------------------------------------------------------------------------------"
for chn in config.channels:
    print "# --inputs-"+chn+"               :", config.inputs[chn]
print "# --------------------------------------------------------------------------------------"
print "# --update-setup            :", options.update_setup
print "# --update-aux              :", options.update_aux
print "# --update-LIMITS           :", options.update_limits
print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
print "# guration parameters.                           "
print "# --------------------------------------------------------------------------------------"

## setup main directory 
setup="{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)

if options.update_setup :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## remove existing cash
    if os.path.exists("{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)):
        os.system("rm -r {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))
    os.system("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup-AZh {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))
    ## copy all input files in question and nothing else by these
    for chn in config.channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{SETUP}/{CHN}/*inputs-AZh-*.root".format(SETUP=setup, CHN=chn)) :
            os.system("rm %s" % file)
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = ''
                if ana in patterns.keys() :
                    pattern =  ''
                source="{CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/{CHN}.inputs-AZh-{PER}{PATTERN}.root".format(
                    CMSSW_BASE=cmssw_base,
                    DIR=directories[chn][per],
                    CHN=chn+'_*' if chn == 'vhtt' else 'htt_'+chn,
                    PER=per,
                    PATTERN=pattern
                    )
                for file in glob.glob(source) :
                        os.system("cp -v {SOURCE} {SETUP}/{CHN}/{CHNNAME}.inputs-AZh-{PER}.root".format(
                            SOURCE=file,
                            CHN=chn,
                            CHNNAME='htt_'+chn,
                            SETUP=setup,
                            PER=per
                            ))
    ## set up directory structure
    dir = "{CMSSW_BASE}/src/setups{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        ##
        ## CENTRAL
        ##
        if ana == 'no-bbb' :
            print "##"
            print "## update no-bbb directory in setup:"
            print "##"
        ##
        ## BIN-BY-BIN
        ##
        if ana == 'bbb' :
            print "##"
            print "## update bbb    directory in setup:"
            print "##"    
            for chn in config.channels:
                for per in config.periods:
                    for idx in range(len(config.bbbcat[chn][per])):
                        if options.new_merging :
                            filename='vhtt.inputs-sm-'+per+'.root' if chn == "vhtt" else 'htt_'+chn+'.inputs-AZh-'+per+'.root'
                            for cat in config.bbbcat[chn][per][idx].split(',') :
                                ## loop all categories in question for index idx
                                if len(config.bbbproc[chn][idx].replace('>',',').split(','))>1 :
                                    ## only get into action if there is more than one sample to do the merging for
                                    os.system("merge_bin_errors.py --folder {DIR} --processes {PROC} --bbb_threshold={BBBTHR} --merge_threshold={THRESH} --verbose {SOURCE} {TARGET}".format(
                                        ## this list has only one entry by construction
                                        DIR=get_channel_dirs(chn, cat,per)[0],
                                        PROC=config.bbbproc[chn][idx].replace('>',','),
                                        BBBTHR=config.bbbthreshold[chn],
                                        THRESH=options.new_merging_threshold,
                                        SOURCE=dir+'/'+ana+'/'+chn+'/'+filename,
                                        TARGET=dir+'/'+ana+'/'+chn+'/'+filename,
                                        ))
                        normalize_bbb = ''
                        if not options.drop_normalize_bbb :
                            normalize_bbb = ' --normalize '
                        os.system("add_bbb_errors.py '{CHN}:{PER}:{CAT}:{PROC}' {NORMALIZE} -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold {THR} --AZh".format(
                            DIR=dir,
                            ANA=ana,
                            CHN=chn,
                            PER=per,
                            NORMALIZE=normalize_bbb,
                            CAT=config.bbbcat[chn][per][idx],
                            PROC=config.bbbproc[chn][idx].replace('>',',') if options.new_merging else config.bbbproc[chn][idx],
                            THR=config.bbbthreshold[chn]
                            ))
                        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                            

if options.update_aux :
    print "##"
    print "## update aux directory:"
    print "##"    
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/aux{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        prune = 'bbb' in ana 
        if ':' in ana :
            ana = ana[ana.find(':')+1:]
        print "setup datacards for:", ana, masses
        for chn in config.channels:
            for per in config.periods:
                if config.categories[chn][per]:
                    os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a AZh -c '{CHN}' --AZh-categories-{CHN}='{CATS}' {TWOHDM} {MASSES}".format(
                        CMSSW_BASE=cmssw_base,
                        LABEL=options.label,
                        ANA=ana,
                        DIR=dir,
                        CATS=' '.join(config.categories[chn][per]),
                        CHN=chn,
                        PER=per,
                        TWOHDM= '--twohdm' if options.model=="2HDM" else '',
                        MASSES=' '.join(masses)
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
        if ':' in ana :
            ana = ana[ana.find(':')+1:]
        print "setup limits structure for:", ana
        label = '' #if ana == 'std' else '-l '+ana
        for chn in config.channels:
            for per in config.periods:
                if config.categories[chn][per]:
                    if options.model=='' :
                        os.system("setup-AZh.py -i aux{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a AZh -c '{CHN}' {LABEL} --AZh-categories-{CHN}='{CATS}' {MASSES}".format(
                            INDEX=options.label,                
                            ANA=ana,
                            DIR=dir,
                            LABEL=label,
                            CATS=' '.join(config.categories[chn][per]),
                            CHN=chn,
                            PER=per,
                            MASSES=' '.join(masses)
                            ))
                    else :
                        os.system("setup-AZh.py -i aux{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a AZh -c '{CHN}' {LABEL} --AZh-categories-{CHN}='{CATS}' --model {MODEL} {MASSES}".format(
                            INDEX=options.label,                
                            ANA=ana,
                            DIR=dir,
                            LABEL=label,
                            CATS=' '.join(config.categories[chn][per]),
                            CHN=chn,
                            PER=per,
                            MODEL=options.model,
                            MASSES=' '.join(masses)
                            ))
