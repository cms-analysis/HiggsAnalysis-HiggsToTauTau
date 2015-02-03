#!/usr/bin/env python

import os
import glob
import re

#need directory and datacard also for 130
os.system("mkdir LIMITS")
os.system("mkdir LIMITS/common")
os.system("cp HplusNuisanceFile.dat LIMITS/common")
os.system("cp combine_datacard_hplushadronic_m120.txt combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/CMS_ttHpW_signal120/CMS_ttHpW_signal130/g combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/CMS_ttHpHp_signal120/CMS_ttHpHp_signal130/g combine_datacard_hplushadronic_m130.txt")
for file in glob.glob("*.txt") :
    print file
    os.system("cp {FILE} htaunu_had_00_8TeV.txt".format(FILE=file))
    mass_match = re.compile("combine_datacard_hplushadronic_m(?P<MASS>[0-9]*\.?[0-9]*).txt?")
    mass_label  = mass_match.match(file).group('MASS')
    os.system("mkdir LIMITS/{MASS}".format(MASS=mass_label))    
    os.system("sed -i s/CMS_ttHpHp_signal{MASS}_statBin/CMS_ttHpHp_signal_statBin/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpW_signal{MASS}_statBin/CMS_ttHpW_signal_statBin/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpHp_signal{MASS}/CMS_ttHpHp_signal/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/CMS_ttHpW_signal{MASS}/CMS_ttHpW_signal/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/combine_histograms_hplushadronic_m{MASS}.root/combine_histograms_hplushadronic_light.root/g htaunu_had_00_8TeV.txt".format(MASS=mass_label))
    os.system("sed -i s/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC'/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC\\nshapes CMS_ttHpHp_signal \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC\\nshapes CMS_ttHpW_signal \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC'/g htaunu_had_00_8TeV.txt")
    os.system("mv htaunu_had_00_8TeV.txt LIMITS/{MASS}".format(MASS=mass_label))
    os.system("cp combine_histograms_hplushadronic_light.root LIMITS/{MASS}".format(MASS=mass_label))
    
    
    
    
