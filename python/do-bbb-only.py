#!/usr/bin/env python

import os

##
## MORIOND-BIN-BY-BIN
##
dir = '.'
ana = 'setups_Imperial/scale-test'
channels = ['em', 'et', 'mt', 'tt']

os.system("cp -r {SOURCE} {SOURCE}-bbb".format(SOURCE=ana))
ana+='-bbb'

for chn in channels :
    if 'mm' in channels :
        ## setup bbb uncertainties for mm (172)
        os.system("add_bbb_errors.py 'mm:7TeV,8TeV:01,03,05:ZTT,TTJ' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
    if 'em' in channels :
        ## setup bbb uncertainties for em (103)
        os.system("add_bbb_errors.py 'em:7TeV,8TeV:01,03,05:Fakes' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
    if 'et' in channels :
        ## setup bbb uncertainties for et 7TeV, (117)
        os.system("add_bbb_errors.py 'et:7TeV:01,03,05:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
                    ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        ## setup bbb uncertainties for et 8TeV, (112)                
        os.system("add_bbb_errors.py 'et:8TeV:01,03,05:ZL,ZJ,QCD>W'  --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        ## setup bbb uncertainties for et 8TeV, (???)                
        os.system("add_bbb_errors.py 'et:8TeV:02:QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                
    if 'mt' in channels :
        ## setup bbb uncertainties for mt 7TeV (118)
        os.system("add_bbb_errors.py 'mt:7TeV:01,03,05:ZL,ZLL,QCD>W' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        ## setup bbb uncertainties for mt 8TeV (120)
        os.system("add_bbb_errors.py 'mt:8TeV:01,03,05:ZL,ZJ,QCD>W'  --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))                
    if 'tt' in channels :
        ## setup bbb uncertainties for tt (48)
        os.system("add_bbb_errors.py 'tt:8TeV:00,01:ZTT,QCD' --normalize -f --in {DIR}/{ANA} --out {DIR}/{ANA}-tmp --threshold 0.10".format(
            DIR=dir,
            ANA=ana
            ))
        os.system("rm -rf {DIR}/{ANA}".format(DIR=dir, ANA=ana))
        os.system("mv {DIR}/{ANA}-tmp {DIR}/{ANA}".format(DIR=dir, ANA=ana))


os.system("setup-datacards.py -i {INPUT} -o {OUTPUT} -p 8TeV -c 'em et mt' 125".format(
    INPUT =ana,
    OUTPUT=ana.replace("setups", "aux")
    ))

os.system("setup-htt.py -i {INPUT} -o {OUTPUT} -p 8TeV -c 'em et mt' 125".format(
    INPUT =ana.replace("setups", "aux"),
    OUTPUT=ana.replace("setups", "LIMITS")
    ))

