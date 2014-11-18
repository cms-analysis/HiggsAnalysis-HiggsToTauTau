from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import *

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Test...\n")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
model_opts = OptionGroup(parser, "MODEL OPTIONS", "These are the options that can be passed on to configure the creation of the model datacards.")
model_opts.add_option("--parameter1", dest="parameter1", default="", type="string",
                       help="The value of the free parameter in the model. Mue (higgs/higgsino mass parameter) Default: \"\"]")
model_opts.add_option("--tanb", dest="tanb", default="", type="string",
                       help="The value of tanb in the model. Default: \"\"]")
model_opts.add_option("--model", dest="modelname", default="mhmax-mu+200", type="string",
                       help="The model which should be used (choices are: mhmax-mu+200, mhmodp, mhmodm, lowmH, tauphobic, lightstau1, lightstopmod). Default: \"mhmax-mu+200\"]")
model_opts.add_option("--ana-type", dest="ana_type", default="NeutralMSSM", type="string",
                       help="The model which should be used (choices are: NeutralMSSM, Hhh). Default: \"NeutralMSSM\"]")
model_opts.add_option("--MSSMvsSM", dest="MSSMvsSM", default=False, action="store_true",
                      help="This is needed for the signal hypothesis separation test MSSM vs SM [Default: False]")
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
morph_opts.add_option("--morphing-htaunu_had", dest="morphing_htaunu_had", default="MORPHED", type="choice",
                 help="Choose the morphing type for the htaunu_had decay channel. [Default: \"MORPHED\"]", choices=["MORPHED", "NEAREST_NEIGHBOUR"])
