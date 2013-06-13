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
parser.add_option_group(model_opts)
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
    def __init__(self, mass, tanb, modelpath='mhmax-mu+200', modeltype='mssm_xsec') :
        ## mass
        self.mass = mass
        ## tanb
        self.tanb = tanb
        ## model path (as defined in ModelParams_BASE)
        self.modelpath = modelpath
        ## model type (as defined in ModelParams_BASE)
        self.modeltype = modeltype
        ## mapping common process names to toll specific names
        self.proc_map_mssm_xsec = {
        'ggH' : 'ggh',
        'bbH' : 'santander'       
        }
        ## central value of type {'proc' : MODEL_PARAMS}
        self.value = {}
        ## shifts of type {'type' : {'proc' : (MODEL_PARAMS,MODEL_PARAMS)}}
        self.shifts = {}

    def setup_model(self, period, decay, procs, shifts=[]) :
        """
        Setup the mdoel for given self.modelpath, self.modeltype, self.mass, self.tanb, period, procs and decay. In case that
        shifts is a non-emty list also shifts in mu or pdf are returned. Other shifts are currently not supported.
        """
        proc_map = {}
        if self.modeltype == 'mssm_xsec' :
            proc_map = self.proc_map_mssm_xsec
        ## create model
        modelMaker = ModelParams_BASE(self.mass, self.tanb)
        ## create central value
        for proc in procs :
            self.value[proc] = modelMaker.create_model_params(period, proc_map[proc], decay, 0, 0, self.modelpath, self.modeltype)
        ## create shifts
        for shift in shifts :
            buffer = {}
            for proc in procs :
                if shift == 'mu' :
                    buffer[proc] = (modelMaker.create_model_params(period, proc_map[proc], decay, -1, 0, self.modelpath, self.modeltype),
                                    modelMaker.create_model_params(period, proc_map[proc], decay, +1, 0, self.modelpath, self.modeltype))
                elif shift == 'pdf' :
                    buffer[proc] = (modelMaker.create_model_params(period, proc_map[proc], decay, 0, -1, self.modelpath, self.modeltype),
                                    modelMaker.create_model_params(period, proc_map[proc], decay, 0, +1, self.modelpath, self.modeltype))
            self.shifts[shift] = buffer
            
def main() :
    print "# --------------------------------------------------------------------------------------"
    print "# tangb_grid_new.py "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --tanb    :", options.tanb
    print "# --mA      :", options.mA
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"

    ## directory that contains all datacards in question
    dir = args[0]
    label = '_{MASS}_{TANB}'.format(MASS=options.mA, TANB=options.tanb)
    ## complete model for given mass and tanb value (including uncertainties)
    #model = MODEL(float(options.mA), float(options.tanb))
    models = {}
    ## adaptor of the datacard for given mass and tanb value
    adaptor = ModelDatacard(options, options.mA, label, False)
    adaptor.cleanup(dir, label)

    ## iterate through all datacards in dir
    for datacard in os.listdir(dir) :
        if not datacard.endswith('.txt') :
            continue
        ## determine decay channel and period
        card_match = re.compile('(?P<DECAY>\w*)_\w*_[0-9]?_(?P<PERIOD>[0-9]*\w*)')
        decay  = card_match.match(datacard).group('DECAY' )
        period = card_match.match(datacard).group('PERIOD')
        unique = decay+period
        ## parse datacards
        old_file = open(dir+'/'+datacard, 'r')
        card = parseCard(old_file, options)
        old_file.close()
        ## determine model
        if not unique in models.keys() :
            models[unique] = MODEL(float(options.mA), float(options.tanb))
            models[unique].setup_model(period, decay, card.list_of_signals(), ['mu', 'pdf'])
        ## adapt datacards
        adaptor.make_model_datacard(dir+'/'+datacard, models[unique].value)
        ## add uncertainty lines
        for proc in card.list_of_signals() :
            for shift in models[unique].shifts.keys() :
                moment = 1 if shift == 'mu' else 2
                adaptor.add_uncert_line(card, dir+'/'+datacard, proc, proc+'_'+shift, models[unique].value, models[unique].shifts[shift], moment)

main()
exit(0)
