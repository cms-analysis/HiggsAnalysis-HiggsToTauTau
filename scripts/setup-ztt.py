#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to setup the calculation of a Ztt cross section measurement using combine with method -M MaxLikelihoodFit. The script relies on the machinery of automatic datacard creation detailed in the setup directory of this package. Apart from options there is no further argument for this script.")
parser.add_option("-n", "--name", dest="name", default="xxxx-test", type="string", help="Name of the working directory. [Default: xxxx-test]")
parser.add_option("--category", dest="category", default="all", type="choice", help="Choose between event categories (depending on analysis) [Default: all]", choices=["cmb", "incl", "vbf", "boost", "all"])
parser.add_option("--channel", dest="channel", default="all", type="choice", help="Choose between ditau decay channels [Default: all]", choices=["cmb", "emu", "etau", "mutau", "all"])

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

## create main directory
os.system("mkdir %s" % options.name)
os.chdir("%s/%s" % (os.getcwd(), options.name))

## all categories combined
if options.channel == "cmb" or options.channel == "all":
    ## individual event categories for all channels
    if options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n cmb   -c em -o ztt_em_0.txt -e ZTT-00  xsec")
        os.system("setup-batch.py -n cmb   -c em -o ztt_em_1.txt -e ZTT-01  xsec")
        os.system("setup-batch.py -n cmb   -c em -o ztt_em_2.txt -e ZTT-02  xsec")
        os.system("setup-batch.py -n cmb   -c et -o ztt_et_0.txt -e ZTT-00  xsec")
        os.system("setup-batch.py -n cmb   -c et -o ztt_et_1.txt -e ZTT-01  xsec")
        os.system("setup-batch.py -n cmb   -c et -o ztt_et_2.txt -e ZTT-02  xsec")
        os.system("setup-batch.py -n cmb   -c mt -o ztt_mt_0.txt -e ZTT-00  xsec")
        os.system("setup-batch.py -n cmb   -c mt -o ztt_mt_1.txt -e ZTT-01  xsec")
        os.system("setup-batch.py -n cmb   -c mt -o ztt_mt_2.txt -e ZTT-02  xsec")
    if options.category == "novbf":
        os.system("setup-batch.py -n novbf -c em -o ztt_em_0.txt -e ZTT-00  xsec")
        os.system("setup-batch.py -n novbf -c et -o ztt_et_0.txt -e ZTT-00  xsec")
        os.system("setup-batch.py -n novbf -c mt -o ztt_mt_0.txt -e ZTT-00  xsec")
    if options.category == "boost":
        os.system("setup-batch.py -n boost -c em -o ztt_em_1.txt -e ZTT-01  xsec")
        os.system("setup-batch.py -n boost -c et -o ztt_et_1.txt -e ZTT-01  xsec")
        os.system("setup-batch.py -n bosst -c mt -o ztt_mt_1.txt -e ZTT-01  xsec")
    if options.category == "vbf":
        os.system("setup-batch.py -n vbf   -c em -o ztt_em_2.txt -e ZTT-02  xsec")
        os.system("setup-batch.py -n vbf   -c et -o ztt_et_2.txt -e ZTT-02  xsec")
        os.system("setup-batch.py -n vbf   -c mt -o ztt_mt_2.txt -e ZTT-02  xsec")
    if options.category == "incl":
        os.system("setup-batch.py -n incl  -c em -o ztt_em_x.txt -e ZTT-xx  xsec")
        os.system("setup-batch.py -n incl  -c et -o ztt_et_x.txt -e ZTT-xx  xsec")
        os.system("setup-batch.py -n incl  -c mt -o ztt_mt_x.txt -e ZTT-xx  xsec")            
## individual event categories for individual channels
if options.channel == "emu" or options.channel == "all":
    if options.category == "novbf" or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n emu   -c em -o ztt_em_0.txt -e ZTT-00  xsec")
    if options.category == "boost" or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n emu   -c em -o ztt_em_1.txt -e ZTT-01  xsec")
    if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n emu   -c em -o ztt_em_2.txt -e ZTT-02  xsec")
    if options.category == "incl":
        os.system("setup-batch.py -n emu   -c em -o ztt_em_x.txt -e ZTT-xx  xsec")                
if options.channel == "etau" or options.channel == "all":
    if options.category == "novbf" or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n etau  -c et -o ztt_et_0.txt -e ZTT-00  xsec")
    if options.category == "boost" or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n etau  -c et -o ztt_et_1.txt -e ZTT-01  xsec")
    if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n etau  -c et -o ztt_et_2.txt -e ZTT-02  xsec")
    if options.category == "incl":
        os.system("setup-batch.py -n etau  -c et -o ztt_et_x.txt -e ZTT-xx  xsec")                
if options.channel == "mutau" or options.channel == "all":
    if options.category == "novbf" or options.category == "cmb" or options.category == "all":            
        os.system("setup-batch.py -n mutau -c mt -o ztt_mt_0.txt -e ZTT-00  xsec")
    if options.category == "boost" or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n mutau -c mt -o ztt_mt_1.txt -e ZTT-01  xsec")
    if options.category == "vbf"   or options.category == "cmb" or options.category == "all":
        os.system("setup-batch.py -n mutau -c mt -o ztt_mt_2.txt -e ZTT-02  xsec")
    if options.category == "incl":
        os.system("setup-batch.py -n mutau -c mt -o ztt_mt_x.txt -e ZTT-xx  xsec")
