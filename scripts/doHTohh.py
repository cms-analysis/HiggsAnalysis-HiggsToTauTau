#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.LimitsConfig import configuration
from HiggsAnalysis.HiggsToTauTau.UncertAdaptor import UncertAdaptor ###NEW
from HiggsAnalysis.HiggsToTauTau.DatacardAdaptor import DatacardAdaptor
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup all datacards and directories.'")
parser.add_option("-a", "--analyses", dest="analyses", default="bbb, plain",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"bbb, plain\" [Default: \"bbb, plain\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. [Default: \"\"]")
parser.add_option("--reload", dest="reload", default=False, action="store_true",
                  help="reload all root input files from the github in a setup directory. [Default: False]")
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
parser.add_option("--new-merging", dest="new_merging", default=False, action="store_true",
                  help="added to test the new merging introduced by Andrew. [Default: False]")
parser.add_option("--new-merging-threshold", dest="new_merging_threshold", default="0.5", type="string",
                  help="Threshold for the new merging by Andrew. [Default: \"0.5\"]")
parser.add_option("--drop-normalize-bbb", dest="drop_normalize_bbb", default=False, action="store_true",
                  help="Normalize yield to stay constand when adding bbb shape uncertainties. [Default: False]")
parser.add_option("--profile", dest="profile", default=False, action="store_true",
                  help="Add extra signals bbH and A->Zh for profiling. [Default: False]")
parser.add_option("-c", "--config", dest="config", default="",
                  help="Additional configuration file to be used for the setup [Default: \"\"]")

(options, args) = parser.parse_args()
if len(args) < 1 :
    args.append("260-350:10")

import os
import glob 
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs
from HiggsAnalysis.HiggsToTauTau.utils import get_channel_dirs

## masses
masses = args
for idx in range(len(masses)) : masses[idx] = masses[idx].rstrip(',')
## analyses
analyses = options.analyses.split()
analyses_save = analyses
for idx in range(len(analyses)) : analyses[idx] = analyses[idx].rstrip(',')
## CMSSW_BASE
cmssw_base=os.environ['CMSSW_BASE']
## setup a backup directory
os.system("mkdir -p backup")
## configuration
config=configuration('Hhh', options.config)

##define inputs from git; Note: not all analyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.summer13_analyses_cfg import htt_mm, htt_em, htt_et, htt_mt, htt_tt, htt_tt
for chn in config.channels :
    directories[chn] = locals()['htt_'+chn](config.inputs[chn])

## postfix pattern for input files
patterns = {
    'plain'        : {'em': '', 'et' : '', 'mt' : '', 'tt' : '', 'mm' : ''},
    'bbb'          : {'em': '', 'et' : '', 'mt' : '', 'tt' : '', 'mm' : ''},
    }

if options.update_all :
    options.reload        = True
    options.update_setup  = True
    options.update_aux    = True
    options.update_limits = True

print "# --------------------------------------------------------------------------------------"
print "# doHhh.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels                :", ' '.join(config.channels)
print "# --periods                 :", ' '.join(config.periods)
print "# --analyses                :", options.analyses
print "# --label                   :", options.label
print "# --blind-datacards         :", options.blind_datacards
print "# --extra-templates         :", options.extra_templates
print "# --------------------------------------------------------------------------------------"
for chn in config.channels:
    print "# --inputs-"+chn+"               :", config.inputs[chn]
print "# --------------------------------------------------------------------------------------"
print "# --reload                  :", options.reload
print "# --update-setup            :", options.update_setup
print "# --update-aux              :", options.update_aux
print "# --update-LIMITS           :", options.update_limits
print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
print "# guration parameters.                           "
print "# --------------------------------------------------------------------------------------"

## setup main directory
setup="{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)

