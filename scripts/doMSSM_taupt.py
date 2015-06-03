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
                  help="Type of analyses to be considered for updating. Lower case is required. Possible choices are: \"bbb, plain, tail-bbb\" [Default: \"bbb, plain\"]")
parser.add_option("--label", dest="label", default="", type="string", 
                  help="Possibility to give the setups, aux and LIMITS directory a index (example LIMITS-bbb). [Default: \"\"]")
parser.add_option("--tail-fitting", dest="fit_tails", default=False, action="store_true",
                  help="Fitting of the MSSM m(tautau) tails for predefined backgrounds [Default: False]")
parser.add_option("--fine-binning", dest="fine_binning", default=False, action="store_true",
                  help="Use finer binning for limit inputs. [Default: False]")
parser.add_option("--merge-bbb", dest="merge_bbb", default=False, action="store_true",
                  help="Merge bin-by-bin uncertainties according to Barlow-Beeston approach. [Default: False]")
parser.add_option("--fine-scan", dest="fine_scan", default=False, action="store_true",
                  help="Create a grid of pivotals with distance of 10 Gev in the range from 90 Gev to 250 GeV to allow for a finer scan of the low mass region. [Default: False]")
parser.add_option("--SMHasBackground", dest="SMHasBackground", default=False, action="store_true",
                  help="Add the SM Higgs to the background. [Default: False]")
parser.add_option("--SMHasSignal", dest="SMHasSignal", default=False, action="store_true",
                  help="Shift the SM Higgs from background to the signal. This is normally needed for the signal hypothesis separation test. The options SMHasBackground has to be true [Default: False]")
parser.add_option("--blind-datacards", dest="blind_datacards", default=False, action="store_true",
                  help="Option to blind datacards. Also needs to be turned on to inject SM to datacards. [Default: False]")
