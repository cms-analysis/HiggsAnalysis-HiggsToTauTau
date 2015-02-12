#!/usr/bin/env python
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to fix the BR problems of the lowmH and tauphobic scenario. ARG corresponds to the file that is to be sculpted. Per default a new file with postfix *_sculpted will be createpick up the mA/tanb datacards from Hplus and Htt, combine them, transfer them to a workspace and put them into a common datacard structure.")
parser.add_option("--path-htt", dest="path_htt", default= "", type="string",
                  help="Path to htt datacards. [Default: \"\"]")
parser.add_option("--path-hplus", dest="path_hplus", default="", type="string",
                  help="Path to hplus datacards. [Default: \"\"]")
parser.add_option("--path-Hhh", dest="path_Hhh", default="", type="string",
                  help="Path to Hhh datacards. [Default: \"\"]")
parser.add_option("--path-AZh", dest="path_AZh", default="", type="string",
                  help="Path to hplus datacards. [Default: \"\"]")
parser.add_option("--label", dest="label", default="", type="string",
                  help="Path to AZh datacards. [Default: \"\"]")
parser.add_option("--MSSMvsSM", dest="MSSMvsSM", default=False, action="store_true",
                  help="This is needed for the signal hypothesis separation test MSSM vs SM [Default: False]")
parser.add_option("--model", dest="model", default="mhmodp", type="string",
                       help="The model which should be used (choices are: mhmax-mu+200, mhmodp, mhmodm, lowmH, tauphobic, lightstau1, lightstopmod, low-tb-high, 2HDM_ty1_mA300_mH300, 2HDM_ty2_mA300_mH300). Default: \"mhmdop\"]")
# check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 0 :
    parser.print_usage()
    exit(1)

import os
import glob
import re

#build limit structure
if os.path.exists("LIMITS{LABEL}-BSMCombination".format(LABEL="" if options.label=="" else "-"+options.label)) :
    os.system("rm -r LIMITS{LABEL}-BSMCombination".format(LABEL="" if options.label=="" else "-"+options.label))
os.system("mkdir LIMITS{LABEL}-BSMCombination".format(LABEL="" if options.label=="" else "-"+options.label))
if options.path_htt != "" :
    os.system("cp -r {HTT}/common LIMITS{LABEL}-BSMCombination/".format(HTT=options.path_htt, LABEL="" if options.label=="" else "-"+options.label))
if options.path_Hhh != "" :
    if os.path.exists("LIMITS{LABEL}-BSMCombination/common".format(LABEL="" if options.label=="" else "-"+options.label)) :
        os.system("cp -r {Hhh}/common/* LIMITS{LABEL}-BSMCombination/common".format(Hhh=options.path_Hhh, LABEL="" if options.label=="" else "-"+options.label))
    else :
        os.system("cp -r {Hhh}/common LIMITS{LABEL}-BSMCombination/".format(Hhh=options.path_Hhh, LABEL="" if options.label=="" else "-"+options.label))
if options.path_AZh != "" :
    if os.path.exists("LIMITS{LABEL}-BSMCombination/common".format(LABEL="" if options.label=="" else "-"+options.label)) :
        os.system("cp -r {AZh}/common/* LIMITS{LABEL}-BSMCombination/common".format(AZh=options.path_AZh, LABEL="" if options.label=="" else "-"+options.label))
    else :
        os.system("cp -r {AZh}/common LIMITS{LABEL}-BSMCombination/".format(AZh=options.path_AZh, LABEL="" if options.label=="" else "-"+options.label))
if options.path_hplus != "" :
    if os.path.exists("LIMITS{LABEL}-BSMCombination/common".format(LABEL="" if options.label=="" else "-"+options.label)) :
        os.system("cp -r {HPLUS}/common/* LIMITS{LABEL}-BSMCombination/common".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label))
    else :
        os.system("cp -r {HPLUS}/common LIMITS{LABEL}-BSMCombination/".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label))



