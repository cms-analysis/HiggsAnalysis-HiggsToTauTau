#!/usr/bin/env python
import os
from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options]", description="Script to kill all lxb jos")
#parser.add_option("-u", "--user", dest="user", default="", type="string",
#                  help="Name of the lxq user!")
#parser.add_option("-j", "--job", dest="job", default="", type="string",
#                  help="Name of the job you want to delete!")

## check number of arguments; in case print usage
(options, args) = parser.parse_args()

#if len(args) < 1 :
#    parser.print_usage()
#    exit(1)


os.system("bjobs > tmp.log")
input_file = open("tmp.log",'r')
for line in input_file :
    words = line.split()
    if words[0].isdigit() :# and words[2].find("{JOB}".format(JOB=options.job))>-1 :
        os.system("bkill {JOBID}".format(JOBID=words[0]))
input_file.close()
print "done"
