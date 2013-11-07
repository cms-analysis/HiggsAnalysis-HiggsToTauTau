from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import *

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Test...\n")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
model_opts = OptionGroup(parser, "MODEL OPTIONS", "These are the options that can be passed on to configure the creation of the model datacards.")
model_opts.add_option("--mA", dest="mA", default="", type="string",
                       help="The value of the free mass parameter in the model. Default: \"\"]")
model_opts.add_option("--tanb", dest="tanb", default="", type="string",
                       help="The value of tanb in the model. Default: \"\"]")
model_opts.add_option("--model", dest="modelname", default="mhmax-mu+200", type="string",
                       help="The model which should be used (choices are: mhmax-mu+200, mhmodp, mhmodm). Default: \"mhmax-mu+200\"]")
parser.add_option_group(model_opts)
morph_opts = OptionGroup(parser, "MORPHING OPTIONS", "With these options you can configure what kind of morphing should be applied for a given decay channel. Note that the same morphing mode is applied to all templates in a given input file.")
morph_opts.add_option("--morphing-htt_ee", dest="morphing_htt_ee", default="NEAREST_NEIGHBOUR", type="choice",
                 help="Choose the morphing type for the htt_ee decay channel. [Default: \"NEAREST_NEIGHBOUR\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
morph_opts.add_option("--morphing-htt_em", dest="morphing_htt_em", default="MORPHED", type="choice",
                 help="Choose the morphing type for the htt_em decay channel. [Default: \"MORPHED\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
morph_opts.add_option("--morphing-htt_mm", dest="morphing_htt_mm", default="NEAREST_NEIGHBOUR", type="choice",
                 help="Choose the morphing type for the htt_mm decay channel. [Default: \"NEAREST_NEIGHBOUR\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
morph_opts.add_option("--morphing-htt_mt", dest="morphing_htt_mt", default="MORPHED", type="choice",
                 help="Choose the morphing type for the htt_mt decay channel. [Default: \"MORPHED\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
morph_opts.add_option("--morphing-htt_et", dest="morphing_htt_et", default="MORPHED", type="choice",
                 help="Choose the morphing type for the htt_et decay channel. [Default: \"MORPHED\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
morph_opts.add_option("--morphing-htt_tt", dest="morphing_htt_tt", default="MORPHED", type="choice",
                 help="Choose the morphing type for the htt_tt decay channel. [Default: \"MORPHED\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
parser.add_option_group(morph_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from HiggsAnalysis.HiggsToTauTau.ModelDatacard import ModelDatacard
from HiggsAnalysis.HiggsToTauTau.ModelParams_BASE import ModelParams_BASE


class MODEL(object) :
    """
    This is a class to characterize a complete physics model with cross section and BR estimates for a required set of run
    periods in terms of center of mass energy, decay channels and production processes. Though it is not a strong requirement
    uncertainties should be available also for each of these configuring parameters. The model needs to be set up consistent
    to resemble the analysed set of datacards. 
    """
    def __init__(self, mass, tanb, modelpath='mhmax-mu+200', modeltype='mssm_xsec') :
        ## mass
        self.mass = mass
        ## tanb
        self.tanb = tanb
        ## model path (as defined in ModelParams_BASE)
        self.modelpath = modelpath
        ## model type (as defined in ModelParams_BASE)
        self.modeltype = modeltype
        ## central value of type {(period,decay,proc) : MODEL_PARAMS}
        self.central = {}
        ## shifts for uncertainties of type {'type' : {(period,decay,proc) : (MODEL_PARAMS,MODEL_PARAMS)}}
        self.uncerts = {}

    def missing_procs(self, decay, period, procs) :
        """
        Return a list of missing_procs in procs, which are still missing  in the model for given decay and period. Check
        centrals as it migth be some procs do not have uncertainties.
        """
        missing_procs = []
        for proc in procs :
            if not (period,decay,proc) in self.central.keys() :
                missing_procs.append(proc)
        return missing_procs
        
    def save_float_conversion(self, float_value) :
        """
        Convert a float into a string. Remove trailing .0's, which are not present for integer masses and would spoil the
        histogram search in the root input file.
        """
        value_str = str(float_value)
        if re.match('^\d*\.0$', value_str) :
            value_str = value_str[:value_str.rfind('.0')]
        return value_str

    def setup_model(self, period, decay, procs, shifts=[]) :
        """
        Setup the mdoel for given self.modelpath, self.modeltype, self.mass, self.tanb, period, procs and decay. In case that
        shifts is a non-emty list also shifts in mu or pdf are returned. Other shifts are currently not supported.
        """
        ## create model
        modelMaker = ModelParams_BASE(self.mass, self.tanb)
        modelMaker.setup_model(period, self.modelpath, self.modeltype)
        ## create central value
        for proc in procs :
            self.central[(period,decay,proc)] = modelMaker.create_model_params(period, proc, decay, '')
        ## create shifts
        for shift in shifts :
            buffer = {}
            for proc in procs :
                buffer[(period,decay,proc)] = (modelMaker.create_model_params(period, proc, decay, shift+'-'),
                                               modelMaker.create_model_params(period, proc, decay, shift+'+'))
            if shift in self.uncerts.keys() :
                self.uncerts[shift].update(buffer)
            else :
                self.uncerts[shift] = buffer
            
def main() :
    print "# --------------------------------------------------------------------------------------"
    print "# tangb_grid_new.py "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --tanb            :", options.tanb
    print "# --mA              :", options.mA
    print "# --morphing-htt_ee : ", options.morphing_htt_ee
    print "# --morphing-htt_em : ", options.morphing_htt_em
    print "# --morphing-htt_mm : ", options.morphing_htt_mm
    print "# --morphing-htt_mt : ", options.morphing_htt_mt
    print "# --morphing-htt_et : ", options.morphing_htt_et
    print "# --morphing-htt_tt : ", options.morphing_htt_tt
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"

    ## directory that contains all datacards in question
    path = args[0]
    label = '_{MASS}_{TANB}'.format(MASS=options.mA, TANB=options.tanb)
    ## mophing configuration
    morph = {
        'htt_ee' : options.morphing_htt_ee,
        'htt_em' : options.morphing_htt_em,
        'htt_mm' : options.morphing_htt_mm,
        'htt_mt' : options.morphing_htt_mt,
        'htt_et' : options.morphing_htt_et,
        'htt_tt' : options.morphing_htt_tt,
        }
    ## complete model for given mass and tanb value (including uncertainties)
    models = {}
    ## adaptor of the datacard for given mass and tanb value
    adaptor = ModelDatacard(options, label, False)
    adaptor.cleanup('.' if not path.find('/')>0 else path[:path.rfind('/')], label)
    ## parse datacard (first go)
    old_file = open(path, 'r')
    card = parseCard(old_file, options)
    old_file.close()
    
    ## determine MODEL for given datacard.
    model = MODEL(float(options.mA), float(options.tanb), options.modelname)
    match = re.compile('(?P<CHN>\w*)_\w*_[0-9]?_(?P<PER>[0-9]*\w*)')
    for bin in card.list_of_bins() :
        ## a bin can be made up of different decay channels or different run periods. Pick decay channel (chn) and run period
        ## (per) either from bin or from from datacards name in case it is not accessible from bin.
        if match.match(bin) :
            chn = match.match(bin).group('CHN')
            per = match.match(bin).group('PER')
        else :
            chn = match.match(path[path.rfind('/')+1:]).group('CHN')
            per = match.match(path[path.rfind('/')+1:]).group('PER')
        ## check which processes are still missing for given decay channel and run period
        missing_procs = model.missing_procs(chn, per, card.list_of_signals())
        if len(missing_procs)>0 :
            print "updating model to parameter set:", per, chn, missing_procs, ['mu', 'pdf']
            model.setup_model(per, chn, missing_procs, ['mu', 'pdf'])
    ## create new datacard
    new_name = path[:path.rfind('.txt')]+'_%.2f'%float(options.tanb)+'.txt'
    os.system("cp {SRC} {TARGET}".format(SRC=path, TARGET=new_name))
    ## adapt datacards
    adaptor.make_model_datacard(new_name, model, morph)

main()
exit(0)
