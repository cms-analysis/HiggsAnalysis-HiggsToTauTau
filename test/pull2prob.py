from optparse import OptionParser, OptionGroup

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Script to determine a goodness of fit assessment from the pulls in mlfit.txt file only. ARG corresponds to the full path in the file.")
## direct options
parser.add_option("--model", dest="model", default="s+b",  type="choice", choices=['b', 's+b'],
                  help="Choose the model that you would like to test. Choose between 'b' and 's+b'. [Default: 's+b']")
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
from scipy import stats

model = 0 if options.model == 'b' else 1

chi2 = 0; ndof = 0
file = open(args[0], 'r')
pattern = re.compile('[+-]\d+\.\d+(?=sig)')
for line in file :
    pulls  = pattern.findall(line)
    if pulls :
        chi2+=float(pulls[model])*float(pulls[model])
        ndof+=1
file.close()

if ndof>0 :
    print "---------------------------------------------------------------------------"
    print "file:", args[0]
    print 
    print "chi2       =", chi2
    print "ndof       =", (ndof-1)
    print "chi2/ndof  =", chi2/(ndof-1)
    print "prob(chi2) =", (1-stats.chi2.cdf(chi2/(ndof-1), 1))
    print "---------------------------------------------------------------------------"
