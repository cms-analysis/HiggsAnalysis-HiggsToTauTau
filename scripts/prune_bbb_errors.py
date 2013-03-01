#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to prune the bin-by-bin uncertainties of an existing set of datacards with bin-by-bin-uncertainties. The script will have the output of the script setup-datacards.py (and add_bbb_errors.py) as input and prune the bin-by-bin uncertainties in all available datacards for all indicated channels in this directory. Prunded bin-by-bin uncertainties will be commented in the corresponding datacard. The script will only prune bin-by-bin uncertainties. ARG corresponds to the input directory.")
agroup = OptionGroup(parser, "MAIN OPTIONS", "These are the main command line options for the use of prune_bbb_errors.py. Choose between the main methods of use --byLimit and --byPull.")
agroup.add_option("--byLimit", dest="optByLimit", default=False, action="store_true",
                  help="With this method the parameters to be pruned will be determined by the influence of the parameter on the limit calculation. For performance reasons the procedure is split by decay channels. [Default: \"False\"]")
agroup.add_option("--byPull", dest="optByPull", default=False, action="store_true",
                  help="With this method the parameters to be pruned will be determined by the pull that the fit has on the parameter in the background only or in the signal+background fit. When applying this method a maximum likelihood fit will be performed on the combination of all indicated decay channel. Depending on the number of nuisance parameters in the model this can take up to several hours. [Default: \"False\"]")
agroup.add_option("--byShift", dest="optByShift", default=False, action="store_true",
                  help="This method is equivalent to method --byPull. Instrad of the pull the rleative shift of the parameter is taken into account, which is determined from the product of the pull with the original size of the uncertainty in the datacard. [Default: \"False\"]")
parser.add_option_group(agroup)
bgroup = OptionGroup(parser, "COMMON OPTIONS", "These are the command line options that are common for all methods. You can determine the mass to be chosen for the pruning process and the number of channels to be considered.")
bgroup.add_option("-c", "--channels", dest="channels", default="mm em mt et tt", type="string",
                  help="The list of channels, for which the datacards should be copied. The list should be embraced by call-ons and separeted by whitespace or comma. Available channels are mm, em, mt, et, tt, vhtt, hmm, hbb. [Default: \"mm em mt et tt\"]")
bgroup.add_option("-m", "--mass", dest="mass", default="125", type="string",
                  help="The mass value to be used to run the pruning algorithm on. [Default: 125]")
bgroup.add_option("--split-by-channel", dest="optSplit", default=False, action="store_true",
                  help="For option s --byPull and --byShift the caltulation of the maximum likelihood fit can be quite time consuming. Use this option to split the fit by channel. The pulls will then be picked up channel-wise. For correlated uncertainties the maximal pull will be chosen. [Default: \"False\"]")
bgroup.add_option("--shield-bins", dest="optShield", default=False, action="store_true",
                  help="Use this option if you want to prevent bins in the vicinity of an expected signal to be subject to bin-by-bin uncertainty pruning, even, if they have a small effect on pulls, relative shifts or limit. If this option is chosen the central value and the relative size of the window can be chosen by the parameters --shield-central and --shield-bounds as described below. [Default: \"False\"]")
