#!/usr/bin/env python

from optparse import OptionParser
from HiggsAnalysis.HiggsToTauTau.horizontal_morphing import Morph

parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="This is a script to apply horizontal template morphing to estimate masses, which have not been simulated. ARG corresponds to the input file that contains the signal samples given by the option --samples for the simulated (pivotal) masses that are given by the options --masses. The samples should include a key word {MASS}, that will be replaced by the masses given by option --masses. Defaults are given for the e-mu case.")
parser.add_option("--categories", dest="categories", default="emu_vbf,emu_boost_low,emu_boost_high", type="string",
                  help="List of event categories to be morphed; can be given as comma separated list of strings with an aritary number of whitespaces. [Default: 'emu_vbf,emu_boost_low,emu_boost_high']")
parser.add_option("--samples", dest="samples", default="ggH{MASS},qqH{MASS},VH{MASS}", type="string",
                  help="List of signal samples to be morphed; can be given as comma separated list of strings with an aritary number of whitespaces. The sample name is expected to include the key word {MASS}, that will be replaced by the masses given by option --masses. [Default: 'ggH{MASS},qqH{MASS},VH{MASS}']")
parser.add_option("--uncerts", dest="uncerts", default="CMS_scale_e_7TeV", type="string",
                  help="List of uncertainties to be considered for morphing; can be given as comma separated list of strings with an aribtary number of whitespaces. The sample name will be completed in the form: {SAMPLE}_{UNCERT}Up/Down. [Default: 'CMS_scale_e_7TeV']")
parser.add_option("--masses", dest="masses", default="110,115,120,125,130,135,140,145", type="string",
                  help="List pivotal mass points for morphing; can be given as comma separated list of strings with an aribtary number of whitespaces. [Default: '110,115,120,125,130,135,140,145']")
parser.add_option("--step-size", dest="step_size", default="1", type="string",
                  help="Step-size for morphing of the masses, in GeV. [Default: 1]")
parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                  help="Run in verbose mode")
parser.add_option("--extrapolate", dest="extrapolate", default="", type="string",
                  help="A comma separated list of masses outside the pivot range to extrapolate to. The distributions will be taken from the endpoints of the pivotal masses, the efficiency will be extrapolated. WARNING: this method is less robust than the interpolation. [Default: '']")
parser.add_option("--trivial", dest="trivial", default=False, action="store_true",
                  help="Apply trivial morphing, i.e. the templates closest to the given mass points will be copied to the corresponding mass point. The normalization will be determined by interpolation/extrapolation from the pivotal masses. [Default: False]")
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if not len(args) == 1 :
    parser.print_usage()
    exit(1)

template_morphing = Morph(args[0],options.categories,options.samples,options.uncerts,options.masses,options.step_size,options.verbose,options.extrapolate,options.trivial)
template_morphing.run()
