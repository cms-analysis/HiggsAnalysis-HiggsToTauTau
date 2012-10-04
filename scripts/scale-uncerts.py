#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] datacard1.txt datacard2.txt ...",
                      description="Script to rescale all uncertainties of type lnN in a given set of datacards by a scaling factor SCALE. The scaling factor SCALE can be changes via the option --scale. Old datacards will be overwritten.")
parser.add_option("-s", "--scale", dest="scale", default=1., type="float", help="Factor by which to scale all uncertainties of a given set of datacards. [Default: 1.]")
(options, args) = parser.parse_args()

if len(args) < 1 :
       parser.print_help()
       exit(1)

import os

scale = options.scale
for datacard in args :
    input_file = open(datacard,'r')
    output_file = open('tmp.txt', 'w')
    for input_line in input_file :
        words = input_line.split()
        output_line = input_line
        if len(words)>1 :
            ## scale shape uncertainties
            if words[1] == "shape" :
                for i in range(2,len(words)):
                    if '-' in words[i] :
                        continue
                    else :
                        words[i] = '%f' % (1./scale)
                output_line = '\t   '.join(words)+'\n'
            ## scale uncert's of type lnN
            if words[1] == "lnN" :
                for i in range(2,len(words)):
                    if '-' in words[i] :
                        continue
                    elif '/' in words[i] :
                        subwords = words[i].split('/')
                        words[i]='%f/%f' % ((float(subwords[0])-1.)/scale+1., (float(subwords[1])-1.)/scale+1.)
                    else :
                        words[i]='%f' % ((float(words[i])-1.)/scale+1.)
                output_line = '\t   '.join(words)+'\n'
        output_file.write(output_line)
    ##close files
    input_file.close()
    output_file.close()
    os.system("cp tmp.txt %s" % datacard)
    print " rescaled uncertainties in file %s" % datacard
print "done"
