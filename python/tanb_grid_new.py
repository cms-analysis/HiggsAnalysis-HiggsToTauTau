from optparse import OptionParser, OptionGroup
from HiggsAnalysis.CombinedLimit.DatacardParser import * 

##
##
##
##  AT THE MOMENT THIS IS JUST A COLLECTION FOR THE NEW tanb_grid.py FUNCTIONALITIES
##
##
##

## set up the option parser
parser = OptionParser(usage="usage: %prog [options] ARG",
                      description="Test...\n")
parser_opts = OptionGroup(parser, "DATACARD PARSER OPTIONS", "These are the options that can be passed on to configure the datacard parsing.")
addDatacardParserOptions(parser_opts)
parser.add_option_group(parser_opts)
## check number of arguments; in case print usage
(options, args) = parser.parse_args()
## check number of arguments; in case print usage
if len(args) < 1 :
    parser.print_usage()
    exit(1)

def test(path=args[0]) :
    ## prepare dummy model
    param = MODEL_PARAMS()
    model = {'ggH': param}
    ## adapt datacards
    adaptor = ModelDatacard(options, path[path.rfind('/')+1:], model, '_new_model')
    adaptor.make_model_datacards(path)
    
test()
