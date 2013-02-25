#!/usr/bin/env python

import os

update_searches  = True
update_couplings = False

## do not forget NOT to scale htt_mm once it comes in
print "**********************************************"
print "*"
print "* update cvs and setups                       "
print "*"
print "**********************************************"
## w/  preprocessed htt_mm inputs
#os.system("doSM.py --update-cvs --update-setup --skip-mm-in-scaling --a pruned --label UPLOAD 110-145:5")
## w/o preprocessed htt_mm inputs
##os.system("doSM.py --update-cvs --update-setup --a pruned --label UPLOAD 110-145")
## do the morphing for em, et, mt, tt
print "**********************************************"
print "*"
print "* do morphing                                 "
print "*"
print "**********************************************"
#os.system("python HiggsAnalysis/HiggsToTauTau/python/do-morphing-only.py")

if update_searches :
    ## continue the setup to aux_search
    print "**********************************************"
    print "*"
    print "* setting up datacards (searches)             "
    print "*"
    print "**********************************************"
    ## w/  preprocessed htt_mm inputs
    os.system("setup-datacards.py --no-fudge-for-mm -i setups_UPLOAD/pruned -o aux_searches -c 'em et mt mm tt' 110-140:0.5 141-145")
    ## w/o preprocessed htt_mm inputs
    ##os.system("setup-datacards.py --merge-no-signal -i setups_UPLOAD/pruned -o aux_searches 110-140:0.5 141-145")
    print "**********************************************"
    print "*"
    print "* apply pruning (searches)                    "
    print "*"
    print "**********************************************"
    os.system("python HiggsAnalysis/HiggsToTauTau/scripts/prune_bbb_errors.py -c 'em et mt mm tt' --byShift --fit-result $PWD/auxiliaries/datacards/mlfit-em+et+mt+mm+tt-130209-split.txt --shift-threshold 0.30 --shield-bins aux_searches/sm")
    print "**********************************************"
    print "*"
    print "* introduce Higgs as BG (searches)            "
    print "*"
    print "**********************************************"
    os.system("addHiggs2BG.py --mass 126 aux_searches")
    print "**********************************************"
    print "*"
    print "* upload datacards (searches)                 "
    print "*"
    print "**********************************************"
    os.system("cvs2local.py -i aux_searches  -o moriond2013/searches/htt  -c 'em et mt mm tt' 110-140:0.5 141-145")

if update_couplings :
    ## continue the setup to aux_couplings
    print "**********************************************"
    print "*"
    print "* setting up datacards (couplings)            "
    print "*"
    print "**********************************************"
    os.system("setup-datacards.py --no-fudge-for-mm -i setups_UPLOAD/pruned -o aux_couplings -c 'mm em et mt tt' 124.5-126.5:0.1")
    print "**********************************************"
    print "*"
    print "* apply pruning (couplings)                   "
    print "*"
    print "**********************************************"
    os.system("python HiggsAnalysis/HiggsToTauTau/scripts/prune_bbb_errors.py -c 'em et mt mm tt' --byShift --fit-result $PWD/auxiliaries/datacards/mlfit-em+et+mt+mm+tt-130209-split.txt --shift-threshold 0.30 --shield-bins --mass 125.0 aux_couplings/sm")
    print "**********************************************"
    print "*"
    print "* upload datacards (couplings)                "
    print "*"
    print "**********************************************"
    os.system("cvs2local.py -i aux_couplings -o moriond2013/couplings/htt -c 'em et mt mm tt' 124.5-126.5:0.1")
