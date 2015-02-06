#!/usr/bin/env python

import os
import glob
import re
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]",
                      description="Script to create a LIMITS dir structure for the Hplus datacards.")
parser.add_option("--model", dest="model", default="mhmodp", type="string",
                  help="The model which should be used (choices are: mhmax-mu+200, mhmodp, mhmodm, lowmH, tauphobic, lightstau1, lightstopmod, low-tb-high, 2HDM_ty1_mA300_mH300, 2HDM_ty2_mA300_mH300). Default: \"mhmdop\"]")
# check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) != 0 :
    parser.print_usage()
    exit(1)


#need directory and datacard also for 130
os.system("mkdir LIMITS")
os.system("mkdir LIMITS/bbb/")
os.system("mkdir LIMITS/bbb/common")
os.system("cp HplusNuisanceFile.dat LIMITS/bbb/common")
os.system("cp combine_datacard_hplushadronic_m120.txt combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/CMS_ttHpW_signal120/CMS_ttHpW_signal130/g combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/CMS_ttHpHp_signal120/CMS_ttHpHp_signal130/g combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/combine_histograms_hplushadronic_m120.root/combine_histograms_hplushadronic_m130.root/g combine_datacard_hplushadronic_m130.txt")
for file in glob.glob("*.txt") :
    print file
    os.system("cp {FILE} htaunu_had_00_8TeV.txt".format(FILE=file))
    mass_match = re.compile("combine_datacard_hplushadronic_m(?P<MASS>[0-9]*\.?[0-9]*).txt?")
    mass_label  = mass_match.match(file).group('MASS')  
    os.system("sed -i s/CMS_ttHpHp_signal{MASS}_statBin/CMS_ttHpHp_signal_statBin/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpW_signal{MASS}_statBin/CMS_ttHpW_signal_statBin/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpHp_signal{MASS}/CMS_ttHpHp_signal/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpW_signal{MASS}/CMS_ttHpW_signal/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/combine_histograms_hplushadronic_m{MASS}.root/combine_histograms_hplushadronic_light.root/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC'/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC\\nshapes CMS_ttHpHp_signal \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC\\nshapes CMS_ttHpW_signal \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC'/g htaunu_had_00_8TeV.txt")
    if options.model=="lowmH":
        continue
    elif "2HDM" in options.model:
        continue
    else :
        os.system("mkdir LIMITS/bbb/{MASS}".format(MASS=mass_label))  
        os.system("mv htaunu_had_00_8TeV.txt LIMITS/bbb/{MASS}".format(MASS=mass_label))
        os.system("cp combine_histograms_hplushadronic_light.root LIMITS/bbb/{MASS}".format(MASS=mass_label))
    
    
if options.model=="lowmH":  
    for mu in (300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100) :
        os.system("mkdir LIMITS/bbb/{MU}".format(MU=mu))    
        os.system("cp combine_histograms_hplushadronic_light.root LIMITS/bbb/{MU}".format(MU=mu))
        os.system("cp htaunu_had_00_8TeV.txt LIMITS/bbb/{MU}/htaunu_had_00_8TeV.txt".format(MU=mu))
    os.system("rm htaunu_had_00_8TeV.txt")

if "2HDM" in options.model:
    for mu in range(-100, 101, 10) :
        os.system("mkdir LIMITS/bbb/{MU}".format(MU=float(mu)/100))    
        os.system("cp combine_histograms_hplushadronic_light.root LIMITS/bbb/{MU}".format(MU=float(mu)/100))
        os.system("cp htaunu_had_00_8TeV.txt LIMITS/bbb/{MU}/htaunu_had_00_8TeV.txt".format(MU=float(mu)/100))
    os.system("rm htaunu_had_00_8TeV.txt")
