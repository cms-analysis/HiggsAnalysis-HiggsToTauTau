#!/usr/bin/env python

from optparse import OptionParser
       
parser = OptionParser(usage="usage: %prog [options] datacatd.txt",
                      description="script to prepare datacards from inputfiles and to copy them to cvs.")
(options, args) = parser.parse_args()

import os

base_directory = os.getcwd()
masses = [110,111,112,113,114,115,116,117,118,119,
          120,121,122,123,124,125,126,127,128,129,
          130,131,132,133,134,135,136,137,138,139,
          140,141,142,143,144,145
          ]

os.chdir(base_directory)
os.system("mkdir emu")
for category in [0,1,2] : 
    os.chdir(base_directory+'/emu')
    os.system("datacard-project.py -c em -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/emu/SM{CAT}".format(CAT=category))
    #os.system("cp ../../htt_em.input.root .")
    for mass in masses :
        os.system("create-datacard.py -i htt_em.input.root -o htt_em_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))

os.chdir(base_directory)
os.system("mkdir etau")
for category in [0,1,2] : 
    os.chdir(base_directory+'/etau')
    os.system("datacard-project.py -c et -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/etau/SM{CAT}".format(CAT=category))
    #os.system("cp ../../htt_et.input.root .")
    for mass in masses :
        os.system("create-datacard.py -i htt_et.input.root -o htt_et_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))

os.chdir(base_directory)
os.system("mkdir mutau")
for category in [0,1,2] :
    os.chdir(base_directory+'/mutau')
    os.system("datacard-project.py -c mt -e SM-0{CAT} SM{CAT}".format(CAT=category))
    os.chdir(base_directory+"/mutau/SM{CAT}".format(CAT=category))
    #os.system("cp ../../htt_mt.input.root .")
    for mass in masses :
        os.system("create-datacard.py -i htt_mt.input.root -o htt_mt_{CAT}-{MASS}.txt {MASS}".format(CAT=category, MASS=mass))

