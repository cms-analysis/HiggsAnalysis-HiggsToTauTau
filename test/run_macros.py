import os
# Runs the macros produced by the produce_macros script. Macros produce PDF and PNG outputs
# macros in norm_list can be run with two boolean arguments:
# The first boolean represents whether the fit weights should be applied (yes)
# The second boolean represents whether the y-axis should be log-scale (we want both plots, so in norm-list, we set the axis-scale to normal)

macro_list = ["etauAfterFit_b","etauAfterFit_nob","etauAfterFit_vbf","etauAfterFit_boost","etauAfterFit_novbf","emuAfterFit_b","emuAfterFit_nob","emuAfterFit_vbf","emuAfterFit_boost","emuAfterFit_novbf","mutauAfterFit_b","mutauAfterFit_nob","mutauAfterFit_vbf","mutauAfterFit_boost","mutauAfterFit_novbf"]
norm_list = ["etauAfterFit_nob","etauAfterFit_novbf","mutauAfterFit_nob","mutauAfterFit_novbf","emuAfterFit_nob","emuAfterFit_novbf"]

log = {
    ("em", "0") : "true",
    ("em", "1") : "true", 
    ("em", "2") : "false",
    ("em", "3") : "false",
    ("em", "5") : "false",
    ("mt", "0") : "true",
    ("mt", "1") : "true", 
    ("mt", "2") : "false",
    ("mt", "3") : "false",
    ("mt", "5") : "false",
    ("et", "0") : "true",
    ("et", "1") : "true", 
    ("et", "2") : "false",
    ("et", "3") : "false",
    ("et", "5") : "false",    
    }

max = {
    ("em", "0") : "2000",
    ("em", "1") :  "500", 
    ("em", "2") :   "50",
    ("em", "3") :   "15",
    ("em", "5") :  "0.7",
    ("mt", "0") : "2000",
    ("mt", "1") :  "500", 
    ("mt", "2") :  "200",
    ("mt", "3") :   "70",
    ("mt", "5") :    "3",
    ("et", "0") :  "100",
    ("et", "1") :   "20", 
    ("et", "2") :   "30",
    ("et", "3") :   "10",
    ("et", "5") :  "1.5",    
    }

min = {
    ("em", "0") : "0.1",
    ("em", "1") : "0.1", 
    ("em", "2") : "0",
    ("em", "3") : "0",
    ("em", "5") : "0",
    ("mt", "0") : "0.1",
    ("mt", "1") : "0.1", 
    ("mt", "2") : "0",
    ("mt", "3") : "0",
    ("mt", "5") : "0",
    ("et", "0") : "0.1",
    ("et", "1") : "0.1", 
    ("et", "2") : "0",
    ("et", "3") : "0",
    ("et", "5") : "0",    
    }

for chn in ["et", "mt", "em"] :
    for per in ["7TeV", "8TeV"] :
        for cat in ["0", "1", "2", "3", "5"] :
            for sca in ["true", "false"] :
                bash_script = "root -l -b -q htt_{CHN}_{CAT}_{PER}.C++\(\"{SCA}\",\"{LOG}\",{MIN},{MAX}\)".format(
                    SCA=sca, LOG=log[(chn,cat)],  MIN=min[(chn,cat)], MAX=max[(chn,cat)], CHN=chn, CAT=cat, PER=per)
                os.system(bash_script)

#for macro in macro_list:
#    bash_script = '''root -l -b -q %s.C++\(\"false\"\)''' % macro
#    os.system(bash_script)
#
#for nmacro in norm_list:
#    bash_script = '''root -l -b -q %s.C++\(\"true\",\"false\"\)''' % nmacro
#    os.system(bash_script)
#
#for nmacro in norm_list:
#    bash_script = '''root -l -b -q %s.C++\(\"false\",\"false\"\)''' % nmacro
#    os.system(bash_script)

