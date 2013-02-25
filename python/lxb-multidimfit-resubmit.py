#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to resubmit jobs for multidim-fits that have not made it through the farm. On successful completion a multidim-fit job wil write a file .done_{IDX} into its output directory, where {IDX} corresponds to the index of the job. The script will search for this output and if found will comment the line with the lxb submission command from the submission script. It will then issue a summary message on how many jobs did not succeed and allow to re-execute the modified submission script, leaving all jobs, that have not finished successfully uncommented. ARG corresponds to the old submission shell script. The absolute path of the directory ,where the jobs of the last submission should have written their output to should be given by option -o (--output).")
parser.add_option("-o", "--output", dest="output", default="", type="string",
                  help="Output directory, where to find the output of the last  submission. [Default: \"\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="increase verbosity. [Default: False]")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

#backup = open("backup_file.sh", "w")
#for idx in range(0, 300) :
#    line = "bsub -q 8nh -oo /afs/cern.ch/work/r/rwolf/scratch/Moriond/CMSSW_5_2_5/src/log/cV-cF-cmb+-CV-CF-125_{IDX}.log /afs/cern.ch/work/r/rwolf/scratch/Moriond/CMSSW_5_2_5/src/cV-cF-cmb+-CV-CF-125/cV-cF-cmb+-CV-CF-125_{IDX}.sh\n".format(IDX=idx)
#    backup.write(line)
#backup.close()
#exit()

## open submission script and go through it line by line (line corresponds to idx-1, starting from 0)
ijob=0
done=0
source = open(args[0],'r')
target = open(args[0]+'_resubmit', 'w')
for line in source:
    if os.path.exists("{PATH}/.done_{IDX}".format(PATH=options.output, IDX=ijob)) :
        if not line.lstrip()[0] == "#" :
            line = "#"+line
            done+=1
    ijob+=1
    target.write(line)
source.close()
target.close()

print "-----------------------------------------------------------------------"
print " Summary of succeeded jobs: "
print " "
print " submitted jobs:" + str(ijob)
print " succeeded jobs:" + str(done)
print " "
print " Successfull jobs have been commented from submission script. Ready for"
print " resubmission: "
print " ./", args[0]+'_resubmit'
print "-----------------------------------------------------------------------"
## search output directory for .done_{IDX} if it exists comment the line with '#'

## 

#import re
#matcher = re.compile('v?htt_\w*.inputs-\w*-(?P<PERIOD>[0-9]*\w*)(-?_?\w*)*.root')
#ecms_str = matcher.match(filename).group('PERIOD')
#ecms_str = ecms_str[:ecms_str.find('TeV')]
#ecms = float(ecms_str)
