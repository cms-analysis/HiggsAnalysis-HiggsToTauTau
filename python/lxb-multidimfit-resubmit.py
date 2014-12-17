#!/usr/bin/env python

from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to resubmit jobs for multidim-fits that have not made it through the farm. On successful completion a multidim-fit job wil write a file .done_{IDX} into its output directory, where {IDX} corresponds to the index of the job. The script will search for this output and if found will comment the line with the lxb submission command from the submission script. It will then issue a summary message on how many jobs did not succeed and allow to re-execute the modified submission script, leaving all jobs, that have not finished successfully uncommented. ARG corresponds to any of the old submission folders. The absolute path to the directory, where all mass directories are located, which containt the jobs of the last submission should have written their output to, should be given by option -o (--output).")
parser.add_option("-o", "--output", dest="output", default="", type="string",
                  help="Output directory, where to find the output of the last  submission. [Default: \"\"]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="increase verbosity. [Default: False]")
parser.add_option("-m", "--mass", dest="mass", default="", type="string",
		  help="Option for choosing explicit masses, for which the scripts should be resubmitted. Format: separate the masses through commata.")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()

import os

directoryList = os.listdir("{PATH}".format(PATH=options.output))
massarray = options.mass.replace(" ","").split(",")
for dir in directoryList :
    if "common" in dir:
        continue
    if ("" not in massarray) and (dir not in massarray):
	continue
    ## open submission script and go through it line by line (line corresponds to idx-1, starting from 0)
    ijob=0
    done=0
    print args[0].rstrip(args[0].rsplit("-")[-1])+dir
    source = open(args[0].rstrip(args[0].rsplit("-")[-1])+dir+"/"+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"_submit.sh",'r')
    target = open(args[0].rstrip(args[0].rsplit("-")[-1])+dir+"/"+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"_resubmit.sh", 'w')
    
    for line in source:
        if os.path.exists("{PATH}/{DIR}/.done_{IDX}".format(PATH=options.output, DIR=dir, IDX=ijob)) :
            if "export" in line:
                continue
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
    print " Successfull jobs have been commented from submission script."
    print " Starting resubmission! "
    #print " ./", args[0].rstrip(args[0].rsplit("-")[-1])+dir+"_resubmit.sh"
    print "-----------------------------------------------------------------------"
    os.system("chmod a+x "+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"/"+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"_resubmit.sh")
    os.system("./"+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"/"+args[0].rstrip(args[0].rsplit("-")[-1])+dir+"_resubmit.sh")
