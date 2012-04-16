#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARGS",
                      description="Simple script to copy input files for limit and significance calculation from cvs to local. A list of arguments can be given. These arguments should be integers corresponding to the mass points for which you want to copy the datacards.")
parser.add_option("-i", "--input", dest="input", default="MitLimits/Higgs2Tau/data/emu/mssm", type="string", help="Input directory [Default: MitLimits/Higgs2Tau/data/emu/mssm]")
parser.add_option("-o", "--out", dest="out", default="mssm-emu", type="string", help="Name of the output directory [Default: mssm-emu]")
parser.add_option("-c", "--channel", dest="channel",   default="mssm-emu", type="choice", help="Channel to be copied [Default: emu]", choices=["mssm", "mssm-incl", "mssm-emu", "mssm-incl-emu", "mssm-etau", "mssm-incl-etau", "mssm-mutau", "mssm-incl-mutau", "mssm-mumu", "mssm-incl-mumu", "sm", "sm-incl", "sm-emu", "sm-incl-emu", "sm-etau", "sm-incl-etau", "sm-mutau", "sm-incl-mutau", "sm-mumu", "sm-incl-mumu", "sm-vbf", "sm-vbf-emu", "sm-vbf-etau", "sm-vbf-mutau", "sm-vbf-mumu", "sm-boost", "sm-boost-emu", "sm-boost-etau", "sm-boost-mutau", "sm-boost-mumu"])

## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

## admin of available masses per channel 
channel_to_mass = {}

## add mass point to the list of available masses per channel
def add_mass(channel, mass) :
    if not channel in channel_to_mass :
        channel_to_mass[channel] = "%s :  " % channel
    channel_to_mass[channel]+= "  %s  " % mass    

## add common directory for common input files
if not os.path.exists("{output}/common".format(output=options.out)) :            
    os.system("mkdir {output}/common".format(output=options.out))

