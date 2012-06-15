import os
# Runs the macros produced by the produce_macros script. Macros produce PDF and PNG outputs
# macros in norm_list can be run with two boolean arguments:
# The first boolean represents whether the fit weights should be applied (yes)
# The second boolean represents whether the y-axis should be log-scale (we want both plots, so in norm-list, we set the axis-scale to normal)

macro_list = ["etauAfterFit_b","etauAfterFit_nob","etauAfterFit_vbf","etauAfterFit_boost","etauAfterFit_novbf","emuAfterFit_b","emuAfterFit_nob","emuAfterFit_vbf","emuAfterFit_boost","emuAfterFit_novbf","mutauAfterFit_b","mutauAfterFit_nob","mutauAfterFit_vbf","mutauAfterFit_boost","mutauAfterFit_novbf"]
norm_list = ["etauAfterFit_nob","etauAfterFit_novbf","mutauAfterFit_nob","mutauAfterFit_novbf","emuAfterFit_nob","emuAfterFit_novbf"]

for macro in macro_list:
    bash_script = '''root -l -b -q %s.C++\(\)''' % macro
    os.system(bash_script)

for macro in macro_list:
    bash_script = '''root -l -b -q %s.C++\(\"false\"\)''' % macro
    os.system(bash_script)

for nmacro in norm_list:
    bash_script = '''root -l -b -q %s.C++\(\"true\",\"false\"\)''' % nmacro
    os.system(bash_script)

for nmacro in norm_list:
    bash_script = '''root -l -b -q %s.C++\(\"false\",\"false\"\)''' % nmacro
    os.system(bash_script)

