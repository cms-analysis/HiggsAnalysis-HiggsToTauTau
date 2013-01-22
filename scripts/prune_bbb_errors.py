#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to prune the bin-by-bin uncertainties of an existing set of datacards with bin-by-bin-uncertainties. The script will have the output of the script setup-datacards.py (and add_bbb_errors.py) as input and prune the bin-by-bin uncertainties in all available datacards for all indicated channels in this directory. Prunded bin-by-bin uncertainties will be commented in the corresponding datacard. The script will only prune bin-by-bin uncertainties. ARG corresponds to the input directory.")
agroup = OptionGroup(parser, "MAIN OPTIONS", "These are the main command line options for the use of prune_bbb_errors.py. Choose between the main methods of use --byLimit and --byPull.")
agroup.add_option("--byLimit", dest="optByLimit", default=False, action="store_true",
                  help="With this method the parameters to be pruned will be determined by the influence of the parameter on the limit calculation. For performance reasons the procedure is split by decay channels. [Default: \"False\"]")
agroup.add_option("--byPull", dest="optByPull", default=False, action="store_true",
                  help="With this method the parameters to be pruned will be determined by the influence the fit has on the parameter in the background only or in the signal+background fit. When applying this method a maximum likelihood fit will be performed on the combination of all indicated decay channel. Depending on the number of nuisance parameters in the model this can take up to several hours. [Default: \"False\"]")
parser.add_option_group(agroup)
bgroup = OptionGroup(parser, "COMMON OPTIONS", "These are the command line options that a common for both methods. You can determine the mass to be chosen for the pruning process, the number of channels to be considered and the threshold to distinguish the pruning. Note that depending on the method the threshold does have a different meaning and should take different values.")
bgroup.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="The list of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et tt\"]")
bgroup.add_option("-m", "--mass", dest="mass", default="125", type="string",
                  help="The mass value to be used to run the pruning algorithm on. [Default: 125]")
