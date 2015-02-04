#!/usr/bin/env python

import os
import glob
import re

#need directory and datacard also for 130
os.system("mkdir LIMITS")
os.system("mkdir LIMITS/common")
os.system("cp HplusNuisanceFile.dat LIMITS/common")
os.system("cp combine_datacard_hplushadronic_m120.txt combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/HH120/HH130/g combine_datacard_hplushadronic_m130.txt")
os.system("sed -i s/HW120/HW130/g combine_datacard_hplushadronic_m130.txt")
for file in glob.glob("*.txt") :
    print file
    mass_match = re.compile("combine_datacard_hplushadronic_m(?P<MASS>[0-9]*\.?[0-9]*).txt?")
    mass_label  = mass_match.match(file).group('MASS')
    os.system("cp {FILE} htaunu_had_00_8TeV-{MASS}.txt".format(FILE=file, MASS=mass_label))
    os.system("sed -i s/lumi/lumi_8TeV/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/HH{MASS}_a_statBin/HH_statBin/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/HW{MASS}_a_statBin/HW_statBin/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/HH{MASS}/HH/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/HW{MASS}/HW/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/_a//g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    os.system("sed -i s/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC'/'shapes \* \* combine_histograms_hplushadronic_light.root \$PROCESS \$PROCESS_\$SYSTEMATIC\\nshapes HH \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC\\nshapes HW \* combine_histograms_hplushadronic_light.root \$PROCESS\$MASS \$PROCESS\$MASS_\$SYSTEMATIC'/g htaunu_had_00_8TeV-{MASS}.txt".format(MASS=mass_label))
    
    
for mu in (300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100) :
    os.system("mkdir LIMITS/{MU}".format(MU=mu))    
    os.system("cp combine_histograms_hplushadronic_light.root LIMITS/{MU}".format(MU=mu))
    os.system("cp htaunu_had_00_8TeV-100.txt LIMITS/{MU}/htaunu_had_00_8TeV.txt".format(MU=mu))
    
os.system("rm htaunu_had_00_8TeV-*.txt")
