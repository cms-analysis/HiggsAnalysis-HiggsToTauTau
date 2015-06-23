#!/usr/bin/env python

from optparse import OptionParser, OptionGroup
parser = OptionParser(usage="usage: %prog [options] ARG1 ARG2 ARG3 ...", description="")
agroup = OptionGroup(parser,"MAIN OPTIONS", "")
agroup.add_option("--log-mass",dest="logMass", default=False, action="store_true", help="")
agroup.add_option("--model-file",dest="modelFile", default="$CMSSW_BASE/src/auxiliaries/models/out.mhmodp-8TeV-tanbHigh-nnlo.root", type="string", help="")
agroup.add_option("--model", dest="model", default="mhmodp", type="string", help="")
agroup.add_option("--mass-tolerance", dest="massTolerance", default=0.15, type="float", help="")
agroup.add_option("--reference-mass", dest="referenceMass", default="A", type="string", help="")
agroup.add_option("--higgs-contribution",dest="higgsContribution", default="hHA", type="string", help="")


(options, args) = parser.parse_args()

from array import array
import ROOT as r
import os
import numpy as np


lxq_fragment = '''#!/bin/zsh
export CMSSW_BASE=$cmssw_base
linux_ver=`lsb_release -s -r`
echo $linux_ver
if [[ $linux_ver < 6.0 ]];
then
     eval "`/afs/desy.de/common/etc/local/ini/ini.pl cmssw_cvmfs`"
     export SCRAM_ARCH=slc5_amd64_gcc472
else
     source /cvmfs/cms.cern.ch/cmsset_default.sh
     export SCRAM_ARCH=slc6_amd64_gcc472
fi
'''

masslist = []
truemasslist = []

if options.logMass: 
	masslist = np.array([4.5 + x*2.42/100 for x in range(101)], dtype='d')
	truemasslist = np.exp(masslist)

else :
	masslist = np.array([90+10*m for m in range(93)], dtype='d')
	truemasslist = masslist
os.system("mkdir -p $CMSSW_BASE/src/higgsContributions")
for i in range(len(masslist)-1):
	submit_name = "{dir}/higgsContributions/higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.mass{mass}.sh".format(dir=os.getcwd(), model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution, mass=truemasslist[i])
	with open(submit_name, 'w') as submit_script:
		os.system("export cmssw_base=$CMSSW_BASE")
		print "Generating submission script: {script}".format(script=submit_name)
		submit_script.write(lxq_fragment)
		submit_script.write("cd {dir}\n".format(dir=os.getcwd()))
		submit_script.write("eval `scram runtime -sh`\n")
		submit_script.write("python $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/scripts/higgsContributions.py {log} --mass={mass} --model={model} --model-file={file} --mass-tolerance={tolerance} --reference-mass={reference} --higgs-contribution={contr}".format(mass=masslist[i], model=options.model, file=options.modelFile, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution, log = "--log-mass" if options.logMass else ""))
		submit_script.close()
		os.system("chmod a+x {script}".format(script=submit_name))
		os.system("qsub -l h_vmem=2000M -l h_rt=00:30:00 -j y -o /dev/null -l distro=sld6 -v cmssw_base {script}".format(script=submit_name))

print "hadd $CMSSW_BASE/src/higgsContributions/higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.{log}root $CMSSW_BASE/src/higgsContributions/higgsContribution.model{model}.tolerance{tolerance}.reference{reference}.contr{contr}.mass*.{log}root".format(model=options.model, tolerance=options.massTolerance, reference=options.referenceMass, contr=options.higgsContribution, log="logMass." if options.logMass else "")