parser.add_option("--extra-templates", dest="extra_templates", default="", type="string", help="List of extra background or signal templates which should be injected to the asimov dataset. Needs to be comma seperated list. Here used to inject SM signal into MSSM datacards. In addition, you can use a scale for each template, e.g. '2.5*ggH_SM125'. The scale number should be left from the template name and is separated from it with a multiplication sign '*'. [Default: \"\"]")
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
parser.add_option("-c", "--config", dest="config", default="",
                  help="Additional configuration file to be used for the setup [Default: \"\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    #parser.print_usage()
    if not options.fine_scan:
        args.append("90 130 100_200:20 250_500:50 600_1000:100")
    else :
        args.append("90_250:10 275_500:25 550_1000:50")
        #args.append("90 100_180:5 200 250_500:50 600_1000:100")
    #exit(1)

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
config=configuration('mssm', options.config)

## define inputs from git; Note: not all analyses are available for all inputs
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
print "# doMSSM.py "
print "# --------------------------------------------------------------------------------------"
print "# You are using the following configuration: "
print "# --channels                :", ' '.join(config.channels)
print "# --periods                 :", ' '.join(config.periods)
print "# --analyses                :", options.analyses
print "# --label                   :", options.label
print "# --drop-list               :", options.drop_list
print "# --tail-fitting            :", options.fit_tails
print "# --fine-binning            :", options.fine_binning
print "# --merge-bbb               :", options.merge_bbb
print "# --new-merging             :", options.new_merging
print "# --new-merging-threshold   :", options.new_merging_threshold
print "# --drop-bbb-normalisation  :", options.drop_normalize_bbb
print "# --fine-scan               :", options.fine_scan
print "# --blind-datacards         :", options.blind_datacards
print "# --extra-templates         :", options.extra_templates
print "# --SMHasBackground         :", options.SMHasBackground
print "# --SMHasSignal             :", options.SMHasSignal
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
setup = "{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)

import time
def runCommand(command):
    print "Executing '%s'" % command
    print " It is now: %s" % time.strftime("%c")
    os.system(command)

if options.reload :
    print "##"
    print "## update input files from cvs:"
    print "##"
    ## remove existing cash
    if os.path.exists("{CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)):
        runCommand("rm -r {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))
    runCommand("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup {CMSSW_BASE}/src/.setup{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label))

    for chn in config.channels :
        print "... copy files for channel:", chn
        ## remove legacy
        for file in glob.glob("{SETUP}/{CHN}/*inputs-mssm-*.root".format(SETUP=setup, CHN=chn)) :
            runCommand("rm %s" % file)        
        ## define postfix for tail fitting
        tailfit = ''
        if options.fine_binning :
            if chn != 'mm' :
                tailfit = '-fb'
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            for ana in analyses :
                pattern = ''
                if ana in patterns.keys() :
                    pattern = patterns[ana][chn]
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
                        runCommand("cp -v {SOURCE} {SETUP}/{CHN}/{FILE}".format(
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
                        runCommand("cp -v {SOURCE} {SETUP}/{CHN}/{FILE}".format(
                            SOURCE=file,
                            SETUP=setup,
                            CHN=chn,
                            FILE=output,
                            ))
if options.update_setup :
    ## scale by acceptance correction. This needs to be done for all available masses independent
    ## from args to guarantee that the tanb_grid templates are properly scaled.
    for chn in config.channels : 
        for per in config.periods :
            if directories[chn][per] == 'None' :
                continue
            runCommand("scale2accept.py -i {SETUP} -c '{CHN}' -p '{PER}' 90 100_200:20 130 250_500:50 600_1000:100".format(
                SETUP=setup,
                CHN=chn,
                PER=per,
                ))
    ## apply horizontal template morphing for finer step sizes for limit calculation
    if options.fine_scan :
        ##em
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_7TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/em/htt_em.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_8TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/em/htt_em.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))        
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_7TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/em/htt_em.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_8TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/em/htt_em.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_7TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/em/htt_em.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='emu_btag,emu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_e_8TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/em/htt_em.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        ##et
        runCommand("horizontal-morphing.py --categories='eleTau_btag,eleTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_7TeV,CMS_eff_t_mssmHigh_etau_7TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/et/htt_et.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='eleTau_btag_low,btag_high,eleTau_nobtag_low,eleTau_nobtag_medium,eleTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_8TeV,CMS_eff_t_mssmHigh_etau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/et/htt_et.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='eleTau_btag,eleTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_7TeV,CMS_eff_t_mssmHigh_etau_7TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/et/htt_et.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='eleTau_btag_low,btag_high,eleTau_nobtag_low,eleTau_nobtag_medium,eleTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_8TeV,CMS_eff_t_mssmHigh_etau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/et/htt_et.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='eleTau_btag,eleTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_7TeV,CMS_eff_t_mssmHigh_etau_7TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/et/htt_et.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='eleTau_btag_low,btag_high,eleTau_nobtag_low,eleTau_nobtag_medium,eleTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_etau_8TeV,CMS_eff_t_mssmHigh_etau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/et/htt_et.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        ##mt
        runCommand("horizontal-morphing.py --categories='muTau_btag,muTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_7TeV,CMS_eff_t_mssmHigh_mutau_7TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/mt/htt_mt.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='muTau_btag_low,muTau_btag_high,muTau_nobtag_low,muTau_nobtag_medium,muTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_8TeV,CMS_eff_t_mssmHigh_mutau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/mt/htt_mt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='muTau_btag,muTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_7TeV,CMS_eff_t_mssmHigh_mutau_7TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/mt/htt_mt.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='muTau_btag_low,muTau_btag_high,muTau_nobtag_low,muTau_nobtag_medium,muTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_8TeV,CMS_eff_t_mssmHigh_mutau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/mt/htt_mt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='muTau_btag,muTau_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_7TeV,CMS_eff_t_mssmHigh_mutau_7TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/mt/htt_mt.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='muTau_btag_low,muTau_btag_high,muTau_nobtag_low,muTau_nobtag_medium,muTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_mutau_8TeV,CMS_eff_t_mssmHigh_mutau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/mt/htt_mt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        ##tt
        runCommand("horizontal-morphing.py --categories='tauTau_btag_low,tauTau_btag_high,tauTau_nobtag_low,tauTau_nobtag_medium,tauTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_tautau_8TeV,CMS_eff_t_mssmHigh_tautau_8TeV,CMS_htt_higgsPtReweight_8TeV,'CMS_htt_higgsPtReweight_scale_8TeV --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/tt/htt_tt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='tauTau_btag_low,tauTau_btag_high,tauTau_nobtag_low,tauTau_nobtag_medium,tauTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_tautau_8TeV,CMS_eff_t_mssmHigh_tautau_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/tt/htt_tt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --categories='tauTau_btag_low,tauTau_btag_high,tauTau_nobtag_low,tauTau_nobtag_medium,tauTau_nobtag_high' --samples='ggH{MASS},bbH{MASS}' --uncerts='CMS_scale_t_tautau_8TeV,CMS_eff_t_mssmHigh_tautau_8TeV,CMS_htt_higgsPtReweight_8TeV,CMS_htt_higgsPtReweight_scale_8TeV' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/tt/htt_tt.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        ##mm
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/mm/htt_mm.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='100,120,130,140,160,180,200,250' --step-size 10. -v {SETUP}/mm/htt_mm.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/mm/htt_mm.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='250,300,350,400,450,500' --step-size 25. -v {SETUP}/mm/htt_mm.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/mm/htt_mm.inputs-mssm-7TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
        runCommand("horizontal-morphing.py --trivial --categories='mumu_btag,mumu_nobtag' --samples='ggH{MASS},bbH{MASS}' --uncerts='' --masses='500,600,700,800,900,1000' --step-size 50. -v {SETUP}/mm/htt_mm.inputs-mssm-8TeV-0.root".format(SETUP=setup, MASS="{MASS}"))
    ## setup directory structure
    dir = "{CMSSW_BASE}/src/setups{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            runCommand("rm -r "+dir.replace('src/', 'src/backup/'))
        runCommand("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    runCommand("mkdir -p {DIR}".format(DIR=dir))
    for ana in analyses :
        runCommand("cp -r {SETUP} {DIR}/{ANA}".format(SETUP=setup, DIR=dir, ANA=ana))
        if options.fit_tails:     
            if '7TeV' in config.periods :
                if 'em' in config.channels :
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'Fakes_fine_binning' -k '8' --range 150  ".format( 
                    #    DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'EWK_fine_binning' -k '9' --range 200  ".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'EWK_fine_binning' -k '8' --range 200  ".format(
                        DIR=dir, ANA=ana))
                    ## runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning' -k '9' --range 200  ".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning' -k '8' --range 200 ".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_nobtag_7TeVDown' -k '8' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_nobtag_7TeVUp'   -k '8' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_btag_7TeVDown' -k '9' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-7TeV-0.root -c em -e 7TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_btag_7TeVUp'   -k '9' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
                if 'et' in config.channels :
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_fine_binning' -k '8' --range 200 ".format(
                         DIR=dir, ANA=ana))                     
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_fine_binning' -k '8' --range 200 ".format(
                         DIR=dir, ANA=ana)) 
                    ## tail fit for QCD shape uncertainties
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_7TeVDown_fine_binning' -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_7TeVUp_fine_binning'   -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_CMS_htt_WShape_etau_nobtag_7TeVDown_fine_binning' -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_CMS_htt_WShape_etau_nobtag_7TeVUp_fine_binning'   -k '8' --range 200 --no-uncerts".format(
                         DIR=dir, ANA=ana))
                     #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_CMS_htt_WShape_etau_btag_7TeVDown_fine_binning' -k '9' --range 200 --no-uncerts".format(
                     #    DIR=dir, ANA=ana))
                     #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-7TeV-0.root -c et -e 7TeV -b 'W_CMS_htt_WShape_etau_btag_7TeVUp_fine_binning'   -k '9' --range 200 --no-uncerts".format(
                     #    DIR=dir, ANA=ana))
                if 'mt' in config.channels :
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_fine_binning' -k '9' --range 120".format(
                    #    DIR=dir, ANA=ana))
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_fine_binning' -k '8' --range 150 --rangelast 700 ".format(
                    #    DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_fine_binning' -k '8' --range 300 ".format(
                        DIR=dir, ANA=ana))
                    ## tail fit for QCD shape uncertainties
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_7TeVDown_fine_binning' -k '8' --range 150 --rangelast 700 --no-uncerts".format(
                   #     DIR=dir, ANA=ana))
                   # runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_7TeVUp_fine_binning'   -k '8' --range 150 --rangelast 700 --no-uncerts".format(
                   #     DIR=dir, ANA=ana))
                   # runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_7TeVDown_fine_binning' -k '9' --range 120  --no-uncerts".format(
                   #     DIR=dir, ANA=ana))
                   # runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_7TeVUp_fine_binning'   -k '9' --range 120  --no-uncerts".format(
                   #     DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_CMS_htt_WShape_mutau_nobtag_7TeVDown_fine_binning' -k '8' --range 300 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_CMS_htt_WShape_mutau_nobtag_7TeVUp_fine_binning'   -k '8' --range 300 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_CMS_htt_WShape_mutau_btag_7TeVDown_fine_binning' -k '9' --range 200 --no-uncerts".format(
                    #    DIR=dir, ANA=ana))
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-7TeV-0.root -c mt -e 7TeV -b 'W_CMS_htt_WShape_mutau_btag_7TeVUp_fine_binning'   -k '9' --range 200 --no-uncerts".format(
                    #    DIR=dir, ANA=ana))           
            if "8TeV" in config.periods :
                if 'em' in config.channels :
                    #runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'Fakes_fine_binning' -k '8' --range 200  ".format( 
                    #    DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'EWK_fine_binning' -k '9' --range 200  ".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'EWK_fine_binning' -k '8' --range 200 " .format(
                        DIR=dir, ANA=ana))
                    ## runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning' -k '9' --range 200  ".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning' -k '8' --range 200 ".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_nobtag_8TeVDown' -k '8' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_nobtag_8TeVUp'   -k '8' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_btag_8TeVDown' -k '9' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
