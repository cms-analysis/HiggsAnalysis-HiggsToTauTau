#!/usr/bin/env python

from optparse import OptionParser
       
parser = OptionParser(usage="usage: %prog [options]",
                      description="script to prepare datacards from inputfiles and to copy them to cvs.")
parser.add_option("-n", "--name", dest="name", default="new-datacards", type="string", help="Name of the directory, which is meant to contain the new datacards. [Default: new-datacards]")
parser.add_option("--SM4", dest="SM4", default=False, action="store_true", help="Re-scale signal samples in input file according to SM4 cross section*BR before datacard creation. [Default: false]")
(options, args) = parser.parse_args()

import os

## main working directory
base_directory = os.getcwd()+'/'+options.name
## list of all masses
masses = [110,111,112,113,114,115,116,117,118,119,
          120,121,122,123,124,125,126,127,128,129,
          130,131,132,133,134,135,136,137,138,139,
          140,141,142,143,144,145
          ]
## create main working directory
os.system("mkdir %s" % options.name)

os.chdir(base_directory)
os.system("mkdir emu")
for category in [0,1,2] : 
    os.chdir(base_directory+'/emu')
    os.system("datacard-project.py -c em -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/emu/SM{CAT}".format(CAT=category))
    os.system("mv em.inputs-sm.root htt_em.input.root")
    if options.SM4 :
        ## all cross section will be rescaled in one go
        os.system(r"root -q -l -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescale2SM4.C+\(true,\"htt_em.input.root\"\)".format(CMSSW_BASE=os.environ['CMSSW_BASE']))
    for mass in masses :
        os.system("create-datacard.py -i htt_em.input.root -o htt_em_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))
    ## cleanup
    os.chdir(base_directory+'/emu')
    os.system("cp SM{CAT}/*.* .".format(CAT=category))
    os.system("rm -r SM{CAT}".format(CAT=category))
os.system("rm cgs.* unc.*")

os.chdir(base_directory)
os.system("mkdir etau")
for category in [0,1,2] : 
    os.chdir(base_directory+'/etau')
    os.system("datacard-project.py -c et -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/etau/SM{CAT}".format(CAT=category))
    os.system("mv et.inputs-sm.root htt_et.input.root")
    if options.SM4 :
        ## all cross section will be rescaled in one go
        os.system(r"root -q -l -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescale2SM4.C+\(true,\"htt_et.input.root\"\)".format(CMSSW_BASE=os.environ['CMSSW_BASE']))
    for mass in masses :
        os.system("create-datacard.py -i htt_et.input.root -o htt_et_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))
    ## cleanup
    os.chdir(base_directory+'/etau')
    os.system("cp SM{CAT}/*.* .".format(CAT=category))
    os.system("rm -r SM{CAT}".format(CAT=category))
os.system("rm cgs.* unc.*")

os.chdir(base_directory)
os.system("mkdir mutau")
for category in [0,1,2] :
    os.chdir(base_directory+'/mutau')
    os.system("datacard-project.py -c mt -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/mutau/SM{CAT}".format(CAT=category))
    os.system("mv mt.inputs-sm.root htt_mt.input.root")
    if options.SM4 :
        ## all cross section will be rescaled in one go
        os.system(r"root -q -l -b {CMSSW_BASE}/src/HiggsAnalysis/HiggsToTauTau/macros/rescale2SM4.C+\(true,\"htt_mt.input.root\"\)".format(CMSSW_BASE=os.environ['CMSSW_BASE']))
    for mass in masses :
        os.system("create-datacard.py -i htt_mt.input.root -o htt_mt_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))
    ## cleanup
    os.chdir(base_directory+'/mutau')
    os.system("cp SM{CAT}/*.* .".format(CAT=category))
    os.system("rm -r SM{CAT}".format(CAT=category))
os.system("rm cgs.* unc.*")
