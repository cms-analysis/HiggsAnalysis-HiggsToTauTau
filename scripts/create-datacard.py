#!/usr/bin/env python
from optparse import OptionParser

## set up the option parser
parser = OptionParser(
    usage="usage: %prog [options] ARG",
    description="Script to create a datacard from a set of configuration files. ARG corresponds to the mass, for which the datacard should be produced. ARG can be omitted if there is no dedicated dependency of the datacard on the mass of the object like for the Ztt measurement. More information can be found in the README file of the setup directory in this paclage. "
    )
parser.add_option("-i", "--input_file", dest="input_file", default="", type="string", help="Input root file [Default: \"\"]")
parser.add_option("-u", "--unc_vals", dest="unc_vals", default="unc.vals", type="string", help="Formatted file with uncertainty values [Default: unc.vals]")
parser.add_option("-c", "--cgs_defs", dest="cgs_defs", default="cgs.conf", type="string", help="Group, sample, category listings [Default: cgs.config]")
parser.add_option("-d", "--unc_defs", dest="unc_defs", default="unc.conf", type="string", help="All uncertainty parameters listed [Default: unc.config]")
parser.add_option("-o", "--output_file", dest="out_file", default="datacard.txt", type="string", help="Output name of the datacard [Default: datacard.txt]")
parser.add_option("--categories", dest="categories", type="string", help="If specified, only build the specified categories")
(options,args)=parser.parse_args()

masspoint=0
if len(args) < 1 :
    print "Warning: ARG has been omitted. Datacards will not be produced for a certain mass point."
else :
    masspoint=args[0]

desired_categories = None
if options.categories is not None:
    desired_categories = options.categories.split(',')

from HiggsAnalysis.HiggsToTauTau.MakerUtilsL import DBuilder
dmaker = DBuilder(
    uncertainty_file=options.unc_vals,
    out_file=options.out_file,
    root_file=options.input_file,
    unc_defs=options.unc_defs,
    cgs_defs=options.cgs_defs,
    mass_point=masspoint,
    categories=desired_categories
    )
dmaker.run()

