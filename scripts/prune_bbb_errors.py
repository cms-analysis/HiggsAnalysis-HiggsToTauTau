#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to prune the bin-by-bin uncertainties of an existing set of datacards with bin-by-bin-uncertainties. The script will have the output of the script setup-datacards.py (and add_bbb_errors.py) as input and prune the bin-by-bin uncertainties in all available datacards for all indicated channels in this directory. Prunded bin-by-bin uncertainties will be commented in the corresponding datacard. The script will only prune bin-by-bin uncertainties. ARG corresponds to the input directory.")
parser.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="List of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. Note that the order in which the arguments are given will determine the order in which the pruning og bin-by-bin uncertainties will be processed. The recommendation is to start with the channels, which are the least sensitive to the bin-by-bin uncertainties and then to proceed to the channels, which are the most sensitive to bin--by-bin uncertainties. [Default: \"mm em mt et tt\"]")
parser.add_option("-m", "--mass", dest="mass", default="125", type="string",
                  help="Mass value to be used for the pruning algorithm. [Default: 125]")
parser.add_option("--threshold", dest="threshold", default="0.0025", type="string",
                  help="Threshold to prune the given bin-by-bin uncertainty. The value is given for the relative pull on the uncertainty parameter in the fit. [Default: 0.005]")
parser.add_option("--metric", dest="metric", default="all",  type="choice", choices=['exp', 'obs', 'all'],
                  help="Metric to be used fro pruning. Choices are: exp (maximal difference on expected limit only), obs (maximal difference on observed only), all (maximal difference on of observed or expected).")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode. [Default: False]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
import glob
import json

## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## metrics for pruning
metric_exp = lambda map : max(abs(map['exp']['AllIn']), abs(map['exp']['AllOut']));
metric_obs = lambda map : max(abs(map['obs']['AllIn']), abs(map['obs']['AllOut']));
metric_all = lambda map : max(metric_exp(map), metric_obs(map))
metrics = { 'exp':metric_exp, 'obs':metric_obs, 'all':metric_all };
metric = metrics[options.metric]

## number of ecxluded files
def manipulate_bbb(datacard, manipulation, excludes=None) :
    excl=0
    file = open(datacard,'r')
    output = open('tmp.txt', 'w')
    for line in file :
        bbb = re.match("^#*\s*(\w+bin\_*\d*\w+)\s+(shape)\s+.*", line)
        if bbb :
            if manipulation == "COMMENT" :
                if excludes != None:
                    if bbb.group(1) in excludes :
                        excl+=1
                        line = '#'+line                    
                else :
                    excl+=1
                    line = '#'+line
            if manipulation == "UNCOMMENT" :
                excl+=1
                line = line.lstrip('#')
        output.write(line)
    ##close files
    file.close()
    output.close()
    os.system("mv tmp.txt %s" % datacard)
    return excl

## pick up parameters from json file per channel
def prune(path) :
    out = 0
    all = 0
    report = json.loads(" ".join([l for l in open(path,"r")]))
    if not report: raise RuntimError, "Couldn't load %s" % path

    toExclude = []
    for (nuisList, map) in report:
        all += 1
        outcome = metric(map)
        if float(outcome) < float(options.threshold) :
            toExclude += nuisList
            out += 1
    print "excluded", out, "from", all
    return toExclude

print "setting up directory structure for bbb uncertainty pruning"
for chn in channels :
    ## pick up the list of available datacards per channel
    datacards = ' '.join(glob.glob(args[0]+'/'+'htt_'+chn+'/*.txt'))
    ## prepare cvs2local.py
    period = "\'"
    if '7TeV' in datacards :
        period+='7TeV '
    if '8TeV' in datacards :
        period+='8TeV '
    period = period.rstrip()+"\'"
    analysis = args[0].rstrip('/')
    analysis = analysis[analysis.rfind('/')+1:]
    os.system("cvs2local.py -i {INPUT} -o tmp -p {PER} -a {ANA} -c {CHN} {MASS}".format(
        INPUT=args[0][:args[0].rstrip('/').rfind('/')],
        PER=period,
        ANA=analysis,
        CHN=chn,
        MASS=options.mass
        ))

## change directory (needed by sizeUpsystematics.py)
parentdir = os.getcwd()
os.chdir("tmp/{MASS}".format(MASS=options.mass))

## to get started comment all bin-by-bin uncertainties
for datacard in glob.glob('*.txt') :
    manipulate_bbb(datacard, "COMMENT")

## run the parameter ranking channelwise. 
for chn in ['tt'] : #channels :
    all = 0
    for datacard in glob.glob('*_{CHN}_*.txt'.format(CHN=chn)) :
        all += manipulate_bbb(datacard, "UNCOMMENT")
    if all == 0 :
        print "no bin-by-bin uncertainties found for channel:", chn
        continue
    else :
        print "ranking all nuisance parameters for channel:", chn
        os.system("combineCards.py -S {CARDS} > test-{CHN}.txt". format(
            ## to run on all cards combined while for each non-covered channel all bbb 
            ## uncertainties are commented and for each pre-ceding channel the bbb
            ## uncertainties are already pruned uncomment the follwing line.
            #CARDS=' '.join(glob.glob('*.txt')),
            ## to run on all cards combined but seperated by channels uncomment the
            ## the following line
            CARDS=' '.join(glob.glob('*_{CHN}_*.txt'.format(CHN=chn))),
            CHN=chn
            ))
        ## run nuisance parameter ranking
        cmd = "python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/sizeUpSystematics.py"
        os.system("{CMD} {PWD}/test-{CHN}.txt --masses={MASS} --X-keep-global-nuisances --dir test-{CHN}".format(
            CMD=cmd,
            PWD=os.getcwd(),
            MASS=options.mass,
            CHN=chn
            ))
        ## clean up test datacard
        os.system("mv test-{CHN}.txt test-{CHN}".format(
        MASS=options.mass,
        CHN=chn
        ))
        ## prune datacards for given channel
        excl = 0
        excludes = prune("test-{CHN}/Removed1.json".format(CHN=chn))
        for datacard in glob.glob('*_{CHN}_*.txt'.format(CHN=chn)) :
            excl += manipulate_bbb(datacard, "COMMENT", excludes)
        print "commented", excl, "bin-by-bin uncertainties from", all, "for chn:", chn
        ## and finally prune all datacards for all masses in input directory
        for datacard in glob.glob('{PARENT}/{INPUT}/htt_{CHN}/*_{CHN}_*.txt'.format(PARENT=parentdir,INPUT=args[0], CHN=chn)) :
            manipulate_bbb(datacard, "COMMENT", excludes)
## clean up if not requested otherwise
if not options.verbose :
    os.chdir(parentdir)
    os.system("rm -r tmp")
