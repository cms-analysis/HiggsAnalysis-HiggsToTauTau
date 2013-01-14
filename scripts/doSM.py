#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to reload the MORIOND analysis with main analysis [Moriond-bin-by-bin] and two cross-check analyses [Moriond, Moriond-mvis]. ARGS should correspond to the masses, for which to setup the structure.")
parser.add_option("-c", "--skip-cvs-update", dest="skip_cvs", default=False, action="store_true", help="skip the cvs update and rescaling of the input files. [Default: False]")
parser.add_option("-s", "--skip-setup", dest="skip_setup", default=False, action="store_true", help="skip setup. [Default: False]")
parser.add_option("-d", "--skip-datacards", dest="skip_datacards", default=False, action="store_true", help="skip datacards. [Default: False]")
parser.add_option("-l", "--skip-limits", dest="skip_limits", default=False, action="store_true", help="skip limit setup. [Default: False]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
masses = args[0]
cmssw_base=os.environ['CMSSW_BASE']
## copy files in setup
aux = {
    'em' : ['MIT'],
    'et' : ['Wisconsin', 'Imperial'],
    'mt' : ['Wisconsin', 'Imperial'],
    'mm' : ['Htt_MuMu_Unblinded'],
    'tt' : ['Htt_FullHad']
    }

setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/setup"
    
if not options.skip_cvs :
    for chn, dirs in aux.iteritems() :
        for dir in dirs :
            print "copy files for channel:", chn
            os.system("cp {CMSSW_BASE}/src/auxiliaries/datacards/collected/{DIR}/htt_{CHN}*.root {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup/{CHN}/".format(
                CMSSW_BASE=cmssw_base,
                DIR=dir,
                CHN=chn
                ))
    os.system("mv {SETUP}/mm/htt_mm.inputs-mssm-7TeV_msv.root {SETUP}/mm/htt_mm.inputs-mssm-7TeV_postfit.root".format(SETUP=setup))
    os.system("mv {SETUP}/mm/htt_mm.inputs-mssm-8TeV_msv.root {SETUP}/mm/htt_mm.inputs-mssm-8TeV_postfit.root".format(SETUP=setup))
    os.system("mv {SETUP}/mm/htt_mm.inputs-sm-7TeV_msv.root {SETUP}/mm/htt_mm.inputs-sm-7TeV_postfit.root".format(SETUP=setup))
    os.system("mv {SETUP}/mm/htt_mm.inputs-sm-8TeV_msv.root {SETUP}/mm/htt_mm.inputs-sm-8TeV_postfit.root".format(SETUP=setup))
    ## scale to SM cross section
    for chn in aux :
        files = os.listdir("{SETUP}/{CHN}".format(SETUP=setup, CHN=chn))
        for file in files :
            if chn == 'tt' :
                ## do NOT scale tt, these are already scaled
                continue
            if chn in file and '-sm-' in file :
                os.system("scale2SM.py -i {SETUP}/{CHN}/{FILE} -s 'ggH, qqH, VH' {MASSES}".format(
                    SETUP=setup,
                    CHN=chn,
                    FILE=file,
                    MASSES=masses
                    ))
                
if not options.skip_setup :
    source = "{CMSSW_BASE}/src/setups".format(CMSSW_BASE=cmssw_base)
    if os.path.exists(source) :
        os.system("rm -r {DIR}".format(DIR=source))
    os.system("mkdir {DIR}".format(DIR=source))
    ## setup main analysis
    os.system("cp -r {SETUP} {DIR}/Moriond".format(SETUP=setup, DIR=source))
    ## setup bin-by-bin ##No included atm
    #os.system("add_bbb_errors.py 'et,mt,em:7TeV,8TeV:01,03,05:ZL,ZLL,Fakes,QCD>W' --input-dir {DIR}/Moriond --output-dir {DIR}/Moriond-bin-by-bin --threshold 0.10".format(
    #    DIR=source
    #    ))
    ## setup mvis ##skip for now
##     if os.path.exists("{DIR}/Moriond-mvis".format(DIR=source)) :
##         os.system("rm -r {DIR}/Moriond-mvis".format(DIR=source))
##     os.system("cp -r {DIR}/Moriond {DIR}/Moriond-mvis".format(DIR=source))
##     for chn in aux :
##         for ana in ['sm'] :
##             for per in ['7TeV', '8TeV'] :
##                 if chn == 'mm' :
##                     pass
##                 else :
##                     if chn == 'tt' and per == '7TeV' :
##                         continue
                  ##   if chn == 'mt' : #NEEDED??
##                         os.system("cp auxiliaries/datacards/collected/Wisconsin/unc-sm-8TeV-02-mvis.vals {DIR}/Moriond-mvis/{CHN}/unc-sm-8TeV-02.vals".format(
##                             DIR=source,
##                             CHN=chn
##                             ))
##                         os.system("cp auxiliaries/datacards/collected/Wisconsin/unc-sm-8TeV-02-mvis.vals {DIR}/Moriond-mvis/{CHN}/unc-sm-8TeV-02.vals".format(
##                             DIR=source,
##                             CHN=chn
##                             ))
##                     os.system("mv {DIR}/Moriond-mvis/{CHN}/htt_{CHN}.inputs-{ANA}-{PER}-mvis.root {DIR}/Moriond-mvis/{CHN}/htt_{CHN}.inputs-{ANA}-{PER}.root".format(
##                         DIR=source,
##                         CHN=chn,
##                         ANA=ana,
##                         PER=per
##                         ))
if not options.skip_datacards :
    ## setup datacards
    datacards = "{CMSSW_BASE}/src/aux".format(CMSSW_BASE=cmssw_base)
    if not os.path.exists(datacards) :
        os.system("mkdir {DIR}".format(DIR=datacards))
    #if os.path.exists(datacards+'/sm') :
    #    os.system("rm -r {DIR}/sm".format(DIR=datacards))
    #os.system("mkdir {DIR}/sm".format(DIR=datacards))
    #if os.path.exists(datacards+'/mssm') :
    #    os.system("rm -r {DIR}/mssm".format(DIR=datacards))
    #os.system("mkdir {DIR}/mssm".format(DIR=datacards))
    for ana in ['Moriond']:#, 'Moriond-bin-by-bin', 'Moriond-mvis'] :
        print "setup datacards for:", ana, "sm"
        os.system("setup-datacards.py -i setups/{ANA} -o {OUTPUT}/sm/{ANA} -a sm -c 'em et mt mm tt' {MASSES}".format(
            ANA=ana,
            OUTPUT=datacards,
            MASSES=masses
            ))
if not options.skip_limits :
    ## setup limit calculation
    limits = "{CMSSW_BASE}/src/MORIOND-Limits".format(CMSSW_BASE=cmssw_base)
    if not os.path.exists(limits) :
        os.system("mkdir {DIR}".format(DIR=limits))
    for ana in ['Moriond']:#, 'Moriond-bin-by-bin', 'Moriond-mvis'] :
        label = ""
        if 'mvis' in ana :
            label = "-l "+ana[ana.find('-')+1:]
        if not options.skip_sm :
            print "setup limits structure for:", ana, "sm"
            os.system("setup-htt.py -i aux/sm/{ANA} -o {OUTPUT}/sm/{ANA} -a sm -c 'em et mt mm tt' {LABEL} {MASSES}".format(
                ANA=ana,
                LABEL=label,
                OUTPUT=limits,
                MASSES=masses
                ))
            if ana == 'Moriond' : #'Moriond-bin-by-bin' :  ##Later change that maybe
                for per in ['7TeV', '8TeV'] :
                    os.system("setup-htt.py -i aux/sm/{ANA} -o {OUTPUT}/sm/{ANA}-{PER} -p {PER} -a sm -c 'em et mt mm tt' {LABEL} {MASSES}".format(
                        ANA=ana,
                        PER=per,
                        LABEL=label,
                        OUTPUT=limits,
                        MASSES=masses
                        ))  