if options.reload :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## remove existing cash
    if os.path.exists("{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)):
        os.system("rm -r {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))
    os.system("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup-Hhh{PROFILE} {CMSSW_BASE}/src/.setup{LABEL}".format(PROFILE="-profile" if options.profile else "", CMSSW_BASE=cmssw_base, LABEL=options.label))
    for chn in config.channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{SETUP}/{CHN}/*inputs-Hhh-*.root".format(SETUP=setup, CHN=chn)) :
            os.system("rm %s" % file)        
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = ''
                if ana in patterns.keys() :
                    pattern = patterns[ana][chn]
                print pattern
                input ="{CHN}.inputs-Hhh-{PER}{PATTERN}.root".format(
                    CHN='htt_'+chn,
                    PER=per,
                    PATTERN=pattern,
                    )
                output="{CHN}.inputs-Hhh-{PER}.root".format(
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

if options.update_setup :
    ## scale by acceptance correction. This needs to be done for all available masses independent
    ## from args to guarantee that the tanb_grid templates are properly scaled.
    for chn in config.channels : #felix
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            if not options.profile :
                continue
            os.system("scale2accept.py -i {SETUP} -c '{CHN}' -p '{PER}' -a 'Hhh' 90 100-200:20 130 250-400:50".format(
                SETUP=setup,
                CHN=chn,
                PER=per,
                ))

            ## apply horizontal template morphing for finer step sizes for limit calculation
            if per != "8TeV":
                continue

            unc = {"em": "CMS_scale_e_8TeV",
                   "et": "CMS_scale_t_etau_8TeV, CMS_scale_j_8TeV",
                   "mt": "CMS_scale_t_mutau_8TeV, CMS_scale_j_8TeV",
                   "tt": "CMS_scale_t_tautau_8TeV",
                   }[chn]

            massStrings = {"em": ["'250,300'", "'300,350'"],
                           "et": ["'250,300'", "'300,350'"],
                           "mt": ["'250,300'", "'300,350'"],
                           "tt": ["'250,350'"],
                           }[chn]

            categoryPrefix = {"em": "emu",
                              "et": "eleTau",
                              "mt": "muTau",
                              "tt": "tauTau",
                              }[chn]
            categoryList = ','.join(["%s_%s" % (categoryPrefix, cat) for cat in config.categoryname[chn][per]])

            args = ["--categories='%s'" % categoryList,
                    "--samples='bbH{MASS}'".format(MASS="{MASS}"),
                    "--step-size 10. -v",
                    "--uncerts='%s'" % unc,
                    " {SETUP}/{CHN}/htt_{CHN}.inputs-Hhh-8TeV.root".format(SETUP=setup, CHN=chn),
                    ]
            for massString in massStrings:
                cmd = " ".join(["horizontal-morphing.py", "--masses=%s" % massString] + args)
                #print cmd
                os.system(cmd)


    ## setup directory structure
    dir = "{CMSSW_BASE}/src/setups{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        if ana == 'plain' :
            print "##"
            print "## update no-bbb directory in setup:"
            print "##"
        if 'bbb' in ana :
            print "##"
            print "## update bbb    directory in setup:"
            print "##"
            for chn in config.channels:
                for per in config.periods:
                    for idx in range(len(config.bbbcat[chn][per])):
                        if options.new_merging :
                            filename='htt_'+chn+'.inputs-Hhh-'+per+'.root'
                            for cat in config.bbbcat[chn][per][idx].split(',') :
                                print cat
                                ## loop all categories in question for index idx
                                if len(config.bbbproc[chn][idx].replace('>','+').split('+'))>1 :
                                    ## only get into action if there is more than one sample to do the merging for
                                    os.system("merge_bin_errors.py --folder {DIR} --processes {PROC} --bbb_threshold={BBBTHR} --merge_threshold={THRESH} --verbose {SOURCE} {TARGET}".format(
                                        ## this list has only one entry by construction
                                        DIR=get_channel_dirs("Hhh",chn, cat,per)[0],
                                        PROC=config.bbbproc[chn][idx].split(',')[0].replace('>',','),
                                        BBBTHR=config.bbbthreshold[chn],
                                        THRESH=options.new_merging_threshold,
                                        SOURCE=dir+'/'+ana+'/'+chn+'/'+filename,
                                        TARGET=dir+'/'+ana+'/'+chn+'/'+filename,
                                        ))
                        normalize_bbb = ''
                        if not options.drop_normalize_bbb :
                            normalize_bbb = ' --normalize '
                        os.system("add_bbb_errors.py '{CHN}:{PER}:{CAT}:{PROC}' {NORMALIZE} -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold {THR} --Hhh".format(
                            DIR=dir,
                            ANA=ana,
                            CHN=chn,
                            PER=per,
                            NORMALIZE=normalize_bbb,
                            CAT=config.bbbcat[chn][per][idx],
                            PROC=config.bbbproc[chn][idx].replace('>',','),
                            THR=config.bbbthreshold[chn]
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
        for chn in config.channels:
            for per in config.periods: 
                if config.categories[chn][per]:
                    os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a Hhh -c '{CHN}' --Hhh-categories-{CHN}='{CATS}' {MASSES}".format(
                    CMSSW_BASE=cmssw_base,
                    LABEL=options.label,
                    ANA=ana,
                    DIR=dir,
                    PER=per,
                    CHN=chn,
                    CATS=' '.join(config.categories[chn][per]),
                    MASSES=' '.join(masses),
                    ))
        if 'bbb' in ana :
            if options.drop_list != '' :
                for subdir in glob.glob("{DIR}/{ANA}/Hhh/*".format(DIR=dir, ANA=ana)) :
                    print '...comment bbb uncertainties for', subdir
                    os.system("python HiggsAnalysis/CombinedLimit/scripts/commentUncerts.py --drop-list={DROP} {SUB}".format(DROP=options.drop_list, SUB=subdir))
    print "analyses", analyses  
    ## blind datacards
    if options.blind_datacards :
        for ana in analyses : 
            os.system("cp -r {DIR}/{ANA} {DIR}/{ANA}-asimov".format(DIR=dir,ANA=ana))
            for chn in config.channels :
                os.system("blindData.py --update-file --extra-templates '{EXTRA_TEMPLATES}' {DIR}/{ANA}-asimov/Hhh/{CHN}".format(
                    EXTRA_TEMPLATES = '' if "-SMHbkg" in ana else options.extra_templates,
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
        for chn in config.channels:
            for per in config.periods:
                if config.categories[chn][per]:
                    os.system("setup-Hhh.py -i aux{INDEX}/{ANA}{ASIMOV} -o {DIR}/{ANA}{ASIMOV} -p '{PER}' -a Hhh -c '{CHN}' {CATS} {MASSES}".format(
                        INDEX=options.label,                
                        ANA=ana,
                        ASIMOV='-asimov' if options.blind_datacards else '',
                        DIR=dir,
                        PER=per,
                        CHN=chn,
                        CATS="--Hhh-categories-%s='%s'" % (chn, " ".join(config.categories[chn][per])),
                        MASSES=' '.join(masses),
                        ))