bgroup.add_option("--fit-result", dest="fit_result", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the combined maximum likelihood fit if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
bgroup.add_option("--fit-result-mt", dest="fit_result_mt", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the mt channel if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
bgroup.add_option("--fit-result-et", dest="fit_result_et", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the et channel if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
bgroup.add_option("--fit-result-em", dest="fit_result_em", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the em channel if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
bgroup.add_option("--fit-result-mm", dest="fit_result_mm", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the mm channel if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
bgroup.add_option("--fit-result-tt", dest="fit_result_tt", default="",  type="string",
                  help="The main option --byPull and --byShift require a maximum likeihood fit to be run before pruning. This can be time consuming. It is possible to pass on the output of pre-calculated fits by this option. Give here the full path to the result file of the fit (mlfit.txt) for the tt channel if it exists already. If empty the fit will be performed within hits script. [Default: \"\"]")
parser.add_option_group(bgroup)
cgroup = OptionGroup(parser, "SHIELD-BINS OPTIONS", "These are the additional command line options when running the script with option --shield-bins. You can give the central value and the relative width of a mass window in which you want to prevent bins to be subject to bin-by-bin uncertainty pruning.")
cgroup.add_option("--shield-central", dest="shield_central", default="125", type="string",
                  help="Give a value here that corresponds to the central value of this window for option --shield-bins. [Default: 125]")
cgroup.add_option("--shield-bounds", dest="shield_bounds", default="0.3", type="string",
                  help="Give a value here that corresponds to the relative width of the window for option --shield-bins. The central value is given by option --shield-central. [Default: 0.3]")
parser.add_option_group(cgroup)
dgroup = OptionGroup(parser, "BYLIMIT OPTIONS", "These are the additional command line options when running the script with option --byLimit.")
dgroup.add_option("--limit-threshold", dest="limit_threshold", default="0.0025", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the relative difference on the limit result (split by channel) when taking the nuisance parameter of choice into account or not. [Default: 0.0025]")
dgroup.add_option("--limit-metric", dest="limit_metric", default="all",  type="choice", choices=['exp', 'obs', 'all'],
                  help="The metric to be used for pruning. Choices are: exp (maximal difference on expected limit only), obs (maximal difference on observed only), all (maximal difference on of observed or expected). [Default: 'all']")
parser.add_option_group(dgroup)
egroup = OptionGroup(parser, "BYPULL OPTIONS", "These are the additional command line options when running the script with option --byPull.")
egroup.add_option("--pull-threshold", dest="pull_threshold", default="0.05", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the pull of the parameter in the maximum likelihood fit. [Default: 0.05]")
egroup.add_option("--pull-metric", dest="pull_metric", default="all",  type="choice", choices=['b-only', 's+b', 'all'],
                  help="The metric to be used for pruning. Choices are: b-only (pull for b-only fit), s+b (pull for s+b fit), all (maximum of pull on b-only and s+b fit). [Default: 'all']")
parser.add_option_group(egroup)
fgroup = OptionGroup(parser, "BYSHIFT OPTIONS", "These are the additional command line options when running the script with option --byShift.")
fgroup.add_option("--shift-threshold", dest="shift_threshold", default="0.05", type="string",
                  help="The threshold to determine the nuisance parameters to be pruned. The value corresponds to the relative shift of the parameter in the maximum likelihood fit. [Default: 0.05]")
fgroup.add_option("--shift-metric", dest="shift_metric", default="all",  type="choice", choices=['b-only', 's+b', 'all'],
                  help="The metric to be used for pruning. Choices are: b-only (pull for b-only fit), s+b (pull for s+b fit), all (maximum of pull on b-only and s+b fit). [Default: 'all']")
parser.add_option_group(fgroup)
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
## configure options for --byPull or --byShift
if options.optByShift :
    options.optByPull = True
## in case of --split-by-channel prevent the max-likelihood fit
## from being performed on the fly
if options.optSplit :
    options.fit_result = 'BY-CHANNEL'
## defined thesholds and metrics
metric = ''
threshold = 0.
if options.optByShift :
    metric = options.shift_metric
    threshold = options.shift_threshold
    print "pruning: byShift (threshold:", options.shift_threshold, " metric:", options.shift_metric+")"
elif options.optByPull :
    metric = options.pull_metric
    threshold = options.pull_threshold    
    print "pruning: byPull  (threshold:", options.pull_threshold, " metric:", options.pull_metric+")"
elif options.optByLimit :
    metric = options.limit_metric
    threshold = options.limit_threshold
    print "pruning: byLimit (threshold:", options.limit_threshold, " metric:", options.limit_metric+")"
if options.optShield :
    print "shield :         (central  :", options.shield_central, "  bounds: +/-"+options.shield_bounds+")"
    
## setup directory structure for for logging
os.system("mkdir -p log")
os.system("mkdir -p log/pruning")
logdir = os.getcwd()+'/log/pruning'

def summarize_uncerts(values, chn=None) :
    """
    This function opens a root file and fills the values that the bin-by-bin
    uncertainties have into a histogram. Depending on the chosen method the
    boundaries of this histogram are adjusted.
    """
    path = logdir
    output = path+"/bin-by-bin-uncertainties-%s.root" % chn if chn else path+"/bin-by-bin-uncertainties.root"
    print "writing pulls/effect on limit to", output
    file = ROOT.TFile(output, "UPDATE")
    nbin = 150 if options.optByPull or options.optByShift else 150
    xmin = 0.  if options.optByPull or options.optByShift else -3.
    xmax = 1.5 if options.optByPull or options.optByShift else  0.
    hist = ROOT.TH1F("bin-by-bin", "bin-by-bin", nbin, xmin, xmax)
    for val in values :
        hist.Fill(val if options.optByPull else math.log10(val))
    file.Write("bin-by-bin")
    file.Close()

def walk_directory(dir, uncerts, bounds) :
    """
    This function walks the directory structure of the input file. It checks for histograms that follow
    the bin-by-bin uncertainty naming conventions. From these histograms it fills the actual value of
    the uncertainty and the boundaries of a user defined window around the mH mass region. These values
    are filled in two dictionaries of type:

     - uncert = {uncert_name, uncert}
     - bounds - {uncert_name, (lower-bound, upper-bound)}
    """
    for key in dir.GetListOfKeys() :
        name=key.GetName()
        if key.GetClassName().startswith('TDirectory') :
            #print "in directory: ", name
            walk_directory(dir.Get(name), uncerts, bounds)
        else :
            if isinstance(dir.Get(name), ROOT.TH1) :
                bbb = re.match("\s*\w+bin\_*(\d*)Up", name)
                if bbb :
                    ## Note: depending on the chosen statistics uncertainties can be
                    ## asymmetric also for histograms. Also there is cases where Down
                    ## has been forced to 0 if it lead to values smaller than 0.
                    upper = dir.Get(name)
                    value = dir.Get(name[:name.find('_CMS')])
                    lower = dir.Get(name.replace('Up', 'Down'))
                    bin_match = re.compile("\s*\w+bin\_*(\d*)\w*")
                    bins = bin_match.findall(name)
                    for bin in bins :
                        ibin = int(bin)
                        cen = float(options.shield_central)
                        bnd = float(options.shield_bounds)
                        ## Note: there is small inconsistency here as the uncertainty
                        ## histograms have been re-normalized to have the same integral
                        ## as the central value after shifting up the bin in question.
                        uncerts[name[name.find('CMS'):name.find('Up')]]=max(abs(value.GetBinContent(ibin)-lower.GetBinContent(ibin)), abs(value.GetBinContent(ibin)-upper.GetBinContent(ibin)))
                        bounds [name[name.find('CMS'):name.find('Up')]]=(value.GetXaxis().FindBin(cen-bnd*cen), value.GetXaxis().FindBin(cen+bnd*cen))

def mimic_pulls(path) :
    """
    Create a pseudo output file from individual channels to shortcut the maximum likelihood
    fit. Each single appearance of an uncertainty will be written to the combined output file.
    For multiple occurrences (corresponding to correlated uncertainties among channels), the
    line will the maximum pull will be chosen. The inputs are defined by options of this
    script.
    """
    inputs = {
        'mt' : options.fit_result_mt,
        'et' : options.fit_result_et,
        'em' : options.fit_result_em,
        'mm' : options.fit_result_mm,
        'tt' : options.fit_result_tt,
        }
    output = {}
    headline = ''
    pull_match = re.compile('[+-]\d+\.\d+(?=sig)')
    for (chn, input) in inputs.iteritems():
        file= open(input,'r')
        for line in file :
            ## add headline
            if 'name' in line :
                if headline == '' :
                    headline = line
                else :
                    continue
            ## fill outputs with uncertainties of this channel
            key = line.split()[0]
            if not key in output.keys() :
                output[key] = line
            else :
                pulls_old  = pull_match.findall(output[key])
                pulls_new  = pull_match.findall(line)
                if pulls_new :
                    val_old = max(abs(float(pulls_old[0])), float(pulls_old[1]))
                    val_new = max(abs(float(pulls_new[0])), float(pulls_new[1]))
                    if val_new > val_old :
                        output[key] = line
        file.close()
    file= open(path,'w')
    file.write(headline)
    for line in output.values() :
        file.write(line)
    file.close()

def load_auxiliaries(filename, uncerts, bounds) :
    """
    This function is called after the directory structure to apply the pruning has been
    set up to fill to auxiliary dictionaries: uncerts keeps the actual Up and Down
    uncertainty for a given uncertainty name; bounds keeps the lower and upper bound of
    the mass window to force bin-by-bin uncertainties in case this option is active.
    The returned structure of these dictionaries will be:

     - uncert = {uncert_name, uncert}
     - bounds - {uncert_name, (lower-bound, upper-bound)}

    where uncert_name corresponds to the unique name of the uncertainty histgoram up to
    the ending Up/Down.
    """
    input = ROOT.TFile(filename, 'READ')
    if not input :
        raise IOError("Can't open input file: %s" % filename)
    walk_directory(input, uncerts, bounds)
    input.Close()

def manipulate_bbb(datacard, manipulation, excludes=None) :
    """
    This function parses a datacard, finds those uncertainties that follow the naming
    conventions for bin-by-bin uncertainties and manipulates them. It can comment or
    uncomment them. If a list excludes is passed on it only acts on those uncerts,
    which are in this list.
    """
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

## fill a set of auxiliary dictionaires here that
## will be used when running with option --byShift
## or with option --shield-bins
uncerts = {}
bounds  = {}
for file in glob.glob("pruning/common/*.root") :
    load_auxiliaries(file, uncerts, bounds)

## change directory (needed by sizeUpsystematics.py)
massdir = options.mass
if '.0' in massdir :
    massdir = massdir.rstrip('0').rstrip('.')
os.chdir("pruning/{MASS}".format(MASS=massdir))

glob_all =0
glob_excl = 0
if options.optByLimit :
    ## metrics for pruning
    metric_exp    = lambda map : max(abs(map['exp']['AllIn']), abs(map['exp']['AllOut']));
    metric_obs    = lambda map : max(abs(map['obs']['AllIn']), abs(map['obs']['AllOut']));
    metric_all    = lambda map : max(metric_exp(map), metric_obs(map))
    metrics = { 'exp':metric_exp, 'obs':metric_obs, 'all':metric_all };
    metric = metrics[metric]
    
    ## pick up parameters from json file per channel
    def prune_by_limit(path, chn) :
        ## counters for monitoring
        out = 0
        all = 0
        shielded = 0
        ## list of all values for monitoring
        vals= []
        report = json.loads(" ".join([l for l in open(path,"r")]))
        if not report: raise RuntimError, "Couldn't load %s" % path
        toExclude = []
        for (nuisList, map) in report:
            all += 1
            outcome = metric(map)
            if options.debug :
                bbb = re.match("\w+bin\_*\d*\w*", nuisList[0])
                if bbb :
                    vals.append(float(outcome))
            if float(outcome) < float(threshold) :
                ## apply shielding of bins
                shield = False
                bin_match = re.compile("\s*\w+bin\_*(\d*)\w*")
                bins = bin_match.findall(name)
                for bin in bins :
                    ibin = int(bin)
                    if options.optShield :
                        if bounds[name][0]<ibin and ibin<bounds[name][1] :
                            shield=True
                if shield :
                    shielded += 1
                else :
                    out += 1
                    toExclude += nuisList
        print "excluded", out, "from", all, ": (", shielded, "rescued by shielding.)"
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
            cards = '{PARENT}/{INPUT}/htt_{CHN}/*_{CHN}_*.txt'.format(
                PARENT="" if parentdir in args[0] else parentdir,
                INPUT=args[0],
                CHN=chn
                )
            for datacard in glob.glob(cards) :
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
        if not options.fit_result == 'BY-CHANNEL' :
            os.system("cp {SRC} out/mlfit.txt".format(SRC=options.fit_result))
    ## pick up parameters from json file per channel
    def prune_by_pull(path) :
        ## counters for monitoring
        out = 0
        all = 0
        shielded = 0
        confused = 0
        ## list of all values for monitoring
        vals= []
        ## datacards input file
        os.system("pwd")
        print path
        file= open(path,'r')
        toExclude = []
        for line in file :
            name=line.split()[0]
            bbb = re.match("^#*\s*(\w+bin\_*\d*\w+)", name)
            if bbb :
                missmatch = False
                if not name in uncerts.keys() :
                    confused += 1
                    missmatch = True
                    print "Warning: bbb uncert:", name,  "not in list of bbb uncerts. This uncert will not be pruned."
                pull_match = re.compile('[+-]\d+\.\d+(?=sig)')
                pulls = pull_match.findall(line)
                if pulls :
                    all+= 1
                    val = 0.
                    ## define metric
                    if metric == 'b' :
                        val = float(pulls[0])
                    if metric == 's+b' :
                        val = float(pulls[1])
                    if metric == 'all' :
                        val = max(abs(float(pulls[0])), float(pulls[1]))
                    ## switch to byShift
                    if options.optByShift :
                        if not missmatch :
                            val*= uncerts[name]
                        else :
                            val = 999
                    if options.debug :
                        vals.append(val)
                    if abs(val) < float(threshold) :
                        ## apply shielding of bins
                        shield = False
                        bin_match = re.compile("\s*\w+bin\_*(\d*)\w*")
                        bins = bin_match.findall(name)
                        for bin in bins :
                            ibin = int(bin)
                            if not missmatch :
                                if options.optShield :
                                    if bounds[name][0]<ibin and ibin<bounds[name][1] :
                                        shield = True
                            else :
                                shield = True
                        if shield :
                            shielded += 1
                        else :
                            out += 1
                            toExclude.append(name)
        file.close()
        print "excluded", out, "from", all, ": (", shielded, "rescued by shielding,", confused, "not pruned due to missmatch of inputs.)"
        if options.debug :
            summarize_uncerts(vals)
        return toExclude
    ## prune datacards for given channel
    if options.optSplit :
        mimic_pulls("out/mlfit.txt")
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
        cards = '{PARENT}/{INPUT}/htt_{CHN}/*.txt'.format(
            PARENT="" if parentdir in args[0] else parentdir,
            INPUT=args[0],
            CHN=chn
            )
        for datacard in glob.glob(cards) :
            ## comment bin-by-bin uncertainties
            manipulate_bbb(datacard, "COMMENT", excludes)
        glob_all += all
        glob_excl += excl

## a short summary
if glob_all>0 :
    print "Summary:"
    print "commented", glob_excl, "bin-by-bin uncertainties from", glob_all, "for all channels. (", float(100*glob_excl/glob_all), "%)"
## clean up if not requested otherwise
os.system("cp out/mlfit.txt {LOG}".format(LOG=logdir))
os.chdir(parentdir)
os.system("rm -rf pruning")