parser.add_option_group(bgroup)
cgroup = OptionGroup(parser, "BYLIMIT OPTIONS", "These are the additional command line options when running the script with option --byLimit.")
cgroup.add_option("--limit-threshold", dest="limit_threshold", default="0.0025", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the relative difference on the limit result (split by channel) when taking the nuisance parameter of choice into account or not. [Default: 0.0025]")
cgroup.add_option("--limit-metric", dest="limit_metric", default="all",  type="choice", choices=['exp', 'obs', 'all'],
                  help="The metric to be used for pruning. Choices are: exp (maximal difference on expected limit only), obs (maximal difference on observed only), all (maximal difference on of observed or expected). [Default: 'all']")
parser.add_option_group(cgroup)
dgroup = OptionGroup(parser, "BYPULL OPTIONS", "These are the additional command line options when running the script with option --byPull.")
dgroup.add_option("--pull-threshold", dest="pull_threshold", default="0.05", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the pull of the parameter in the maximum likelihood fit. [Default: 0.05]")
dgroup.add_option("--pull-metric", dest="pull_metric", default="all",  type="choice", choices=['b-only', 's+b', 'all'],
                  help="The metric to be used for pruning. Choices are: b-only (pull for b-only fit), s+b (pull for s+b fit), all (maximum of pull on b-only and s+b fit). [Default: 'all']")
dgroup.add_option("--fit-result", dest="fit_result", default="",  type="string",
                  help="The full path to the result file of the fit (mlfit.txt) if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
parser.add_option_group(dgroup)
parser.add_option("--debug", dest="debug", default=False, action="store_true",
                  help="Run in debug mode. Only recommended for (performace) testing or debugging. [Default: False]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
import glob
import json
import math
import ROOT

## channels
channels = options.channels.split()
for idx in range(len(channels)) : channels[idx] = channels[idx].rstrip(',')
## parent directory from which the tool has been executed
parentdir = os.getcwd()

## setup directory structure for for logging
os.system("mkdir -p log")
os.system("mkdir -p log/pruning")
logdir = os.getcwd()+'/log/pruning'

def summarize_uncerts(values, chn=None) :
    path = logdir
    output = path+"/bin-by-bin-uncertainties-%s.root" % chn if chn else path+"/bin-by-bin-uncertainties.root"
    print "writing pulls/effect on limit to", output
    file = ROOT.TFile(output, "UPDATE")
    nbin = 150 if options.optByPull else 150
    xmin = 0.  if options.optByPull else -3.
    xmax = 1.5 if options.optByPull else  0.
    hist = ROOT.TH1F("bin-by-bin", "bin-by-bin", nbin, xmin, xmax)
    for val in values :
        hist.Fill(val if options.optByPull else math.log10(val))
    file.Write("bin-by-bin")
    file.Close()

## number of excluded files
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

print "setting up directory structure for bbb uncertainty pruning"
for chn in channels :
    ## uncomment all cards in case that pruning has been run beforehand on these cards already. 
    for datacard in glob.glob('{PARENT}/{INPUT}/htt_{CHN}/*.txt'.format(PARENT=parentdir,INPUT=args[0], CHN=chn)) :
        manipulate_bbb(datacard, "UNCOMMENT")
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
    os.system("cvs2local.py -i {INPUT} -o pruning -p {PER} -a {ANA} -c {CHN} {MASS}".format(
        INPUT=args[0][:args[0].rstrip('/').rfind('/')],
        PER=period,
        ANA=analysis,
        CHN=chn,
        MASS=options.mass
        ))

## in case of option --byPull and empty fit-results
## run the max-likelihood fit before changing into
## the pruning directory
if options.optByPull and options.fit_result == "" :
    os.system("limit.py --max-likelihood --stable pruning/{MASS}".format(MASS=options.mass))
    os.system("cp pruning/{MASS}/out/mlfit.txt {LOG}".format(MASS=options.mass, LOG=logdir))
        
## change directory (needed by sizeUpsystematics.py)
os.chdir("pruning/{MASS}".format(MASS=options.mass))

glob_all =0
glob_excl = 0
if options.optByLimit :
    ## metrics for pruning
    metric_exp    = lambda map : max(abs(map['exp']['AllIn']), abs(map['exp']['AllOut']));
    metric_obs    = lambda map : max(abs(map['obs']['AllIn']), abs(map['obs']['AllOut']));
    metric_all    = lambda map : max(metric_exp(map), metric_obs(map))
    metrics = { 'exp':metric_exp, 'obs':metric_obs, 'all':metric_all };
    metric = metrics[options.limit_metric]
    
    ## pick up parameters from json file per channel
    def prune_by_limit(path, chn) :
        out = 0
        all = 0
        vals= []
        report = json.loads(" ".join([l for l in open(path,"r")]))
        if not report: raise RuntimError, "Couldn't load %s" % path
        toExclude = []
        for (nuisList, map) in report:
            all += 1
            outcome = metric(map)
            if options.debug :
                bbb = re.match("\w+bin\_*\d*\w+", nuisList[0])
                if bbb :
                    vals.append(float(outcome))
            if float(outcome) < float(options.limit_threshold) :
                toExclude += nuisList
                out += 1
        print "excluded", out, "from", all
        if options.debug :
            summarize_uncerts(vals, chn)
        return toExclude
        
    ## to get started comment all bin-by-bin uncertainties
    for datacard in glob.glob('*.txt') :
        manipulate_bbb(datacard, "COMMENT")    
    ## run the parameter ranking channelwise. 
    for chn in channels :
        all = 0
        for datacard in glob.glob('*_{CHN}_*.txt'.format(CHN=chn)) :
            all += manipulate_bbb(datacard, "UNCOMMENT")
        if all == 0 :
            print "no bin-by-bin uncertainties found for channel:", chn
            continue
        else :
            print "ranking all nuisance parameters for channel:", chn
            if not os.path.exists('test-{CHN}'.format(CHN=chn)) :
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
            else:
                print 'ranking directory exists already. Will not re-run, but use existing results.'
            ## prune datacards for given channel
            excl = 0
            excludes = prune_by_limit("test-{CHN}/Removed1.json".format(CHN=chn), chn)
            for datacard in glob.glob('*_{CHN}_*.txt'.format(CHN=chn)) :
                excl += manipulate_bbb(datacard, "COMMENT", excludes)
            if all>0 :
                print "commented", excl, "bin-by-bin uncertainties from", all, "for channel:", chn, "(", float(100*excl/all), "%)"
            ## and finally prune all datacards for all masses in input directory
            for datacard in glob.glob('{PARENT}/{INPUT}/htt_{CHN}/*_{CHN}_*.txt'.format(PARENT=parentdir,INPUT=args[0], CHN=chn)) :
                ## uncomment bin-by-bin uncertainties that might have been processed alreadt in previous iterations
                manipulate_bbb(datacard, "UNCOMMENT")
                ## comment bin-by-bin uncertainties
                manipulate_bbb(datacard, "COMMENT", excludes)
            glob_all += all
            glob_excl += excl
    if options.debug :
        os.system("hadd bin-by-bin-uncertainties.root bin-by-bin-uncertainties-*.root")
        
if options.optByPull :
    ## copy the results of the max-likelihood fit to local
    if not options.fit_result == "" :
        os.system("mkdir -p out")
        os.system("cp {SRC} out/mlfit.txt".format(SRC=options.fit_result))
    ## pick up parameters from json file per channel
    def prune_by_pull(path) :
        out = 0
        all = 0
        vals= []
        file = open(path,'r')
        toExclude = []
        for line in file :
            bbb = re.match("^#*\s*(\w+bin\_*\d*\w+)", line.split()[0])
            if bbb :
                pull_match = re.compile('[+-]\d+\.\d+(?=sig)')
                pulls = pull_match.findall(line)
                if pulls :
                    all += 1
                    if options.pull_metric == 'b' :
                        if options.debug :
                            vals.append(float(pulls[0]))
                        if abs(float(pulls[0])) < float(options.pull_threshold) :
                            out += 1
                            toExclude.append(line.split()[0])
                    if options.pull_metric == 's+b' :
                        if options.debug :
                            vals.append(float(pulls[1]))                        
                        if abs(float(pulls[1])) < float(options.pull_threshold) :
                            out += 1
                            toExclude.append(line.split()[0])
                    if options.pull_metric == 'all' :
                        if options.debug :
                            vals.append(float(max(abs(float(pulls[0])), float(pulls[1]))))
                        if max(abs(float(pulls[0])), float(pulls[1])) < float(options.pull_threshold) :
                            out += 1
                            toExclude.append(line.split()[0])
        file.close()
        print "excluded", out, "from", all
        if options.debug :
            summarize_uncerts(vals)
        return toExclude
    ## prune datacards for given channel
    excludes = prune_by_pull("out/mlfit.txt")
    for chn in channels :
        all  = 0
        excl = 0
        for datacard in glob.glob('*_{CHN}_*.txt'.format(CHN=chn)) :
            all  += manipulate_bbb(datacard, "UNCOMMENT")
            excl += manipulate_bbb(datacard, "COMMENT", excludes)
        if all>0 :
            print "commented", excl, "bin-by-bin uncertainties from", all, "for channel:", chn, "(", float(100*excl/all), "%)"
        ## and finally prune all datacards for all masses in input directory
        for datacard in glob.glob('{PARENT}/{INPUT}/htt_{CHN}/*.txt'.format(PARENT=parentdir,INPUT=args[0], CHN=chn)) :
            ## uncomment bin-by-bin uncertainties that might have been processed alreadt in previous iterations
            #manipulate_bbb(datacard, "UNCOMMENT")
            ## comment bin-by-bin uncertainties
            manipulate_bbb(datacard, "COMMENT", excludes)
        glob_all += all
        glob_excl += excl

## a short summary
if glob_all>0 :
    print "Summary:"
    print "commented", glob_excl, "bin-by-bin uncertainties from", glob_all, "for all channels. (", float(100*glob_excl/glob_all), "%)"
## clean up if not requested otherwise
os.chdir(parentdir)
os.system("rm -r pruning")