parser.add_option_group(morph_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

import os
import re 
import ROOT # needed for ana_type=Hhh to recalculate mH into mA
from HiggsAnalysis.HiggsToTauTau.MODEL_PARAMS import MODEL_PARAMS
from HiggsAnalysis.HiggsToTauTau.ModelDatacard import ModelDatacard
from HiggsAnalysis.HiggsToTauTau.ModelParams_BASE import ModelParams_BASE
from HiggsAnalysis.HiggsToTauTau.tools.mssm_xsec_tools import mssm_xsec_tools # needed for ana_type=Hhh to recalculate mH into mA


class MODEL(object) :
    """
    This is a class to characterize a complete physics model with cross section and BR estimates for a required set of run
    periods in terms of center of mass energy, decay channels and production processes. Though it is not a strong requirement
    uncertainties should be available also for each of these configuring parameters. The model needs to be set up consistent
    to resemble the analysed set of datacards. 
    """
    def __init__(self, parameter1, tanb, modelpath='mhmax-mu+200', modeltype='mssm_xsec') :
        ## parameter1
        # for lowmH this is mue (higgs/higgsino mass parameter) for all other scenarios this is mA
        # for ana_type=Hhh parameter1 is mH and has to be changed into corresponding mA for given mH/tanb 
        self.parameter1 = parameter1
        ## tanb
        self.tanb = tanb
        ## model path (as defined in ModelParams_BASE)
        self.modelpath = modelpath
        ## model type (as defined in ModelParams_BASE)
        self.modeltype = 'hplus_xsec' if options.ana_type=="Hplus" else 'mssm_xsec'
        ## central value of type {(period,decay,proc) : MODEL_PARAMS}
        self.central = {}
        ## shifts for uncertainties of type {'type' : {(period,decay,proc) : (MODEL_PARAMS,MODEL_PARAMS)}}
        self.uncerts = {}
        ## mass of the pseudoscalar A 
        self.mA = 0

    def missing_procs(self, decay, period, procs) :
        """
        Return a list of missing_procs in procs, which are still missing  in the model for given decay and period. Check
        centrals as it migth be some procs do not have uncertainties.
        """
        missing_procs = []
        for proc in procs :
            if not (period,decay,proc) in self.central.keys() :
                if not '_SM125' in proc :
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
        modelMaker = ModelParams_BASE(self.parameter1, self.tanb, options.ana_type)
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
        ## create masses
        if options.ana_type=="Hplus":
            self.mA = self.parameter1
        else :
            self.mA = modelMaker.create_model_params(period, proc, decay, '').masses['A']
        

def mX_to_mA(card) :
	match = re.compile('(?P<CHN>[a-zA-Z0-9]+)_[a-zA-Z0-9]+_[0-9]+_(?P<PER>[a-zA-Z0-9]+)')
        for bin in card.list_of_bins() :
        ## a bin can be made up of different decay channels or different run periods. Pick decay channel (chn) and run period
        ## (per) either from bin or from from datacards name in case it is not accessible from bin.	    
            if match.match(bin) :
                chn = match.match(bin).group('CHN')
                per = match.match(bin).group('PER')
            else :
                chn = match.match(path[path.rfind('/')+1:]).group('CHN')
                per = match.match(path[path.rfind('/')+1:]).group('PER')
        if options.ana_type=="Hhh" :
            tanbregion = ''
            if float(options.tanb) < 1:
                tanbregion = 'tanbLow'
            else:
                tanbregion = 'tanbHigh'
            mssm_xsec_tools_path = os.getenv('CMSSW_BASE')+'/src/auxiliaries/models/out.'+options.modelname+'-'+per+'-'+tanbregion+'-nnlo.root'
            prescan = mssm_xsec_tools(mssm_xsec_tools_path)
            Spline_input = ROOT.TGraph()
            k=0
            for mass in range(90, 1000) :
                Spline_input.SetPoint(k, prescan.lookup_value(mass, float(options.tanb), "h_mH"), mass)
                k=k+1
            print "for mH = ", options.parameter1, "  mA = ", Spline_input.Eval(float(options.parameter1))
            return Spline_input.Eval(float(options.parameter1))
                

            
def main() :
    print "# --------------------------------------------------------------------------------------"
    print "# tanb_grid_new.py "
    print "# --------------------------------------------------------------------------------------"
    print "# You are using the following configuration: "
    print "# --tanb                :", options.tanb
    print "# --parameter1          :", options.parameter1 #for the lowmH scenario this is the higgs/higgsino mass parameter; everywhere else its mass of A
    print "# --ana_type            :", options.ana_type
    print "# if ana_type == Hhh, only --morphing-htt_tt --morphing-htt_mt and --morphing-htt_et set for now despite printout below"
    print "# --morphing-htt_ee     : ", options.morphing_htt_ee
    print "# --morphing-htt_em     : ", options.morphing_htt_em
    print "# --morphing-htt_mm     : ", options.morphing_htt_mm
    print "# --morphing-htt_mt     : ", options.morphing_htt_mt
    print "# --morphing-htt_et     : ", options.morphing_htt_et
    print "# --morphing-htt_tt     : ", options.morphing_htt_tt
    print "# --morphing-htaunu_had : ", options.morphing_htaunu_had
    print "# Check option --help in case of doubt about the meaning of one or more of these confi-"
    print "# guration parameters.                           "
    print "# --------------------------------------------------------------------------------------"

    ## directory that contains all datacards in question
    path = args[0]
    print "path = %s" % path
    label = '_{PARAMETER1}_{TANB}'.format(PARAMETER1=options.parameter1, TANB=options.tanb)
    ## mophing configuration
    if options.ana_type=="Hhh" :
        morph= {
            'htt_mt'   : options.morphing_htt_mt,
            'htt_et'   : options.morphing_htt_et,
            'htt_tt'   : options.morphing_htt_tt,
            } 
    else :
        morph = {
            'htt_ee'     : options.morphing_htt_ee,
            'htt_em'     : options.morphing_htt_em,
            'htt_mm'     : options.morphing_htt_mm,
            'htt_mt'     : options.morphing_htt_mt,
            'htt_et'     : options.morphing_htt_et,
            'htt_tt'     : options.morphing_htt_tt,
            'htaunu_had' : options.morphing_htaunu_had,
            }
    ## complete model for given mass and tanb value (including uncertainties)
    models = {}
    ## adaptor of the datacard for given mass and tanb value
    adaptor = ModelDatacard(options, label, options.parameter1, False, options.ana_type)
    adaptor.cleanup('.' if not path.find('/')>0 else path[:path.rfind('/')], label)
    ## parse datacard (first go)
    old_file = open(path, 'r')
    card = parseCard(old_file, options)
    old_file.close()
    
    ##if ana_type=="Hhh" mH has to be translated into mA  
#    if options.ana_type=="Hhh" : #mH has to be translated into mA  
#        neededParameter = mX_to_mA(card)
#    else :
    neededParameter = options.parameter1   
        
    print options.ana_type
    ## determine MODEL for given datacard.
    model = MODEL(float(neededParameter), float(options.tanb), options.modelname)
    match = re.compile('(?P<CHN>[a-zA-Z0-9]+)_[a-zA-Z0-9]+_[0-9]+_(?P<PER>[a-zA-Z0-9]+)')
    for bin in card.list_of_bins() :
        print "processing bin = %s:" % bin 
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
            if options.ana_type=="Hplus":
                print "updating model to parameter set:", per, chn, missing_procs, ['mu']
                model.setup_model(per, chn, missing_procs, ['mu'])
            else :
                print "updating model to parameter set:", per, chn, missing_procs, ['mu', 'pdf']
                model.setup_model(per, chn, missing_procs, ['mu', 'pdf'])
    ## create new datacard
    new_name = path[:path.rfind('.txt')]+'_%.2f'%float(options.tanb)+'.txt'
    os.system("cp {SRC} {TARGET}".format(SRC=path, TARGET=new_name))
    ## adapt datacards
    if options.MSSMvsSM :
        ## this options rejects the scaling of bbH and ggH by 1/tanb -> therefore at each mA/tanb point all signals (including SM) are xs*BR
        model.tanb = 1
    adaptor.make_model_datacard(new_name, model, morph)

main()
exit(0)
