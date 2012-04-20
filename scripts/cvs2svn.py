#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Simple script to copy input files for limit and significance calculation from CVS to SVN. A list of arguments can be given. These arguments should be integers corresponding to the mass points for which you want to copy the datacards.")
parser.add_option("-i", "--input", dest="input", default="UserCode/MBachtis/htautau/sm", type="string", help="Mikes input directory [Default: UserCode/MBachtis/htautau/sm]")
parser.add_option("-o", "--out", dest="out", default="lp11", type="string", help="Name of the output directory [Default: lp11]")
parser.add_option("-c", "--channel", dest="channel", default="sm", type="choice", help="Channel to be copied [Default: sm]", choices=["sm", "emu", "etau", "mutau", "mumu"])
parser.add_option("--SM4", dest="sm4", default=False, action="store_true", help="Copy SM4 datacards [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

pre = ""
if options.sm4 :
    pre = "SM4_"

for mass in parseArgs(args) :
    if options.channel == "emu" or options.channel == "sm" :
        os.system("cp {input}/htt_em_0-{mass}.txt {output}/{mass}/{pre}htt_em_0.txt".format(input=options.input, output=options.out, pre=pre, mass=mass))
        os.system("perl -pi -e 's/htt_em.input.root/..\/common\/{pre}htt_em.input.root/g' {output}/{mass}/{pre}htt_em_0.txt".format(pre=pre, output=options.out, mass=mass))
        os.system("cp {input}/htt_em_1-{mass}.txt {output}/{mass}/{pre}htt_em_1.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_em.input.root/..\/common\/{pre}htt_em.input.root/g' {output}/{mass}/{pre}htt_em_1.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_em_2-{mass}.txt {output}/{mass}/{pre}htt_em_2.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_em.input.root/..\/common\/{pre}htt_em.input.root/g' {output}/{mass}/{pre}htt_em_2.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_em.input.root {output}/common/{pre}htt_em.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
    if options.channel == "etau" or options.channel == "sm" :
        os.system("cp {input}/htt_et_0-{mass}.txt {output}/{mass}/{pre}htt_et_0.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_et.input.root/..\/common\/{pre}htt_et.input.root/g' {output}/{mass}/{pre}htt_et_0.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_et_1-{mass}.txt {output}/{mass}/{pre}htt_et_1.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_et.input.root/..\/common\/{pre}htt_et.input.root/g' {output}/{mass}/{pre}htt_et_1.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_et_2-{mass}.txt {output}/{mass}/{pre}htt_et_2.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_et.input.root/..\/common\/{pre}htt_et.input.root/g' {output}/{mass}/{pre}htt_et_2.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_et.input.root {output}/common/{pre}htt_et.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
    if options.channel == "mutau" or options.channel == "sm" :
        os.system("cp {input}/htt_mt_0-{mass}.txt {output}/{mass}/{pre}htt_mt_0.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_mt.input.root/..\/common\/{pre}htt_mt.input.root/g' {output}/{mass}/{pre}htt_mt_0.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_mt_0-{mass}.txt {output}/{mass}/{pre}htt_mt_1.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_mt.input.root/..\/common\/{pre}htt_mt.input.root/g' {output}/{mass}/{pre}htt_mt_1.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_mt_0-{mass}.txt {output}/{mass}/{pre}htt_mt_2.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/htt_mt.input.root/..\/common\/{pre}htt_mt.input.root/g' {output}/{mass}/{pre}htt_mt_2.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/htt_mt.input.root {output}/common/{pre}htt_mt.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
    if options.channel == "mumu" : ## or options.channel == "sm" :
        os.system("cp {input}/muMu_SM0_mH{mass}.txt {output}/{mass}/{pre}htt_mm_0.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/muMu_SM0_mH{mass}.root/{pre}htt_mm_0.input.root/g' {output}/{mass}/{pre}htt_mm_0.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/muMu_SM0_mH{mass}.root {output}/{mass}/{pre}htt_mm_0.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
        os.system("cp {input}/muMu_SM1_mH{mass}.txt {output}/{mass}/{pre}htt_mm_1.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/muMu_SM1_mH{mass}.root/{pre}htt_mm_1.input.root/g' {output}/{mass}/{pre}htt_mm_1.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/muMu_SM1_mH{mass}.root {output}/{mass}/{pre}htt_mm_1.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
        os.system("cp {input}/muMu_SM2_mH{mass}.txt {output}/{mass}/{pre}htt_mm_2.txt".format(input=options.input, output=options.out, mass=mass, pre=pre))
        os.system("perl -pi -e 's/muMu_SM2_mH{mass}.root/{pre}htt_mm_2.input.root/g' {output}/{mass}/{pre}htt_mm_2.txt".format(output=options.out, mass=mass, pre=pre))
        os.system("cp {input}/muMu_SM2_mH{mass}.root {output}/{mass}/{pre}htt_mm_2.input.root".format(input=options.input, output=options.out, mass=mass, pre=pre))        
  
