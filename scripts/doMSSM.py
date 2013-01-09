#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to setup all datacards and directories and to perform limit calculations at the end hopefully only plotting has to be done. ARGS should correspond to the masses, for which to setup the structure. The script assumes that all datacards (but unscaled) are located in $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/setup/[em,et,mt,mm,tt,hbb].")
##
## GENERAL OPTIONS
##
parser.add_option("-u", "--user", dest="user", default="USER", type="string", help="UserName needed for batch checkbacks. [Default: USER]")
parser.add_option("-n", "--name", dest="name", default="testing", type="string", help="Name of copied setup-dir in $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/<name> and of new setup-dir after scaling. [Default: testing]")
##
## SKIP OPTIONS
##
parser.add_option("-s", "--skip-setup", dest="skip_setup", default=False, action="store_true", help="skip setup. [Default: False]")
parser.add_option("-d", "--skip-datacards", dest="skip_datacards", default=False, action="store_true", help="skip datacards. [Default: False]")
parser.add_option("-l", "--skip-limits", dest="skip_limits", default=False, action="store_true", help="skip limit setup. [Default: False]")
##
## BATCH OPTIONS
##
cgroup = OptionGroup(parser, "BATCH OPTIONS", "These are the command line options that can be used to configure lxb (lxq) batch job submission via the script lxb_submit.py. Batch job submission of this type is applicable for the following options: --likelihood-scan, --asymptotic, --tanb+. When using batch job submission in one of these main options it is possible to go up by one level in the directory structure when specifying ARGs as described in the head of this parameter description. Note: when running in batch mode batch jobs are split by each mass directory that can be found in the directory structure.")
cgroup.add_option("-q", "--queue", dest="queue", default="-q 8nh", type="string",
                  help="The queue, to which to submit the jobs. [Default: \"-q 8nh\"]")
cgroup.add_option("--lxq", dest="lxq", default=False, action="store_true",
                  help="Specify this option when running on lxq instead of lxb for simple batch job submissions. [Default: False]")
cgroup.add_option("--condor", dest="condor", default=False, action="store_true",
                  help="Specify this option when running on condor instead of lxb for simple batch job submissions. [Default: False]")
parser.add_option_group(cgroup)

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import time

masses = args[0]
cmssw_base=os.environ['CMSSW_BASE']
base_dir = os.getcwd()

##
## START 
##

## creating backup
print "INFO: create a backup"
os.system("cp -r {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/setup {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/{NAME}".format(
    NAME=options.name, CMSSW_BASE=os.environ['CMSSW_BASE']
    ))

## scaling of root files and adding bin-by-bin uncertainties
setup=cmssw_base+"/src/HiggsAnalysis/HiggsToTauTau/{NAME}".format(NAME=options.name)
if not options.skip_setup:    
    ##acceptance correction
    print "INFO: Acceptance correction scaling"
    os.system("scale2accept.py -i {SETUP} -c 'em, et, mt, mm' 90 100-200:20 130 250-500:50 600-1000:100".format(
        SETUP=setup
        ))
    #os.system("scale2accept.py -i {SETUP} -c tt -p 8TeV 90 100-200:20 130 250-500:50".format(
        #SETUP=setup
        #))
    #os.system("scale2accept.py -i {SETUP} -c hbb -p 7TeV 90 100-200:20 130 250-350:50".format(
        #SETUP=setup
        #))
    ##bin-by-bin uncertainties
    print "INFO: Adding bin-by-bin uncertainties"    
    dir=cmssw_base+"/src/setups"
    os.system("add_bbb_errors.py 'et,mt,em:7TeV,8TeV:08,09:ZL,ZLL,Fakes,QCD>W' --mssm --in='{SETUP}' --out='{DIR}/{NAME}' --threshold 0.10".format(
        DIR=dir,
        SETUP=setup,
        NAME=options.name
        ))
       
if not options.skip_datacards :
    ##creation of datacards
    print "INFO: Creation od datacards"
    os.system("setup-datacards.py -i {DIR}/{NAME} -o {NAME} -a mssm -c 'em et mt mm hbb' {MASSES}".format(
        DIR=dir,
        SETUP=setup,
        MASSES=masses,
        NAME=options.name        
        ))
    ##setting up directory structure
    print "INFO: Setting up the directory structure"
    os.system("setup-htt.py -i {NAME} -o {NAME}_out -a mssm -c 'em et mt mm hbb' {MASSES}".format(
        MASSES=masses,
        NAME=options.name
        ))
    os.system("cp -r {NAME}_out {NAME}_out2".format(
        NAME=options.name
        ))

if not options.skip_limits :
    ##postfit plots
    print "INFO: Calculating pulls and postfit plots"
    os.chdir("{CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/test".format(
        CMSSW_BASE=os.environ['CMSSW_BASE']
        ))
    os.system("./mlfit_and_copy.py -a mssm {CMSSW_BASE}/src/{NAME}_out/cmb/100".format(
        CMSSW_BASE=os.environ['CMSSW_BASE'],
        NAME=options.name
        ))
    os.system("python produce_macros.py -a mssm")
    os.system("python run_macros.py -a mssm")
    ##standard tanb-mA limit
    print "INFO: Calculating limits in tanb-mA plane"
    os.chdir("{BASE_DIR}".format(
        BASE_DIR= base_dir
        ))
    os.system("xsec2tanb.py --tanb+ {LXQ} {NAME}_out/cmb/*".format(
        NAME=options.name,
        LXQ="--lxq" if options.lxq else ""
        ))
    #wait for jobs to finish
    output=""
    if options.lxq :
        p = os.popen("qstat -u {USER}".format(
        USER=options.user
        ))
        output = p.readline()
        p.close() 
    else  :
        p = os.popen('bjobs')
        output = p.readline()
        p.close() 
    while output!="" :    
        time.sleep(60)
    os.system("submit.py --tanb+ --options='multi-core=4' {LXQ} {QUEUE} {CONDOR} {NAME}_out/cmb/*".format(
        NAME=options.name,
        LXQ="--lxq" if options.lxq else "",
        QUEUE="--queue='-l h_cpu=12:00:00 -j y -o /dev/null'" if options.queue!="" else "",
        CONDOR="--condor" if options.condor else ""
        ))
    ##2D scans ggH-bbH
    print "INFO: Calculating multidim scans"
    os.system("submit.py {LXQ} {QUEUE} {CONDOR} --multidim-fit --physics-model='ggH-bbH' {NAME}_out/cmb/*".format(
        NAME=options.name,
        LXQ="--lxq" if options.lxq else "",
        QUEUE="--queue='-l h_cpu=1:00:00 -j y -o /dev/null'" if options.queue!="" else "",
        CONDOR="--condor" if options.condor else ""
        ))
    #wait for jobs to finish
    output=""
    if options.lxq :
        p = os.popen("qstat -u {USER}".format(
        USER=options.user
        ))
        output = p.readline()
        p.close() 
    else  :
        p = os.popen('bjobs')
        output = p.readline()
        p.close() 
    while output!="" :    
        time.sleep(60)
    os.system("limit.py --collect --multidim-fit --physics-model='ggH-bbH' {NAME}_out/cmb/*".format(
        NAME=options.name
        ))