if options.channel.find("mssm")>-1 :
    ## open masses.vals. Append if it exists already, create otherwise
    if os.path.exists("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out)) :
        masses = open("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out), 'a')
    else :
        masses = open("{pwd}/{output}/common/masses.vals".format(pwd=os.getcwd(), output=options.out), 'w')

    ## loop masses
    for mass in args :
        if not os.path.exists("{output}/{mass}".format(output=options.out, mass=mass)) :            
            os.system("mkdir {output}/{mass}".format(output=options.out, mass=mass))
        if options.channel == "mssm-emu" or options.channel == "mssm" :
            add_mass("htt_em_1", mass)
            os.system("cp {input}/eleMu_B_mA{mass}.txt {output}/{mass}/htt_em_1.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/emu-limit-inputs-V02-003.root/..\/common\/htt_em_1.input.root/g' {output}/{mass}/htt_em_1.txt".format(output=options.out, mass=mass))
            os.system("cp {input}/emu-limit-inputs-V02-003.root {output}/common/htt_em_1.input.root".format(input=options.input, output=options.out))
        if options.channel == "mssm-incl-emu" or options.channel == "mssm-emu" or options.channel == "mssm-incl" or options.channel == "mssm" :
            add_mass("htt_em_0", mass)
            os.system("cp {input}/eleMu_NoB_mA{mass}.txt {output}/{mass}/htt_em_0.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/emu-limit-inputs-V01-003.root/..\/common\/htt_em_0.input.root/g' {output}/{mass}/htt_em_0.txt".format(output=options.out, mass=mass))
            os.system("cp {input}/emu-limit-inputs-V01-003.root {output}/common/htt_em_0.input.root".format(input=options.input, output=options.out))
        if options.channel == "mssm-etau" or options.channel == "mssm" :
            add_mass("htt_et_1", mass)
            os.system("cp {input}/eleTau_B_mA{mass}.txt {output}/{mass}/htt_et_1.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/eleTau.root/..\/common\/htt_et.input.root/g' {output}/{mass}/htt_et_1.txt".format(output=options.out, mass=mass))
        if options.channel == "mssm-incl-etau" or options.channel == "mssm-etau" or options.channel == "mssm-incl" or options.channel == "mssm" :
            add_mass("htt_et_0", mass)
            os.system("cp {input}/eleTau_NoB_mA{mass}.txt {output}/{mass}/htt_et_0.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/eleTau.root/..\/common\/htt_et.input.root/g' {output}/{mass}/htt_et_0.txt".format(output=options.out, mass=mass))
            os.system("cp {input}/eleTau.root {output}/common/htt_et.input.root".format(input=options.input, output=options.out))        
        if options.channel == "mssm-mutau" or options.channel == "mssm" :
            add_mass("htt_mt_1", mass)
            os.system("cp {input}/muTau_B_mA{mass}.txt {output}/{mass}/htt_mt_1.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/muTau.root/..\/common\/htt_mt.input.root/g' {output}/{mass}/htt_mt_1.txt".format(output=options.out, mass=mass))    
        if options.channel == "mssm-incl-mutau" or options.channel == "mssm-mutau" or options.channel == "mssm-incl" or options.channel == "mssm" :
            add_mass("htt_mt_0", mass)
            os.system("cp {input}/muTau_NoB_mA{mass}.txt {output}/{mass}/htt_mt_0.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/muTau.root/..\/common\/htt_mt.input.root/g' {output}/{mass}/htt_mt_0.txt".format(output=options.out, mass=mass))        
            os.system("cp {input}/muTau.root {output}/common/htt_mt.input.root".format(input=options.input, output=options.out))        
        if options.channel == "mssm-mumu" or options.channel == "mssm" :
            add_mass("htt_mm_1", mass)
            os.system("cp {input}/muMu_B_mA{mass}.txt {output}/{mass}/htt_mm_1.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/muMu_B_mA{mass}.root/htt_mm_1.input.root/g' {output}/{mass}/htt_mm_1.txt".format(output=options.out, mass=mass)) 
            os.system("cp {input}/muMu_B_mA{mass}.root {output}/{mass}/htt_mm_1.input.root".format(input=options.input, output=options.out, mass=mass))
        if options.channel == "mssm-incl-mumu" or options.channel == "mssm-mumu" or options.channel == "mssm-incl" or options.channel == "mssm" :
            add_mass("htt_mm_0", mass)
            os.system("cp {input}/muMu_NoB_mA{mass}.txt {output}/{mass}/htt_mm_0.txt".format(input=options.input, output=options.out, mass=mass))
            os.system("perl -pi -e 's/muMu_NoB_mA{mass}.root/htt_mm_0.input.root/g' {output}/{mass}/htt_mm_0.txt".format(output=options.out, mass=mass)) 
            os.system("cp {input}/muMu_NoB_mA{mass}.root {output}/{mass}/htt_mm_0.input.root".format(input=options.input, output=options.out, mass=mass))
            ##
            ## to replace the upper block as soon as the new datacards structure for mumu is tested to work
            ##
            #add_mass("htt_mm_1", mass)
            #os.system("cp {input}/muMu_B_mA{mass}.txt {output}/{mass}/htt_mm_1.txt".format(input=options.input, output=options.out, mass=mass))
            #os.system("perl -pi -e 's/muMu_merged.root/..\/common\/htt_mm_1.input.root/g' {output}/{mass}/htt_mm_1.txt".format(output=options.out, mass=mass)) 
            #os.system("cp {input}/muMu_merged.root {output}/common/htt_mm_1.input.root".format(input=options.input, output=options.out, mass=mass))
            #add_mass("htt_mm_0", mass)
            #os.system("cp {input}/muMu_NoB_mA{mass}.txt {output}/{mass}/htt_mm_0.txt".format(input=options.input, output=options.out, mass=mass))
            #os.system("perl -pi -e 's/muMu_merged.root/..\/common\/htt_mm_0.input.root/g' {output}/{mass}/htt_mm_0.txt".format(output=options.out, mass=mass)) 
            #os.system("cp {input}/muMu_merged.root {output}/common/htt_mm_0.input.root".format(input=options.input, output=options.out, mass=mass))

    ## write channel-mass strings to masses.vals
    for channel in channel_to_mass :
        masses.write(channel_to_mass[channel]+"\n")
    masses.close()
    ## distribute file across all mass points
    #for mass in args : 
    #    os.system("cp {output}/common/masses.vals {output}/{mass}/".format(output=options.out, mass=mass))
else :
    ## loop masses
    for mass in args :
        if not os.path.exists("{output}/{mass}".format(output=options.out, mass=mass)) :            
            os.system("mkdir {output}/{mass}".format(output=options.out, mass=mass))
        if options.channel == "sm-emu" or options.channel == "sm" :
            os.system("cp {input}/htt_em_?-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_em.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
        if options.channel == "sm-etau" or options.channel == "sm" :
            os.system("cp {input}/htt_et_?-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_et.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-mutau" or options.channel == "sm" :
            os.system("cp {input}/htt_mt_?-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_mt.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-mumu" or options.channel == "sm" :
            os.system("cp {input}/muMu_SM?_mH{mass}.* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))

        if options.channel == "sm-vbf-emu" or options.channel == "sm-vbf" :
            os.system("cp {input}/htt_em_[02]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_em.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
        if options.channel == "sm-vbf-etau" or options.channel == "sm-vbf" :
            os.system("cp {input}/htt_et_[02]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_et.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-vbf-mutau" or options.channel == "sm-vbf" :
            os.system("cp {input}/htt_mt_[02]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_mt.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-vbf-mumu" or options.channel == "sm-vbf" :
            os.system("cp {input}/muMu_SM[02]_mH{mass}.* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
    
        if options.channel == "sm-boost-emu" or options.channel == "sm-boost" :
            os.system("cp {input}/htt_em_[01]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_em.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
        if options.channel == "sm-boost-etau" or options.channel == "sm-boost" :
            os.system("cp {input}/htt_et_[01]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_et.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-boost-mutau" or options.channel == "sm-boost" :
            os.system("cp {input}/htt_mt_[01]-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_mt.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-boost-mumu" or options.channel == "sm-boost" :
            os.system("cp {input}/muMu_SM[01]_mH{mass}.* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
    
        if options.channel == "sm-incl-emu" or options.channel == "sm-incl" :
            os.system("cp {input}/htt_em_0-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_em.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
        if options.channel == "sm-incl-etau" or options.channel == "sm-incl" :
            os.system("cp {input}/htt_et_0-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_et.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-incl-mutau" or options.channel == "sm-incl" :
            os.system("cp {input}/htt_mt_0-{mass}.txt {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))
            os.system("cp {input}/htt_mt.input.root {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))        
        if options.channel == "sm-incl-mumu" or options.channel == "sm-incl" :
            os.system("cp {input}/muMu_SM0_mH{mass}.* {output}/{mass}/".format(input=options.input, output=options.out, mass=mass))

