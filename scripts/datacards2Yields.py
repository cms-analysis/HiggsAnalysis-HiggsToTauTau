#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import *

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Script to extract event yields for data, signal and background from a set of input datacards. ARGS corresponds to the datacards, which are the input to the script. The script will extract the yields and the names of the signal an background templates and print them to the default output. Finally it will print a sum of all yields across all inputs datacards to the default output. This script is applicable for counting experiments and binned likelihood analyses. it makes use of the HiggsAnalysis/CombinedLimit/python/DatacardsParser, which needs to be accessible from your working area.'")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
yield_opts = OptionGroup(parser, "YIELD OPTIONS", "These are the options that can be passed on to configure the printout to the default output.")
yield_opts.add_option("--channel-name", dest="channel_name", default="", type="string",
                  help="You can use this option to specify a certaint channel name that will be added to the output. [Default: \"\"]")
yield_opts.add_option("--group-processes", dest="group_processes", default="", type="string",
                  help="You can use this option to group several processes under a single process name. The required syntax is GROUPNAME1:PROC1-1,PROC1-2,PROC1-3 GROUPNAME2:PROC2-1,PROC2-2,PROC2-3 ... aso. [Default: \"\"]")
parser.add_option_group(yield_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os

## determine process groups
process_groups = {}
for group in options.group_processes.split() :
    process_groups[group.split(':')[0]] = group.split(':')[1].split(',')

## global counters for yield
obs = 0
sig = {}
bgr = {}

## loop files
for path in args :
    file = open(path, 'r')
    card = parseCard(file, options)
    ## initialize dictionary
    for proc in card.list_of_signals() :
        if not proc in sig.keys() :
            sig[proc] = 0
    for proc in card.list_of_backgrounds() :
        if not proc in bgr.keys() :
            bgr[proc] = 0
    # sum up yields
    for bin in card.list_of_bins() :
        obs+=card.obs[bin]
        for proc in card.list_of_signals() :
            sig[proc]+= card.rate(bin, proc)
        for proc in card.list_of_backgrounds() :
            bgr[proc]+= card.rate(bin, proc)
    file.close()

def save_add(target, elem_key, elem_val) :
    """
    add elem to the dictionary or add it to an existing entry
    """
    if not elem_key in target.keys() :
        target[elem_key] =elem_val
    else :
        target[elem_key]+=elem_val
                
def compactify(source_dict, groups) :
    """
    write extended list of processes into a more compact way is configured such 
    """
    blacklist = []
    target_dict = {}
    for key, val in source_dict.iteritems() :
        for group, procs in groups.iteritems() :
            if key in procs :
                blacklist.append(key)
                save_add(target_dict, group, val)
    ## add remaining elements
    for key, val in source_dict.iteritems() :
        if not key in blacklist :
            save_add(target_dict, key  , val)
    return target_dict
                
## compactify table row if configured such
if process_groups.keys() :
    sig = compactify(sig, process_groups)
    bgr = compactify(bgr, process_groups)

## do the printing
procs  = ' &\t'
yields = options.channel_name+' &\t'
## add signal to string
for n, y in sig.iteritems() :
    procs +=n+' &\t'
    yields+='{YIELD}'.format(YIELD=y)+' &\t'
## add background to string
for n, y in bgr.iteritems() :
    procs +=n+' &\t'
    yields+='{YIELD}'.format(YIELD=y)+' &\t'
## add data to string
print "%% ----------------------------------------------------------------------------------------------------"
procs += 'Data'    +' \\\ \hline \\\ '
yields+= '{OBS}'.format(OBS=obs)+' \\\ \hline \\\ '
print procs
print yields
print "%% ----------------------------------------------------------------------------------------------------"