##                     runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_em.inputs-mssm-8TeV-0.root -c em -e 8TeV -b 'ttbar_fine_binning_CMS_htt_TTbarShape_em_btag_8TeVUp'   -k '9' --range 200 --no-uncerts".format(
##                         DIR=dir, ANA=ana))
                if 'et' in config.channels :
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    ##raise ValueError("STOP.")
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '10' --range 200 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '11' --range 220 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_fine_binning' -k '12' --range 220 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '13' --range 200 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '14' --range 200 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '10' --range 240 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '11' --range 240 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_fine_binning' -k '12' --range 325 --rangelast 1500 --fitoption 1 --fitmodel 1 --erroroption 1".format(                        
                        DIR=dir, ANA=ana))
                    ## tail fit for QCD shape uncertainties
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVDown_fine_binning' -k '10' --range 200 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVUp_fine_binning'   -k '10' --range 200 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVDown_fine_binning' -k '11' --range 220 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVUp_fine_binning'   -k '11' --range 220 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVDown_fine_binning' -k '12' --range 220 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVUp_fine_binning'  -k '12' --range 220 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVDown_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVUp_fine_binning'   -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVDown_fine_binning' -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_etau_8TeVUp_fine_binning'   -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_low_8TeVDown_fine_binning' -k '10' --range 200 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_low_8TeVUp_fine_binning'   -k '10' --range 200 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_medium_8TeVDown_fine_binning' -k '11' --range 220 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_medium_8TeVUp_fine_binning'   -k '11' --range 220 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_high_8TeVDown_fine_binning' -k '12' --range 220 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_nobtag_high_8TeVUp_fine_binning'   -k '12' --range 220 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_low_8TeVDown_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_low_8TeVUp_fine_binning'   -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_high_8TeVDown_fine_binning' -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'QCD_CMS_htt_QCDShape_etau_btag_high_8TeVUp_fine_binning'   -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_low_8TeVDown_fine_binning' -k '10' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_low_8TeVUp_fine_binning'   -k '10' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_medium_8TeVDown_fine_binning' -k '11' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_medium_8TeVUp_fine_binning'   -k '11' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_high_8TeVDown_fine_binning' -k '12' --range 325 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_nobtag_high_8TeVUp_fine_binning'   -k '12' --range 325 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_btag_low_8TeVDown_fine_binning' -k '13' --range 200 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_btag_low_8TeVUp_fine_binning'   -k '13' --range 200 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_btag_high_8TeVDown_fine_binning' -k '14' --range 250 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_et.inputs-mssm-8TeV-0.root -c et -e 8TeV -b 'W_CMS_htt_WShape_etau_btag_high_8TeVUp_fine_binning'   -k '14' --range 250 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                if 'mt' in config.channels : 
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '14' --range 180 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '10' --range 280 --rangelast 600 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '11' --range 260 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_fine_binning' -k '12' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                       DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '13' --range 200 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '14' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '10' --range 240 --rangelast 1500 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '11' --range 240 --rangelast 1500 --fitoption 1 --fitmodel 1 --erroroption 1".format( 
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_fine_binning' -k '12' --range 325 --rangelast 1500 --fitoption 1 --fitmodel 1 --erroroption 1".format( 
                        DIR=dir, ANA=ana))
                    ## tail fit for QCD shape uncertainties
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVDown_fine_binning' -k '10' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVUp_fine_binning' -k '10' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVDown_fine_binning' -k '11' --range 260 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVUp_fine_binning'   -k '11' --range 260 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVDown_fine_binning' -k '12' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVUp_fine_binning'   -k '12' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVDown_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVUp_fine_binning'   -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVDown_fine_binning' -k '14' --range 200 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_mutau_8TeVUp_fine_binning'   -k '14' --range 200 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_low_8TeVDown_fine_binning' -k '10' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_low_8TeVUp_fine_binning' -k '10' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_medium_8TeVDown_fine_binning' -k '11' --range 260 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_medium_8TeVUp_fine_binning'   -k '11' --range 260 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_high_8TeVDown_fine_binning' -k '12' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_nobtag_high_8TeVUp_fine_binning'   -k '12' --range 280 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_low_8TeVDown_fine_binning' -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_low_8TeVUp_fine_binning'   -k '13' --range 140 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_high_8TeVDown_fine_binning' -k '14' --range 200 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'QCD_CMS_htt_QCDShape_mutau_btag_high_8TeVUp_fine_binning'   -k '14' --range 200 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))                    
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_low_8TeVDown_fine_binning' -k '10' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_low_8TeVUp_fine_binning'   -k '10' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_medium_8TeVDown_fine_binning' -k '11' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_medium_8TeVUp_fine_binning'   -k '11' --range 240 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_high_8TeVDown_fine_binning' -k '12' --range 325 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_nobtag_high_8TeVUp_fine_binning'   -k '12' --range 325 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_btag_low_8TeVDown_fine_binning' -k '13' --range 200 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_btag_low_8TeVUp_fine_binning'   -k '13' --range 200 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_btag_high_8TeVDown_fine_binning' -k '14' --range 250 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_mt.inputs-mssm-8TeV-0.root -c mt -e 8TeV -b 'W_CMS_htt_WShape_mutau_btag_high_8TeVUp_fine_binning'   -k '14' --range 250 --fitoption 1 --fitmodel 1 --erroroption 1 --no-uncerts".format(
                        DIR=dir, ANA=ana))
                if 'tt' in config.channels :
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '13' --range 300 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '14' --range 250 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '10' --range 300 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))                        
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '11' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_fine_binning' -k '12' --range 250 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    ## tail fit for QCD shape uncertainties
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVUp_fine_binning' -k '13' --range 300 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVDown_fine_binning' -k '13' --range 300 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVUp_fine_binning' -k '13' --range 300 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVDown_fine_binning' -k '13' --range 300 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVUp_fine_binning' -k '14' --range 250 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVDown_fine_binning' -k '14' --range 250 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVUp_fine_binning' -k '14' --range 250 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVDown_fine_binning' -k '14' --range 250 --rangelast 800 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVUp_fine_binning' -k '10' --range 300 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVDown_fine_binning' -k '10' --range 300 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVUp_fine_binning' -k '10' --range 300 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVDown_fine_binning' -k '10' --range 300 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVUp_fine_binning' -k '11' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVDown_fine_binning' -k '11' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVUp_fine_binning' -k '11' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVDown_fine_binning' -k '11' --range 250 --rangelast 1000 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVUp_fine_binning' -k '12' --range 250 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrNorm_tautau_8TeVDown_fine_binning' -k '12' --range 250 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVUp_fine_binning' -k '12' --range 250 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                    runCommand("addFitNuisance.py -s {DIR}/{ANA} -i htt_tt.inputs-mssm-8TeV-0.root -c tt -e 8TeV -b 'QCD_CMS_htt_QCDfrShape_tautau_8TeVDown_fine_binning' -k '12' --range 250 --rangelast 700 --fitoption 1 --fitmodel 1 --erroroption 1".format(
                        DIR=dir, ANA=ana))
                ## cleanup
                runCommand("rm rootlogon.C")
                runCommand("mkdir -p tail-fitting")
                runCommand("mv *_Rebin.* tail-fitting")
        if ana == 'plain' :
            print "##"
            print "## update no-bbb directory in setup:"
            print "##"
        if 'tail' in ana :
            print "##"
            print "## update tail   directory in setup:"
            print "##"
            for chn in config.channels :
                print "{DIR}/{TARGET}/{CHN}/unc-mssm-*.vals".format(DIR=dir, TARGET=ana, CHN=chn)
                for file in glob.glob("{DIR}/{TARGET}/{CHN}/unc-mssm-*.vals".format(DIR=dir, TARGET=ana, CHN=chn)) :
                    print "perl -pi -e 's/\#\[tail\]//g'   {FILE}".format(FILE=file)
                    runCommand("perl -pi -e 's/\#\[tail\]//g'   {FILE}".format(FILE=file))
        if 'bbb' in ana :
            print "##"
            print "## update bbb    directory in setup:"
            print "##"
            for chn in config.channels:
                for per in config.periods:
                    for idx in range(len(config.bbbcat[chn][per])):
                        if options.new_merging :
                            filename='htt_'+chn+'.inputs-mssm-'+per+'-0.root'
                            for cat in config.bbbcat[chn][per][idx].split(',') :
                                ## loop all categories in question for index idx
                                if len(config.bbbproc[chn][idx].replace('>',',').split(','))>1 :
                                    ## only get into action if there is more than one sample to do the merging for
                                    runCommand("merge_bin_errors.py --folder {DIR} --processes {PROC} --bbb_threshold={BBBTHR} --merge_threshold={THRESH} --verbose {SOURCE} {TARGET}".format(
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
                        runCommand("add_bbb_errors.py '{CHN}:{PER}:{CAT}:{PROC}' {NORMALIZE} -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold {THR} --mssm".format(
                            DIR=dir,
                            ANA=ana,
                            CHN=chn,
                            PER=per,
                            NORMALIZE=normalize_bbb,
                            CAT=config.bbbcat[chn][per][idx],
                            PROC=config.bbbproc[chn][idx].replace('>',',') if options.new_merging else config.bbbproc[chn][idx],
                            THR=config.bbbthreshold[chn]
                            ))                   
                        runCommand("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
                        runCommand("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        if options.SMHasBackground :
            analysesv2 = []
            for ana in analyses :
                runCommand("cp -r {DIR}/{TARGET} {DIR}/{TARGET}-SMHbkg".format(DIR=dir, TARGET=ana))
                cgs_adaptor = UncertAdaptor()
                for chn in ['em', 'et', 'mm', 'mt', 'tt']:
                    if chn in config.channels:
                        for period in config.periods:
                            for idx in range(len(config.bbbcat[chn][period])) :
                                for category in config.bbbcat[chn][period][idx].split(',') :
                                    filename="{DIR}/{TARGET}-SMHbkg/{CHN}/cgs-mssm-{PERIOD}-{CATEGORY}.conf".format(DIR=dir, TARGET=ana, CHN=chn, PERIOD=period, CATEGORY=category)
                                    print 'processing file:', filename
                                    cgs_adaptor.cgs_processes(filename,None,['ggH_SM125','qqH_SM125','VH_SM125'],None,None)
                analysesv2.append(ana)                
                analysesv2.append(ana+'-SMHbkg')
            analyses=analysesv2
                                
if options.update_aux :
    print "##"
    print "## update aux directory:"
    print "##"
    dir = "{CMSSW_BASE}/src/aux{LABEL}".format(CMSSW_BASE=cmssw_base, LABEL=options.label)
    if os.path.exists(dir) :
        if os.path.exists(dir.replace('src/', 'src/backup/')):
            runCommand("rm -r "+dir.replace('src/', 'src/backup/'))
        runCommand("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    runCommand("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        for chn in config.channels:
            for per in config.periods: 
                if config.categories[chn][per]:
                    runCommand("setup-datacards.py -i {CMSSW_BASE}/src/setups{LABEL}/{ANA} -o {DIR}/{ANA} -p '{PER}' -a mssm -c '{CHN}' --mssm-categories-{CHN}='{CATS}' {MASSES}".format(
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
                for subdir in glob.glob("{DIR}/{ANA}/mssm/*".format(DIR=dir, ANA=ana)) :
                    print '...comment bbb uncertainties for', subdir
                    runCommand("python HiggsAnalysis/CombinedLimit/scripts/commentUncerts.py --drop-list={DROP} {SUB}".format(DROP=options.drop_list, SUB=subdir))
        if options.SMHasBackground and options.SMHasSignal:
            analysesv2 = []
            if '-SMHbkg' in ana :
                anav2= ana.replace('-SMHbkg','')
                runCommand("cp -r {DIR}/{ANA} {DIR}/{ANAv2}-MSSMvsSM".format(DIR=dir,ANA=ana,ANAv2=anav2))
                datacard_adaptor = DatacardAdaptor()
                for subdir in glob.glob("{DIR}/{ANAv2}-MSSMvsSM/mssm/*".format(DIR=dir, ANAv2=anav2)) :
                    for datacard in glob.glob("{SUBDIR}/*".format(SUBDIR=subdir)) :
                        if '.txt' in datacard :
                            datacard_adaptor.simplistic_shift_bg_to_signal(datacard,["ggH_SM125","qqH_SM125","VH_SM125"])
                analysesv2.append(ana)  
                analysesv2.append(anav2+'-MSSMvsSM')
                analysesv2.append(anav2)
            analyses=analysesv2
    print "analyses", analyses  
    ## blind datacards
    if options.blind_datacards :
        for ana in analyses : 
            runCommand("cp -r {DIR}/{ANA} {DIR}/{ANA}-asimov".format(DIR=dir,ANA=ana))
            for chn in config.channels :
                runCommand("blindData.py --update-file --extra-templates '{EXTRA_TEMPLATES}' {DIR}/{ANA}-asimov/mssm/{CHN}".format(
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
            runCommand("rm -r "+dir.replace('src/', 'src/backup/'))
        runCommand("mv {DIR} {CMSSW_BASE}/src/backup/".format(DIR=dir, CMSSW_BASE=cmssw_base))
    runCommand("mkdir -p {DIR}".format(DIR=dir))    
    for ana in analyses :
        print "setup limits structure for:", ana
        for chn in config.channels:
            for per in config.periods:
                if config.categories[chn][per]:
                    runCommand("setup-htt.py -i aux{INDEX}/{ANA}{ASIMOV} -o {DIR}/{ANA}{ASIMOV} -p '{PER}' -a mssm -c '{CHN}' --mssm-categories-{CHN}='{CATS}' {MASSES}".format(
                        INDEX=options.label,                
                        ANA=ana,
                        ASIMOV='-asimov' if options.blind_datacards else '',
                        DIR=dir,
                        PER=per,
                        CHN=chn,
                        CATS=' '.join(config.categories[chn][per]),
                        MASSES=' '.join(masses),
                        ))
        ## add inputs files with 1D msvfit histograms in LIMIT directory structure
        if 'mm' in config.channels :
            for subdir in glob.glob("{DIR}/{ANA}/*".format(DIR=dir, ANA=ana)) :
                runCommand("cp -v {SETUP}/mm/*-msv.root {DIR}/common".format(SETUP=setup, DIR=subdir))
