#!/usr/bin/env python

from optparse import OptionParser

parser = OptionParser(usage="usage: %prog [options] ARGs",
                      description="This is a script to rescale uncertainties of type lnN or shape in all datacards pointed to by ARGs, by a scaling factor scale. This factor can be given via option --scale. Via the options --blacklist (--whitelist) sets of regular expressions corresponding to nuisance parameters can be passed that should not (exclusively) be scaled. Note that the original datacards will be overwritten.")
parser.add_option("--scale", dest="scale", default=1., type="float",
                  help="Factor by which to scale all uncertainties of a given set of datacards. Note: the nuisance parameters will be scaled by a factor 1/SCALE. [Default: 1.]")
parser.add_option("--blacklist", dest="blacklist", default="", type="string",
                  help="A list of regular python style expressions for nuisance parameters that should not be considered during the pruning decision. (You can add holy cows here.) The regular expressions should be embraced by quotation marks and separated by whitespace. [Default: \"\"]")
parser.add_option("--whitelist", dest="whitelist", default="", type="string",
                  help="A list of regular python style expressions that can be used to restrict the pruning to only those nuisance parameters that match these expressions. (You can e.g. restrict yourself only to bin-by-bin uncertainties.) The regular expressions should be embraced by quotation marks and separated by whitespace. [Default: \"\"]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
       parser.print_help()
       exit(1)

import os
import re

def remove_empty_strings(list) :
       """
       Remove emptry strings from list
       """
       indices = []
       for idx in range(len(list)) :
              if list[idx] == '' : indices.append(idx)
       for idx in indices :
              list.pop(idx)
       return list

def in_list(name, list) :
       """
       Return True if name does have a correspondence in the list of regular expressions of list and False else.
       Make sure that list does not contain empty strings. 
       """
       inList = False
       for unc in list :
              if re.search(unc, name) :
                     inList = True
       return inList

def main() :
    ## turn options.blacklist into a list
    blacklist = options.blacklist.split(' ')
    for idx in range(len(blacklist)) : blacklist[idx] = blacklist[idx].rstrip(',')
    blacklist = remove_empty_strings(blacklist)
    ## turn options.whitelist into a list
    whitelist = options.whitelist.split(' ')
    for idx in range(len(whitelist)) : whitelist[idx] = whitelist[idx].rstrip(',')
    whitelist = remove_empty_strings(whitelist)
    ## scale factor
    scale = options.scale
    for datacard in args :
           input_file = open(datacard,'r')
           output_file = open(datacard+'_tmp', 'w')
           for input_line in input_file :
                  words = input_line.split()
                  output_line = input_line
                  if len(words)>1 :
                         if not in_list(words[0], blacklist) :
                                if len(whitelist) == 0 or in_list(words[0], whitelist) :
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
           ## close files
           input_file.close()
           output_file.close()
           os.system("mv {CARD}_tmp {CARD}".format(CARD=datacard))
           print " rescaled uncertainties in file %s" % datacard
    print "done"

main()
