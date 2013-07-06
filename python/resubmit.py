import glob
import argparse

parser = argparse.ArgumentParser(description='This script is designed to build an resubmitscript for jobs run before. It checks for existing rootfiles with the label "-id_subid" in the output folder and addapts the submitscript accordingly. Please bear in mind ths script does not check whether the rootfiles are created correctly!')
parser.add_argument('--path', '-p', dest='path', default='LIMITS/cmb/', help='path to result files')
parser.add_argument('--submitfile', '-sf', dest='submitfile', help='path to submit files')
parser.add_argument('--sub-jobs', '-sj', dest='subjobs', type=int, default='8', help='number of subjobs')

options = parser.parse_args()

source = open(options.submitfile, 'r')
target = open(options.submitfile[:-3]+'_resubmit.sh', 'w')
linecount=0
jobid=0
subid=0
for line in source:
    subid = linecount%options.subjobs
    if subid == 0 and linecount != 0: jobid+=1 # jobid is increased if we are through all subid's and only if line is not zero 
    print glob.glob("%s/*/*-%s_%s*"%(options.path, str(jobid), str(subid)))
    if glob.glob("%s/*/*-%s_%s*"%(options.path, str(jobid), str(subid))) != []:
        if not line.lstrip()[0] == '#':
            line = '#'+line
    linecount+=1
    target.write(line)
source.close()
target.close()
