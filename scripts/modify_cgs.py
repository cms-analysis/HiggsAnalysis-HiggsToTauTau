#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--analysis", "-a", default='sm', dest="analysis", help="Choose here between sm and mssm analysis. [Default: 'sm']")
parser.add_argument("--setup", "-s", default='', dest="setuppath", help="Absolute path to the setup directory, in which the operation should take place. [Default: '']")
parser.add_argument("--channels", "-c", nargs="*", dest="channels", help="Channels to be considered.")
parser.add_argument("--periods", "-p", nargs="*", dest="periods", help="Periods to be considered.")
parser.add_argument("--categories", "-cat", nargs="*", dest="categories", help="Categories to be edited.")
parser.add_argument("--add-to-signal", "-as", nargs="*", dest="addsignal", help="Processes to be added to the signal.")
parser.add_argument("--add-to-background", "-ab", nargs="*", default='', dest="addbackground", help="Processes to be added to the background.")
opt=parser.parse_args()

import os
import re
from HiggsAnalysis.HiggsToTauTau.UncertAdaptor import UncertAdaptor

def main() :
    print "# --------------------------------------------------------------------------------------"
    print "# Modify cgs.conf file. "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --setup             :", opt.setuppath
    print "# --channels          :", opt.channels
    print "# --periods           :", opt.periods
    print "# --categories        :", opt.categories
    print "# --add-to-signal     :", opt.addsignal
    print "# --add-to-background :", opt.addbackground
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"

    setuppath=opt.setuppath
    cgs_shuffle = UncertAdaptor()
    for channel in opt.channels :
        for period in opt.periods :
            for category in opt.categories :
                filename="{SETUP}/{CHANNEL}/cgs-{ANA}-{PERIOD}-{CATEGORY}.conf".format(SETUP=setuppath, CHANNEL=channel, ANA=opt.analysis, PERIOD=period, CATEGORY=category)
                print 'processing file:', filename
                cgs_shuffle.cgs_processes(filename, opt.addsignal, opt.addbackground)

main()
