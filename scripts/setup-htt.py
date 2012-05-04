#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Simple script to setup the limit calculation for htt and ztt measurements. The script relies on the machienery of automatic datacard creation detailed in the setup directory of this package. Apart from options there is no further argument for this script.")
parser.add_option("-n", "--name", dest="name", default="xxxx-test", type="string", help="Name of the working directory. The tool will create two subdirectories mssm and sm, in which it will create subdirectories for all masspoints available for the analysis [Default: xxxx-test]")
parser.add_option("--sm-masses", dest="sm_masses", default="110 115 120 125 130 135 140 145", type="string", help="Available SM mass points [Default: 110 115 120 125 130 135 140 145]")
parser.add_option("--mssm-masses", dest="mssm_masses", default="90 100 120 130 140 160 180 200 250 300 350 400 450 500", type="string", help="Available MSSM mass points [Default: 90 100 120 130 140 160 180 200 250 300 350 400 450 500]")
parser.add_option("--analysis", dest="analysis", default="all", type="choice", help="Choose between sm or mssm analysis [Default: all]", choices=["sm", "mssm", "all"])
parser.add_option("--category", dest="category", default="all", type="choice", help="Choose between event categories (depending on analysis) [Default: all]", choices=["cmb", "incl", "btag", "nobtag", "novbf", "vbf", "boost", "all"])
parser.add_option("--channel", dest="channel", default="all", type="choice", help="Choose between ditau decay channels [Default: all]", choices=["cmb", "emu", "etau", "mutau", "all"])
parser.add_option("--drop-channels", dest="drop",default="", type="string", help="Scale the given channels to 0. in the datacards. (This action will be applied to all channels that match the given string patterns, which may be on as a whitespace or ',' separated list). [Default: \"\"]")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

## create main directory
os.system("mkdir %s" % options.name)
os.chdir("%s/%s" % (os.getcwd(), options.name))

## fill optionals
optionals = ""
if options.drop != "":
    optionals+=" --drop-channels '%s'" % options.drop 

