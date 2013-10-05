#!/usr/bin/env python
from optparse import OptionParser, OptionGroup
from HiggsAnalysis.HiggsToTauTau.LimitsConfig import configuration
from HiggsAnalysis.HiggsToTauTau.UncertAdaptor import UncertAdaptor
from HiggsAnalysis.HiggsToTauTau.horizontal_morphing import Morph
from HiggsAnalysis.HiggsToTauTau.AsimovDatacard import *
from HiggsAnalysis.HiggsToTauTau.scale2SM import RescaleSamples
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs 
import os

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to reload the Summer13 analysis for the main analyses [bbb, no-bbb] and potential cross check analyses [mvis, incl]. ARGs corresponds to the masses, for which to setup the structure.")
parser.add_option("-a", "--analyses", dest="analyses", default="no-bbb, bbb, bbb:hww-bg",
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"no-bbb, bbb, bbb:hww-bg, mvis, inclusive\" [Default: \"no-bbb, bbb, bbb:hww-bg\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. [Default: \"\"]")
parser.add_option("--ignore-during-scaling", dest="do_not_scales", default="mm vhtt", type="string",
                  help="List of channels, which the scaling by cross seciton times BR shoul not be applied. The list should be embraced by call-ons and separeted by whitespace or comma. [Default: \"vhtt mm\"]")
parser.add_option("--hww-mass", dest="hww_mass", default='', type="string",
                  help="specify this option if you want to fix the hww contributions for the channels em and vhtt to a given mass. This configuration applies to hww as part of the signal. When an empty string is given the mass will be scanned. For analysis hhw-bg, where hww signal contributions are defined as background in any case mH=125 GeV willbe chosenindependent from this configuration. [Default: '']")
parser.add_option("--hww-scale", dest="hww_scale", default='1.', type="string",
                  help="specify the scale factor for the hww contribution here. The scale factor should be relative to the SM expectation. [Default: 1.]")
parser.add_option("--add-0jet-signal", dest="add_0jet_signal", default=False, action="store_true",
                  help="Specify this option to add the signal in the 0jet event categories of the main channels. [Default: False]")
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
parser.add_option("-c", "--config", dest="config", default="",
                  help="Additional configuration file to be used for the setup [Default: \"\"]")

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
config=configuration('sm', options.config, options.add_mutau_soft)

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
    'no-bbb' : '',
    'bbb'    : '',
    'bbb:hww-bg'    : '',
    }

if options.update_all :
    options.update_setup     = True
    options.update_aux       = True
    options.update_limits    = True

masspoints = parseArgs(args)
masspoints = [str(points) for points in masspoints]

print "# --------------------------------------------------------------------------------------"
print "# doSM.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels                :", ' '.join(config.channels)
print "# --periods                 :", ' '.join(config.periods)
print "# --analyses                :", options.analyses
print "# --label                   :", options.label
print "# --drop-list               :", options.drop_list
print "# --ignore-during-scaling   :", options.do_not_scales
print "# --hww-mass                :", 'free' if options.hww_mass == '' else options.hww_mass
print "# --hww-scale               :", options.hww_scale
print "# --add-0jet-signal         :", options.add_0jet_signal
print "# --add-mutau-soft          :", options.add_mutau_soft
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

