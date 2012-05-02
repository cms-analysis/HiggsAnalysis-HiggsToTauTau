#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Simple script to copy input files for limit and significance calculation from SVN to local. A list of arguments can be given. These arguments (ARGS) should be integers corresponding to the mass points for which you want to copy the datacards.")
parser.add_option("-i", "--input", dest="input", default="lp11/", type="string", help="LP11 input directory [Default: lp11/]")
parser.add_option("-o", "--out", dest="out", default="cmb", type="string", help="Name of the output directory [Default: cmb]")
parser.add_option("-c", "--channel", dest="channel", default="all", type="choice", help="Channel to be copied [Default: all]", choices=["all", "htt", "hgg", "hbb", "hww", "hzz4l", "hzz2l2q", "hzz2l2nu", "hzz2l2t"])
parser.add_option("--SM4", dest="sm4", default=False, action="store_true", help="Copy SM4 datacards [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

prefix = ""
if options.sm4 :
    prefix = "SM4_"

for mass in parseArgs(args) :
    print "{output}/{mass}".format(output=options.out, mass=mass)
    if not os.path.exists("{output}/{mass}".format(output=options.out, mass=mass)) :            
        os.system("mkdir {output}/{mass}".format(output=options.out, mass=mass))
    if not os.path.exists("{output}/common".format(output=options.out)) :            
        os.system("mkdir {output}/common".format(output=options.out))       
    if options.channel == "htt" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}htt_et* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/{pre}htt_mt* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/{pre}htt_em* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/{pre}htt_mm* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/{pre}vhtt*.txt   {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/vhtt_shapes.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/common/{pre}htt_*.root {output}/common/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hgg" or options.channel == "all" :
        ## for hgg copy the input file which is common for all masspoints from common to common
        #os.system("cp {input}/common/{pre}hggmva.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        #os.system("cp {input}/common/{pre}hgg*.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/{mass}/{pre}hgg{SM4}_*.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix, SM4="NOVBF" if options.sm4 else ""))
        os.system("cp {input}/common/{pre}hgg*.root {output}/common/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hbb" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}vhbb_* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hww" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}hww* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hzz4l" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}hzz4l_* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hzz2l2q" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}hzz2l2q_* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hzz2l2nu" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}hzz2l2nu_* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
    if options.channel == "hzz2l2t" or options.channel == "all" :
        os.system("cp {input}/{mass}/{pre}hzz2l2t_* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass, pre=prefix))
        os.system("cp {input}/common/{pre}hzz2l2t_* {output}/common/".format(input=options.input, output=options.out, pre=prefix))
    ## check if directory is empty -- if yes remove it from the list of masspoints to be submited
    if len(os.listdir("{output}/{mass}".format(output=options.out, mass=mass))) == 0 :
        os.system("rm -r {output}/{mass}".format(output=options.out, mass=mass))