#####################################################
### lowmH
if options.model=="lowmH" :
    print "model", options.model
    for mass in range(300, 3101, 100) :
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_htt != "" :
            for file in glob.glob("{HTT}/{MASS}/debug/*0.txt".format(HTT=options.path_htt, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="htt_"+str(tanb)+".txt"))
        if options.path_hplus != "" :
            for file in glob.glob("{HPLUS}/{MASS}/debug/*0.txt".format(HPLUS=options.path_hplus, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="hplus_"+str(tanb)+".txt"))
                os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root_{MASS}_{TANB} LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb[:-1])))
                os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_Hhh != "" :
            for file in glob.glob("{Hhh}/{MASS}/debug/*0.txt".format(Hhh=options.path_Hhh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="Hhh_"+str(tanb)+".txt"))
        if options.path_AZh != "" :
            for file in glob.glob("{AZh}/{MASS}/debug/*0.txt".format(AZh=options.path_AZh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="AZh_"+str(tanb)+".txt"))
    ##combine cards
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        for file in glob.glob("LIMITS{LABEL}-BSMCombination/{MASS}/*0.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass))) :
            print "combining cards"
            tanbs=file.rstrip(".txt").split("_")
            tanb=tanbs[1]
            os.system("combineCards.py -S LIMITS{LABEL}-BSMCombination/{MASS}/*_{TANB}.txt > LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
    ##text2workspace either MSSMvsBG or MSSMvsSM
            print "txt2workspace"
            if options.MSSMvsSM :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -P HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:twoHypothesisHiggs -o LIMITS{LABEL}-BSMCombination/{MASS}/fixedMu_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            else :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -o LIMITS{LABEL}-BSMCombination/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            os.system("mv LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))


#####################################################
### 2HDM
elif "2HDM" in options.model :
    print "model", options.model
    for mass in range(-1.0, 1.01, 0.1) :
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_htt != "" :
            for file in glob.glob("{HTT}/{MASS}/debug/*0.txt".format(HTT=options.path_htt, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="htt_"+str(tanb)+".txt"))
        if options.path_hplus != "" :
            for file in glob.glob("{HPLUS}/{MASS}/debug/*0.txt".format(HPLUS=options.path_hplus, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="hplus_"+str(tanb)+".txt"))
                os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root_{MASS}_{TANB} LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb[:-1])))
                os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_Hhh != "" :
            for file in glob.glob("{Hhh}/{MASS}/debug/*0.txt".format(Hhh=options.path_Hhh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="Hhh_"+str(tanb)+".txt"))
        if options.path_AZh != "" :
            for file in glob.glob("{AZh}/{MASS}/debug/*0.txt".format(AZh=options.path_AZh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="AZh_"+str(tanb)+".txt"))
    ##combine cards
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        for file in glob.glob("LIMITS{LABEL}-BSMCombination/{MASS}/*0.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass))) :
            print "combining cards"
            tanbs=file.rstrip(".txt").split("_")
            tanb=tanbs[1]
            os.system("combineCards.py -S LIMITS{LABEL}-BSMCombination/{MASS}/*_{TANB}.txt > LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
    ##text2workspace either MSSMvsBG or MSSMvsSM
            print "txt2workspace"
            if options.MSSMvsSM :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -P HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:twoHypothesisHiggs -o LIMITS{LABEL}-BSMCombination/{MASS}/fixedMu_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            else :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -o LIMITS{LABEL}-BSMCombination/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            os.system("mv LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))


#####################################################
### low-tb-high
elif options.model=="low-tb-high" :
    print "model", options.model
    for mass in (160, 180, 200, 250, 300, 350, 400, 450, 500) :
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_htt != "" :
            for file in glob.glob("{HTT}/{MASS}/debug/*0.txt".format(HTT=options.path_htt, MASS=str(mass))) :
                print file
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="htt_"+str(tanb)+".txt"))
        if options.path_hplus != "" :
            for file in glob.glob("{HPLUS}/{MASS}/debug/*0.txt".format(HPLUS=options.path_hplus, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]                
                if mass < 141 and tanb < 10 :
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="hplus_"+str(tanb)+".txt"))
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root_{MASS}_{TANB} LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb[:-1])))
                    
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_Hhh != "" :
            for file in glob.glob("{Hhh}/{MASS}/debug/*0.txt".format(Hhh=options.path_Hhh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                if mass < 351 and mass > 249 :                
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="Hhh_"+str(tanb)+".txt"))
        if options.path_AZh != "" :
            for file in glob.glob("{AZh}/{MASS}/debug/*0.txt".format(AZh=options.path_AZh, MASS=str(mass))) :
                print file
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                if mass < 351 and mass > 219 :    
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="AZh_"+str(tanb)+".txt"))             
    ##combine cards
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        for file in glob.glob("LIMITS{LABEL}-BSMCombination/{MASS}/*0.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass))) :
            print "combining cards"
            tanbs=file.rstrip(".txt").split("_")
            tanb=tanbs[1]
            os.system("combineCards.py -S LIMITS{LABEL}-BSMCombination/{MASS}/*_{TANB}.txt > LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
    ##text2workspace either MSSMvsBG or MSSMvsSM
            print "txt2workspace"
            if options.MSSMvsSM :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -P HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:twoHypothesisHiggs -o LIMITS{LABEL}-BSMCombination/{MASS}/fixedMu_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            else :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -o LIMITS{LABEL}-BSMCombination/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            os.system("mv LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))


#####################################################
### mhmax, mhmod, lightstau1, lightstopmod, tauphobic
else :
    print "model", options.model
    #for mass in (90, 100, 120, 130, 140, 160, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000) :
    for mass in (130, 140, 350) :    
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_htt != "" :
            for file in glob.glob("{HTT}/{MASS}/debug/*0.txt".format(HTT=options.path_htt, MASS=str(mass))) :
                print file
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="htt_"+str(tanb)+".txt"))
        if options.path_hplus != "" :
            for file in glob.glob("{HPLUS}/{MASS}/debug/*0.txt".format(HPLUS=options.path_hplus, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]                
                if mass < 141 and float(tanb) < 10 :
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="hplus_"+str(tanb)+".txt"))
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root_{MASS}_{TANB} LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb[:-1])))
                    
                    os.system("cp {HPLUS}/{MASS}/combine_histograms_hplushadronic_light.root LIMITS{LABEL}-BSMCombination/{MASS}".format(HPLUS=options.path_hplus, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        if options.path_Hhh != "" :
            for file in glob.glob("{Hhh}/{MASS}/debug/*0.txt".format(Hhh=options.path_Hhh, MASS=str(mass))) :
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                if mass < 351 and mass > 249 :                
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="Hhh_"+str(tanb)+".txt"))
        if options.path_AZh != "" :
            for file in glob.glob("{AZh}/{MASS}/debug/*0.txt".format(AZh=options.path_AZh, MASS=str(mass))) :
                print file
                tanbs=file.rstrip(".txt").split("_")
                tanb=tanbs[1]
                if mass < 351 and mass > 219 :    
                    os.system("cp {FILE} LIMITS{LABEL}-BSMCombination/{MASS}/{NEWNAME}".format(FILE=file, LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), NEWNAME="AZh_"+str(tanb)+".txt"))             
    ##combine cards
        os.system("mkdir LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass)))
        for file in glob.glob("LIMITS{LABEL}-BSMCombination/{MASS}/*0.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass))) :
            print "combining cards"
            tanbs=file.rstrip(".txt").split("_")
            tanb=tanbs[1]
            os.system("combineCards.py -S LIMITS{LABEL}-BSMCombination/{MASS}/*_{TANB}.txt > LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
    ##text2workspace either MSSMvsBG or MSSMvsSM
            print "txt2workspace"
            if options.MSSMvsSM :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -P HiggsAnalysis.HiggsToTauTau.PhysicsBSMModel:twoHypothesisHiggs -o LIMITS{LABEL}-BSMCombination/{MASS}/fixedMu_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            else :
                os.system("text2workspace.py -m {MASS} LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt -o LIMITS{LABEL}-BSMCombination/{MASS}/batch_{TANB}.root".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))
            os.system("mv LIMITS{LABEL}-BSMCombination/{MASS}/tmp_{TANB}.txt LIMITS{LABEL}-BSMCombination/{MASS}/debug".format(LABEL="" if options.label=="" else "-"+options.label, MASS=str(mass), TANB=str(tanb)))




    