## add 0jet signal to the main channels
def add_zero_jet(path) :
    """
    Add signal to the 0jet event categories
    """
    cgs_adaptor = UncertAdaptor()
    for channel in config.channels:
        for period in config.periods:
            for category in config.categories[channel][period]:
                if '0jet' in config.categoryname[channel][config.categories[channel][period].index(category)]:
                    filename="{PATH}/{CHANNEL}/cgs-sm-{PERIOD}-{CATEGORY}.conf".format(PATH=path, CHANNEL=channel, PERIOD=period, CATEGORY=category if int(category)>9 else '0'+category)
                    print 'processing file:', filename
                    cgs_adaptor.cgs_processes(filename,['ggH','qqH','VH'])

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
                pattern = ''
                if ana in patterns.keys() :
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
                if chn == 'mt' and options.add_mutau_soft:
                    os.system("cp -v {CMSSW_BASE}/src/auxiliaries/shapes/{DIR}/htt_mt.inputs-sm-8TeV-soft.root {SETUP}/mt/".format(
                        CMSSW_BASE=cmssw_base,
                        DIR=config.inputs['mt_soft'],
                        SOURCE=file,
                        SETUP=setup
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
    if 'mt' in config.channels and options.add_mutau_soft:
        os.system("hadd {SETUP}/mt/htt_mt.inputs-sm-8TeV-bak.root {SETUP}/mt/htt_mt.inputs-sm-8TeV.root {SETUP}/mt/htt_mt.inputs-sm-8TeV-soft.root".format(SETUP=setup))
        os.system("mv {SETUP}/mt/htt_mt.inputs-sm-8TeV-bak.root {SETUP}/mt/htt_mt.inputs-sm-8TeV.root".format(SETUP=setup))
        os.system("rm {SETUP}/mt/htt_mt.inputs-sm-8TeV-soft.root".format(SETUP=setup))
    ## apply horizontal morphing for processes, which have not been simulated for 7TeV: ggH_hww145, qqH_hww145
    for file in glob.glob("{SETUP}/em/htt_em.inputs-sm-7TeV*.root".format(SETUP=setup)) :
        template_morphing = Morph(file, 'emu_0jet_low,emu_0jet_high,emu_1jet_low,emu_1jet_high,emu_vbf_loose', 'ggH_hww{MASS}', 'QCDscale_ggH1in,CMS_scale_e_7TeV', '140,150', 5, True,'') 
        template_morphing.run()
        template_morphing = Morph(file, 'emu_0jet_low,emu_0jet_high,emu_1jet_low,emu_1jet_high,emu_vbf_loose', 'qqH_hww{MASS}', 'CMS_scale_e_7TeV', '140,150', 5, True,'') 
        template_morphing.run()
    ## scale to SM cross section (main processes and all channels tbu those listed in do_not_scales)
    for chn in config.channels :
        for file in glob.glob("{SETUP}/{CHN}/*-sm-*.root".format(SETUP=setup, CHN=chn)) :
            ## vhtt is NOT scaled to 1pb. So nothing needs to be doen here
            if not chn in do_not_scales :
                process = RescaleSamples(file, ['ggH', 'qqH', 'VH', 'WH', 'ZH'], masspoints)
                process.rescale()
    if 'em' in config.channels :
        print "##"
        print "## --->>> adding extra scale for htt_hww contribution in em <<<---"
        print "##"
        ## special treatment for channels which include contributions from hww
        hww_processes = ['ggH_hww', 'qqH_hww']
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
            process = RescaleSamples(file, hww_processes, masspoints)
            process.rescale()
            for proc in hww_processes :
                for mass in masspoints :
                    os.system(r"root -l -b -q {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescaleSignal.C+\(true,{SCALE},\"{INPUTFILE}\",\"{PROCESS}\",0\)".format(
                        CMSSW_BASE=os.environ.get("CMSSW_BASE"),
                        SCALE=hww_over_htt[str(mass)]*float(options.hww_scale),
                        INPUTFILE=file,
                        PROCESS=proc+mass
                        ))
    ## set up directory structure
    dir = "{CMSSW_BASE}/src/setups{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            os.system("rm -r "+dir.replace('src/', 'src/backup/'))
        os.system("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    os.system("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        if 'hww-bg' in ana :
            continue
        os.system("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        ##
        ## CENTRAL
        ##
        if ana == 'no-bbb' :
            print "##"
            print "## update no-bbb directory in setup:"
            print "##"
            if options.add_0jet_signal :
                add_zero_jet(dir+'/'+ana)
        ##
        ## BIN-BY-BIN
        ##
        if ana == 'bbb' :
            print "##"
            print "## update bbb    directory in setup:"
            print "##"    
            if options.add_0jet_signal :
                add_zero_jet(dir+'/'+ana)
            for chn in config.channels:
                for per in config.periods:
                    for idx in range(len(config.bbbcat[chn][per])):
                        os.system("add_bbb_errors.py '{CHN}:{PER}:{CAT}:{PROC}' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold {THR}".format(
                            DIR=dir,
                            ANA=ana,
                            CHN=chn,
                            PER=per,
                            CAT=config.bbbcat[chn][per][idx],
                            PROC=config.bbbproc[chn][idx],
                            THR=config.bbbthreshold[chn]
                            ))
                        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                            
    for ana in analyses :
        if 'hww-bg' in ana :
            os.system("cp -r {DIR}/{SOURCE} {DIR}/{TARGET}".format(DIR=dir, SOURCE=ana[:ana.find(':')], TARGET=ana[ana.find(':')+1:]))
            cgs_adaptor = UncertAdaptor()
            if 'em' in config.channels:
                for period in config.periods:
                    for category in config.categories['em'][period]:
                        filename="{DIR}/{TARGET}/em/cgs-sm-{PERIOD}-0{CATEGORY}.conf".format(DIR=dir, TARGET=ana[ana.find(':')+1:], PERIOD=period, CATEGORY=category)
                        print 'processing file:', filename
                        cgs_adaptor.cgs_processes(filename,None,['ggH_hww','qqH_hww'])
            for file in glob.glob("{DIR}/{TARGET}/em/cgs-sm-*.conf".format(  DIR=dir, TARGET=ana[ana.find(':')+1:])) :
                os.system("perl -pi -e 's/ggH_hww/ggH_hww{MASS}/g' {FILE}".format(MASS='125', FILE=file))
                os.system("perl -pi -e 's/qqH_hww/qqH_hww{MASS}/g' {FILE}".format(MASS='125', FILE=file))
            for file in glob.glob("{DIR}/{TARGET}/em/unc-sm-*.vals".format(  DIR=dir, TARGET=ana[ana.find(':')+1:])) :
                os.system("perl -pi -e 's/ggH_hww/ggH_hww{MASS}/g' {FILE}".format(MASS='125', FILE=file))
                os.system("perl -pi -e 's/qqH_hww/qqH_hww{MASS}/g' {FILE}".format(MASS='125', FILE=file))

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
        print "setup datacards for:", ana
        for chn in config.channels:
            for per in config.periods:
                if config.categories[chn][per]:
                    os.system("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a sm -c '{CHN}' --sm-categories-{CHN}='{CATS}' {MASSES}".format(
                        CMSSW_BASE=cmssw_base,
                        LABEL=options.label,
                        ANA=ana,
                        DIR=dir,
                        CATS=' '.join(config.categories[chn][per]),
                        CHN=chn,
                        PER=per,
                        MASSES=' '.join(masses)
                        ))
        if prune :
            if options.drop_list != '' :
                for subdir in glob.glob("{DIR}/{ANA}/sm/*".format(DIR=dir, ANA=ana)) :
                    print '...comment bbb uncertainties for', subdir
                    os.system("commentUncerts.py --drop-list={DROP} {SUB}".format(DROP=options.drop_list, SUB=subdir))
        ## fix hww mass to a given mass if configured such; do not apply this to hww-bg, where this has been done already at
        ## an earlier level
        if not ana == 'hww-bg' :
            if not options.hww_mass == '' :
                for file in glob.glob("{DIR}/{ANA}/sm/htt_em/htt_em_*.txt".format(DIR=dir, ANA=ana)) :
                    os.system("perl -pi -e 's/ggH_hww/ggH_hww{MASS}/g' {FILE}".format(MASS=options.hww_mass, FILE=file))
                    os.system("perl -pi -e 's/qqH_hww/qqH_hww{MASS}/g' {FILE}".format(MASS=options.hww_mass, FILE=file))
                for file in glob.glob("{DIR}/{ANA}/sm/vhtt/vhtt_*.txt".format(DIR=dir, ANA=ana)) :
                    os.system("perl -pi -e 's/WH_hww/WH_hww{MASS}/g' {FILE}".format(MASS=options.hww_mass, FILE=file))
                    os.system("perl -pi -e 's/ZH_hww/ZH_hww{MASS}/g' {FILE}".format(MASS=options.hww_mass, FILE=file))
        ## fix the problem in the datacards, that the massindex is already contained in the process name
        if not options.hww_mass == '' :
            file = "{DIR}/{ANA}/sm/htt_{em,vhtt}/{htt_em,vhtt}_*.txt".format(DIR=dir, ANA=ana)
            os.system("sed -i -e '/_hww125/ s/$PROCESS$MASS/$PROCESS/g' {FILE}".format(MASS=options.hww_mass, FILE=file))
        ## blind datacards 
        if options.blind_datacards : 
            for chn in channels :
                cardMaker = AsimovDatacard('', True, -1, False, '125', '1.0',options.extra_templates)
                for dir in '{DIR}/{ANA}/sm/{CHN}'.format(DIR=dir, ANA=ana, CHN=chn if chn == 'vhtt' else 'htt_'+chn):
                    cardMaker.cleanup(dir, '_asimov')
                    cardMaker.make_asimov_datacards(dir, False)

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