## setup mssm directories
if options.analysis == "mssm" or options.analysis == "all":
    os.system("mkdir mssm")
    os.chdir("%s/mssm" % os.getcwd())
    ## individual event categories for all channels
    if options.channel == "cmb" or options.channel == "all":
        if options.category == "cmb" or options.category == "all" :
            os.system("setup-batch.py -n cmb    -c em  -o htt_em_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n cmb    -c et  -o htt_et_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n cmb    -c mt  -o htt_mt_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n cmb    -c em  -o htt_em_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n cmb    -c et  -o htt_et_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n cmb    -c mt  -o htt_mt_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))        
        if options.category == "all" or options.category == "btag" :
            os.system("setup-batch.py -n btag   -c em  -o htt_em_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n btag   -c et  -o htt_et_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n btag   -c mt  -o htt_mt_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
        if options.category == "all" or options.category == "incl" :
            os.system("setup-batch.py -n incl   -c em  -o htt_em_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n incl   -c et  -o htt_et_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))
            os.system("setup-batch.py -n incl   -c mt  -o htt_mt_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))
    ## individual event categories for individual channels
    if options.channel == "emu" or options.channel == "all" :
        if options.category == "cmb" or options.category == "all" or options.category == "nobtag" :
            os.system("setup-batch.py -n emu    -c em  -o htt_em_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
        if options.category == "cmb" or options.category == "all" or options.category == "btag" :
            os.system("setup-batch.py -n emu    -c em  -o htt_em_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
        if options.category == "incl" :
            os.system("setup-batch.py -n emu    -c em  -o htt_em_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))            
    if options.channel == "etau" or options.channel == "all" :
        if options.category == "cmb" or options.category == "all" or options.category == "nobtag" :
            os.system("setup-batch.py -n etau   -c et  -o htt_et_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
        if options.category == "btag"   or options.category == "cmb" or options.category == "all" :
            os.system("setup-batch.py -n etau   -c et  -o htt_et_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
        if options.category == "incl" :
            os.system("setup-batch.py -n etau   -c et  -o htt_et_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))            
    if options.channel == "mutau" or options.channel == "all" :
        if options.category == "nobtag" or options.category == "cmb" or options.category == "all" :
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_0.txt -e MSSM-00  %s %s" % (optionals, options.mssm_masses))
        if options.category == "btag"   or options.category == "cmb" or options.category == "all" :
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_1.txt -e MSSM-01  %s %s" % (optionals, options.mssm_masses))
        if options.category == "incl" :
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_x.txt -e MSSM-xx  %s %s" % (optionals, options.mssm_masses))
    os.chdir("%s/.." % os.getcwd())

## setup sm directories
if options.analysis == "sm" or options.analysis == "all":
    os.system("mkdir sm")
    os.chdir("%s/sm" % os.getcwd())
    ## all categories combined
    if options.channel == "cmb" or options.channel == "all":
        ## individual event categories for all channels
        if options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n cmb    -c em  -o htt_em_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c em  -o htt_em_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c em  -o htt_em_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c et  -o htt_et_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c et  -o htt_et_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c et  -o htt_et_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c mt  -o htt_mt_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c mt  -o htt_mt_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n cmb    -c mt  -o htt_mt_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
        if options.category == "novbf" or options.category == "all":
            os.system("setup-batch.py -n novbf  -c em  -o htt_em_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n novbf  -c et  -o htt_et_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n novbf  -c mt  -o htt_mt_0.txt -e SM-00    %s %s" % (optionals, options.sm_masses  ))
        if options.category == "boost" or options.category == "all":
            os.system("setup-batch.py -n boost  -c em  -o htt_em_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n boost  -c et  -o htt_et_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n boost  -c mt  -o htt_mt_1.txt -e SM-01    %s %s" % (optionals, options.sm_masses  ))
        if options.category == "vbf" or options.category == "all":
            os.system("setup-batch.py -n vbf    -c em  -o htt_em_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n vbf    -c et  -o htt_et_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n vbf    -c mt  -o htt_mt_2.txt -e SM-02    %s %s" % (optionals, options.sm_masses  ))
        if options.category == "incl":
            os.system("setup-batch.py -n incl   -c em  -o htt_em_x.txt -e SM-xx    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n incl   -c et  -o htt_et_x.txt -e SM-xx    %s %s" % (optionals, options.sm_masses  ))
            os.system("setup-batch.py -n incl   -c mt  -o htt_mt_x.txt -e SM-xx    %s %s" % (optionals, options.sm_masses  ))            
    ## individual event categories for individual channels
    if options.channel == "emu" or options.channel == "all":
        if options.category == "novbf" or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n emu    -c em  -o htt_em_0.txt  -e SM-00   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "boost" or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n emu    -c em  -o htt_em_1.txt  -e SM-01   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n emu    -c em  -o htt_em_2.txt  -e SM-02   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "incl":
            os.system("setup-batch.py -n emu    -c em  -o htt_em_x.txt  -e SM-xx   %s %s" % (optionals, options.sm_masses  ))                
    ## all categories in the etau channel
    if options.channel == "etau" or options.channel == "all":
        if options.category == "novbf" or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n etau   -c et  -o htt_et_0.txt  -e SM-00   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "boost" or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n etau   -c et  -o htt_et_1.txt  -e SM-01   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n etau   -c et  -o htt_et_2.txt  -e SM-02   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "incl":
            os.system("setup-batch.py -n etau   -c et  -o htt_et_x.txt  -e SM-xx   %s %s" % (optionals, options.sm_masses  ))                
    ## all categories in the mutau channel
    if options.channel == "mutau" or options.channel == "all":
        if options.category == "novbf" or options.category == "cmb" or options.category == "all":            
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_0.txt  -e SM-00   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "boost" or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_1.txt  -e SM-01   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_2.txt  -e SM-02   %s %s" % (optionals, options.sm_masses  ))
        if options.category == "incl":
            os.system("setup-batch.py -n mutau  -c mt  -o htt_mt_x.txt  -e SM-xx   %s %s" % (optionals, options.sm_masses  ))
