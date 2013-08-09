#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.LimitsConfig import configuration
import os

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to reload the Summer13 analysis for the main analyses [bbb, no-bbb] and potential cross check analyses [mvis, incl]. ARGs corresponds to the masses, for which to setup the structure.")
parser.add_option("-a", "--analyses", dest="analyses", default="no-bbb, bbb",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"no-bbb, bbb, mvis, inclusive\" [Default: \"no-bbb, bbb\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--ignore-during-scaling", dest="do_not_scales", default="ee mm vhtt", type="string",
                  help="List of channels, which the scaling by cross seciton times BR shoul not be applied. The list should be embraced by call-ons and separeted by whitespace or comma. [Default: \"vhtt ee mm\"]")
parser.add_option("--add-mutau-soft", dest="add_mutau_soft", default=False, action="store_true",
                  help="Specify this option to add the soft muon pt analysis. [Default: False]")
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
parser.add_option("-c", "--config", dest="config", default="{CMSSW}/src/HiggsAnalysis/HiggsToTauTau/limits.config".format(CMSSW=os.getenv('CMSSW_BASE')),
                  help="Configuration file to be used for the setup [Default: \"\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    #parser.print_usage()
    args.append("110-145:5")
    #exit(1)

import glob 
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

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
config=configuration('sm', options.config)

## define inputs from cvs; Note: not all analyses are available for all inputs
directories = {}
from HiggsAnalysis.HiggsToTauTau.summer13_analyses_cfg import htt_ee, htt_mm, htt_em, htt_et, htt_mt, htt_tt, vhtt
for chn in config.channels:
    if chn != 'vhtt':
        directories[chn] = locals()['htt_'+chn](config.inputs[chn])
    else:
        directories[chn] = locals()[chn](config.inputs[chn])

## postfix pattern for input files
patterns = {
    'no-bbb'   : '',
    'bbb'    : '',
    }

if options.update_all :
    options.update_setup     = True
    options.update_aux       = True
    options.update_limits    = True

print "# --------------------------------------------------------------------------------------"
print "# doSM.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels        :", config.channels
print "# --periods         :", config.periods
print "# --analyses        :", options.analyses
print "# --label           :", options.label
print "# --drop-list       :", options.drop_list
print "# --do-not-scales   :", options.do_not_scales
print "# --add-mutau-soft  :", options.add_mutau_soft
print "# --------------------------------------------------------------------------------------"
for chn in config.channels:
    print "# --inputs-"+chn+"       :", config.inputs[chn]
print "# --------------------------------------------------------------------------------------"
print "# --update-setup    :", options.update_setup
print "# --update-aux      :", options.update_aux
print "# --update-LIMITS   :", options.update_limits
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
    os.system("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))

    for chn in config.channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{SETUP}/{CHN}/*inputs-sm-*.root".format(SETUP=setup, CHN=chn)) :
            os.system("rm %s" % file)
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = patterns[ana]
                source="{CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/{CHN}.inputs-sm-{PER}{PATTERN}.root".format(
                    CMSSW_BASE=cmssw_base,
                    DIR=directories[chn][per],
                    CHN=chn+'_*' if chn == 'vhtt' else 'htt_'+chn,
                    PER=per,
                    PATTERN=pattern
                    )
                for file in glob.glob(source) :
                    os.system("cp -v {SOURCE} {SETUP}/{CHN}/".format(
                        SOURCE=file,
                        SETUP=setup,
                        CHN=chn
                        ))
    if 'vhtt' in config.channels :
        for per in config.periods :
            if directories['vhtt'][per] == 'None' :
                continue
            for ana in analyses :
                pattern = patterns[ana]
                if not os.path.exists("{SETUP}/vhtt/vhtt.inputs-sm-{PER}{PATTERN}.root".format(SETUP=setup, PER=per, PATTERN=pattern)):
                    os.system("hadd {SETUP}/vhtt/vhtt.inputs-sm-{PER}{PATTERN}.root {SETUP}/vhtt/vhtt_*.inputs-sm-{PER}{PATTERN}.root".format(
                        SETUP=setup,
                        PER=per,
                        PATTERN=pattern
                        ))
                    os.system("rm {SETUP}/vhtt/vhtt_*.inputs-sm-{PER}{PATTERN}.root".format(
                        SETUP=setup,
                        PER=per,
                        PATTERN=pattern
                        ))
    ## scale to SM cross section
    for chn in config.channels :
        for file in glob.glob("{SETUP}/{CHN}/*-sm-*.root".format(SETUP=setup, CHN=chn)) :
            ## vhtt is NOT scaled to 1pb. So nothing needs to be doen here
            if not chn in do_not_scales :
                os.system("scale2SM.py -i {FILE} -s 'ggH, qqH, VH, WH, ZH' {MASSES}".format(
                    FILE=file,
                    MASSES=' '.join(masses)
                    ))
    if 'em' in config.channels : ## move back to XYZ->em
        print "##"
        print "## --->>> adding extra scale for htt_hww contribution in em <<<---"
        print "##"
        ## special treatment for channels which include contributions from hww
        hww_processes = ['ggH_hww', 'qqH_hww', 'VH_hww']
        ## BR ratios: hww/htt as function of the mass
        hww_over_htt = {
            # mass     hww    htt  WW->2l2v
            '90'  : 0.00209/0.0841*3*0.108*3*0.108,
            '95'  : 0.00472/0.0841*3*0.108*3*0.108,
            '100' : 0.01110/0.0836*3*0.108*3*0.108,
            '105' : 0.02430/0.0825*3*0.108*3*0.108,
            '110' : 0.04820/0.0802*3*0.108*3*0.108,
            '115' : 0.08670/0.0765*3*0.108*3*0.108,
            '120' : 0.14300/0.0710*3*0.108*3*0.108,
            '125' : 0.21600/0.0637*3*0.108*3*0.108,
            '130' : 0.30500/0.0548*3*0.108*3*0.108,
            '135' : 0.40300/0.0452*3*0.108*3*0.108,
            '140' : 0.50300/0.0354*3*0.108*3*0.108,
            '145' : 0.60200/0.0261*3*0.108*3*0.108,
            }
        ## multiply with proper xsec and correct for proper BR everywhere, where any of the above processes occurs
        for file in glob.glob("{SETUP}/em/*inputs-sm-*.root".format(SETUP=setup)) :
            os.system("scale2SM.py -i {FILE} -s '{PROCS}' {MASSES}".format(
                FILE=file,
                PROCS=', '.join(hww_processes),
                MASSES=' '.join(masses)
                ))
            for proc in hww_processes :
                for mass in parseArgs(masses) :
                    os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{SCALE},\"{INPUTFILE}\",\"{PROCESS}\",0\)".format(
                        CMSSW_BASE=os.environ.get("CMSSW_BASE"),
                        SCALE=hww_over_htt[str(mass)],
                        INPUTFILE=file,
                        PROCESS=proc+str(mass)
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
                    if chn not in ['et', 'mt', 'vhtt']:
                        if len(config.bbbcat[chn][per])>0: #make sure there are categories for this period (maybe unnecessary)
                            os.system("add_bbb_errors.py '{CHN}:{PER}:{CAT}:{PROC}' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold {THR}".format(
                                DIR=dir,
                                ANA=ana,
                                CHN=chn,
                                PER=per,
                                PROC=config.bbbproc[chn],
                                CAT=config.bbbcat[chn][per],
                                THR=config.bbbthreshold
                                ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                            

            if 'et' in config.channels :
                if '7TeV' in config.periods :
                    ## setup bbb uncertainties for et 7TeV
                    os.system("add_bbb_errors.py 'et:7TeV:01,02,04,05,06:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                if '8TeV' in config.periods :
                    ## setup bbb uncertainties for et 8TeV
                    os.system("add_bbb_errors.py 'et:8TeV:01,02,04,05,06,07:ZL,ZJ,QCD>W'  --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
            if 'mt' in config.channels :
                if '7TeV' in config.periods :
                    ## setup bbb uncertainties for mt 7TeV
                    os.system("add_bbb_errors.py 'mt:7TeV:01,02,04,05,06:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                if '8TeV' in config.periods :
                    ## setup bbb uncertainties for mt 8TeV
                    os.system("add_bbb_errors.py 'mt:8TeV:01,02,04,05,06,07{SOFT}:ZL,ZJ,QCD>W'  --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana,
                        SOFT=',10,11,12,13,15,16' if options.add_mutau_soft else ''                        
                        ))
                os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                
            if 'vhtt' in config.channels :
                if '7TeV' in config.periods :
                    ## setup bbb uncertainties for vhtt
                    os.system("add_bbb_errors.py 'vhtt:7TeV:00:fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:01:fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    #os.system("add_bbb_errors.py 'vhtt:7TeV:02:fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                    #    DIR=dir,
                    #    ANA=ana
                    #    ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:03:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:04:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:05:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:06:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:07:wz' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:7TeV:08:wz' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                if '8TeV' in config.periods :
                    ## setup bbb uncertainties for vhtt
                    os.system("add_bbb_errors.py 'vhtt:8TeV:00:fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:01:fakes,charge_fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:02:fakes,charge_fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:03:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:04:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:05:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:06:Zjets' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:07:wz' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
                        ))
                    os.system("add_bbb_errors.py 'vhtt:8TeV:08:wz' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
                        DIR=dir,
                        ANA=ana
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
        print "setup datacards for:", ana
        for chn in config.channels:
            for per in config.periods:
                if len(config.categories[chn][per])>0: #make sure there are categories for this period (maybe unnecessary)
                    os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c {CHN} --sm-categories-{CHN}='{CATS}' {MASSES}".format(
                        LABEL=options.label,
                        CMSSW_BASE=cmssw_base,
                        ANA=ana,
                        DIR=dir,
                        CATS=' '.join(config.categories[chn][per]),
                        CHN=chn,
                        PER=per,
                        MASSES=' '.join(masses)
                        ))
        if ana == 'bbb' :
            if options.drop_list != '' :
                for subdir in glob.glob("{DIR}/bbb/sm/*".format(DIR=dir)) :
                    print '...comment bbb uncertainties for', subdir
                    os.system("commentUncerts.py --drop-list={DROP} {SUB}".format(DROP=options.drop_list, SUB=subdir))

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
        label = '' #if ana == 'std' else '-l '+ana

        for chn in config.channels:
            for per in config.periods:
                if len(config.categories[chn][per])>0: #make sure there are categories for this period (maybe unnecessary)
                    os.system("setup-htt.py -i aux{INDEX}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' {LABEL} --sm-categories-{CHN}='{CATS}' {MASSES}".format(
                        INDEX=options.label,                
                        ANA=ana,
                        DIR=dir,
                        LABEL=label,
                        CATS=' '.join(config.categories[chn][per]),
                        CHN=chn,
                        PER=per,
                        MASSES=' '.join(masses)
                        ))
